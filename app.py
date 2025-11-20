"""
Cybersecurity News Web Application
A Flask-based web app for aggregating cybersecurity news from multiple sources
"""

from flask import Flask, render_template, request, jsonify
from rss_fetcher import RSSFetcher, get_latest_news
from severity_analyzer import classify_articles_batch
import logging
from datetime import datetime
import threading
import time
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cybersec-news-webapp-2025'

# Initialize RSS fetcher
rss_fetcher = RSSFetcher()

# Cache for storing fetched articles
articles_cache = {
    'articles': [],
    'last_updated': None,
    'classified': False
}

CACHE_DURATION_MINUTES = 5


def should_refresh_cache():
    """Check if cache should be refreshed"""
    if not articles_cache['last_updated']:
        return True
    
    time_diff = datetime.now() - articles_cache['last_updated']
    return time_diff.total_seconds() > (CACHE_DURATION_MINUTES * 60)


def refresh_articles():
    """Refresh the articles cache - classification happens in background"""
    try:
        logger.info("Refreshing articles cache...")
        articles = get_latest_news(limit_per_source=15)
        
        # Update cache immediately without classification
        articles_cache['articles'] = articles
        articles_cache['last_updated'] = datetime.now()
        articles_cache['classified'] = False
        logger.info(f"Cache refreshed with {len(articles)} articles")
        
        # Start background thread to classify articles
        classification_thread = threading.Thread(target=classify_articles_in_background, args=(articles,))
        classification_thread.daemon = True
        classification_thread.start()
        
        return articles
    except Exception as e:
        logger.error(f"Error refreshing articles: {str(e)}")
        return articles_cache['articles']


def classify_articles_in_background(articles):
    """Background thread to classify articles without blocking"""
    try:
        logger.info("Background classification started...")
        classified_articles = classify_articles_batch(articles, delay=0.3)
        
        # Update cache with classified articles
        articles_cache['articles'] = classified_articles
        articles_cache['classified'] = True
        logger.info(f"Background classification completed for {len(classified_articles)} articles")
    except Exception as e:
        logger.error(f"Error in background classification: {str(e)}")


def auto_refresh_articles():
    """Background thread to automatically refresh articles every 5 minutes"""
    while True:
        try:
            time.sleep(CACHE_DURATION_MINUTES * 60)  # Sleep for 5 minutes
            logger.info("Auto-refresh triggered")
            refresh_articles()
        except Exception as e:
            logger.error(f"Error in auto-refresh thread: {str(e)}")
            time.sleep(60)  # Wait 1 minute before retrying on error


@app.route('/')
def index():
    """Main page showing all cybersecurity news"""
    if should_refresh_cache():
        refresh_articles()
    
    # Get filter parameters
    source_filter = request.args.get('source', 'all')
    severity_filter = request.args.get('severity', 'all')
    search_query = request.args.get('search', '').strip()
    sort_order = request.args.get('sort', 'newest')  # 'newest' or 'oldest'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    
    # Validate per_page
    if per_page not in [6, 12, 24, 48, 0]:  # 0 means 'All'
        per_page = 12
    
    # Validate sort_order
    if sort_order not in ['newest', 'oldest']:
        sort_order = 'newest'
    
    # Validate severity_filter
    if severity_filter not in ['all', 'high', 'medium', 'low']:
        severity_filter = 'all'
    
    articles = articles_cache['articles'].copy()
    
    # Apply source filter
    if source_filter != 'all':
        articles = [a for a in articles if a['source'] == source_filter]
    
    # Apply severity filter
    if severity_filter != 'all':
        articles = [a for a in articles if a.get('severity', 'MEDIUM').lower() == severity_filter.lower()]
    
    # Apply search filter
    if search_query:
        search_lower = search_query.lower()
        articles = [
            a for a in articles 
            if search_lower in a['title'].lower() or 
               search_lower in a.get('description', '').lower()
        ]
    
    # Apply sorting
    if sort_order == 'oldest':
        articles.reverse()  # Original cache is sorted newest first
    
    total_articles = len(articles)
    
    # Handle pagination
    if per_page == 0:  # Show all
        paginated_articles = articles
        total_pages = 1
        page = 1
    else:
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_articles = articles[start_idx:end_idx]
        total_pages = (total_articles + per_page - 1) // per_page  # Ceiling division
        
        # Ensure page is within valid range
        if page > total_pages and total_pages > 0:
            page = total_pages
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            paginated_articles = articles[start_idx:end_idx]
    
    sources = rss_fetcher.get_sources()
    
    return render_template(
        'index.html',
        articles=paginated_articles,
        sources=sources,
        selected_source=source_filter,
        selected_severity=severity_filter,
        search_query=search_query,
        sort_order=sort_order,
        last_updated=articles_cache['last_updated'],
        current_page=page,
        total_pages=total_pages,
        per_page=per_page,
        total_articles=total_articles,
        classification_complete=articles_cache['classified']
    )


@app.route('/api/articles')
def api_articles():
    """API endpoint to get articles in JSON format"""
    if should_refresh_cache():
        refresh_articles()
    
    source_filter = request.args.get('source', 'all')
    limit = request.args.get('limit', 50, type=int)
    
    articles = articles_cache['articles'][:limit]
    
    # Apply source filter
    if source_filter != 'all':
        articles = [a for a in articles if a['source'] == source_filter]
    
    return jsonify({
        'articles': [{
            'title': a['title'],
            'link': a['link'],
            'published': a['published'].isoformat(),
            'summary': a['summary'],
            'source': a['source'],
            'author': a['author']
        } for a in articles],
        'total': len(articles),
        'last_updated': articles_cache['last_updated'].isoformat() if articles_cache['last_updated'] else None
    })


@app.route('/api/sources')
def api_sources():
    """API endpoint to get available news sources"""
    sources = rss_fetcher.get_sources()
    return jsonify({
        'sources': sources,
        'total': len(sources)
    })


@app.route('/api/refresh')
def api_refresh():
    """API endpoint to force refresh the articles cache"""
    articles = refresh_articles()
    return jsonify({
        'success': True,
        'articles_count': len(articles),
        'last_updated': articles_cache['last_updated'].isoformat()
    })


@app.route('/api/classification-status')
def api_classification_status():
    """API endpoint to check if classification is complete"""
    return jsonify({
        'classified': articles_cache['classified'],
        'article_count': len(articles_cache['articles'])
    })


@app.route('/api/article-content')
def api_article_content():
    """API endpoint to fetch article content for reading view"""
    article_url = request.args.get('url')
    
    if not article_url:
        return jsonify({'error': 'URL parameter is required'}), 400
    
    try:
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the article page
        response = requests.get(article_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'advertisement']):
            element.decompose()
        
        # Try to find article content
        article_content = None
        
        # Common article selectors
        selectors = [
            'article',
            '[role="main"]',
            '.article-content',
            '.post-content',
            '.entry-content',
            '.content',
            'main'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                article_content = element
                break
        
        if not article_content:
            # Fallback to body if no article element found
            article_content = soup.find('body')
        
        # Extract title
        title = soup.find('title')
        title_text = title.string if title else 'Article'
        
        # Clean up the content
        if article_content:
            # Convert to string and clean up
            content_html = str(article_content)
            
            return jsonify({
                'success': True,
                'title': title_text,
                'content': content_html,
                'url': article_url
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not extract article content'
            }), 404
            
    except requests.Timeout:
        return jsonify({
            'success': False,
            'error': 'timeout',
            'message': 'Request timeout - article took too long to load',
            'url': article_url
        }), 504
    except requests.HTTPError as e:
        if e.response.status_code == 403:
            return jsonify({
                'success': False,
                'error': 'forbidden',
                'message': 'Unable to access this article due to security restrictions',
                'url': article_url
            }), 403
        return jsonify({
            'success': False,
            'error': 'http_error',
            'message': f'Failed to fetch article: {str(e)}',
            'url': article_url
        }), e.response.status_code if hasattr(e, 'response') else 500
    except requests.RequestException as e:
        logger.error(f"Error fetching article content: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'request_failed',
            'message': 'Failed to fetch article content',
            'url': article_url
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'unknown',
            'message': 'An unexpected error occurred',
            'url': article_url
        }), 500


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', sources=rss_fetcher.get_sources())


@app.template_filter('time_ago')
def time_ago_filter(dt):
    """Convert datetime to human-readable 'time ago' format"""
    if not isinstance(dt, datetime):
        return str(dt)
    
    now = datetime.now()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal error: {str(error)}")
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Initial cache load
    refresh_articles()
    
    # Start auto-refresh background thread
    auto_refresh_thread = threading.Thread(target=auto_refresh_articles, daemon=True)
    auto_refresh_thread.start()
    logger.info(f"Auto-refresh thread started (interval: {CACHE_DURATION_MINUTES} minutes)")
    
    # Run the app
    print("\n" + "="*60)
    print("  Cybersecurity News Web Application")
    print("="*60)
    print("\n  Server starting at http://localhost:5000")
    print(f"  Auto-refresh enabled: Every {CACHE_DURATION_MINUTES} minutes")
    print("  Press CTRL+C to quit\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
