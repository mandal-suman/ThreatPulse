"""
RSS Feed Fetcher for Cybersecurity News
Fetches and parses news from multiple cybersecurity sources
"""

import feedparser
from datetime import datetime
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RSS Feed Sources
RSS_FEEDS = {
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
    'Krebs on Security': 'https://krebsonsecurity.com/feed/',
    'Bleeping Computer': 'https://www.bleepingcomputer.com/feed/',
    'Dark Reading': 'https://www.darkreading.com/rss.xml',
    'Threatpost': 'https://threatpost.com/feed/',
    'Security Week': 'https://www.securityweek.com/feed/',
    'Cybersecurity Insiders': 'https://www.cybersecurity-insiders.com/feed/',
}


class RSSFetcher:
    """Fetches and parses RSS feeds from cybersecurity news sources"""
    
    def __init__(self, feeds: Dict[str, str] = None):
        self.feeds = feeds if feeds else RSS_FEEDS
    
    def fetch_feed(self, source_name: str, feed_url: str, limit: int = 10) -> List[Dict]:
        """
        Fetch and parse a single RSS feed
        
        Args:
            source_name: Name of the news source
            feed_url: URL of the RSS feed
            limit: Maximum number of articles to fetch
            
        Returns:
            List of article dictionaries
        """
        try:
            logger.info(f"Fetching feed from {source_name}")
            feed = feedparser.parse(feed_url)
            
            articles = []
            for entry in feed.entries[:limit]:
                article = {
                    'title': entry.get('title', 'No Title'),
                    'link': entry.get('link', '#'),
                    'published': self._parse_date(entry),
                    'summary': self._clean_summary(entry.get('summary', 'No summary available')),
                    'source': source_name,
                    'author': entry.get('author', 'Unknown'),
                }
                articles.append(article)
            
            logger.info(f"Successfully fetched {len(articles)} articles from {source_name}")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching feed from {source_name}: {str(e)}")
            return []
    
    def fetch_all_feeds(self, limit_per_feed: int = 10) -> List[Dict]:
        """
        Fetch articles from all configured RSS feeds
        
        Args:
            limit_per_feed: Maximum number of articles per feed
            
        Returns:
            List of all articles from all sources
        """
        all_articles = []
        
        for source_name, feed_url in self.feeds.items():
            articles = self.fetch_feed(source_name, feed_url, limit_per_feed)
            all_articles.extend(articles)
        
        # Sort by published date (newest first)
        all_articles.sort(key=lambda x: x['published'], reverse=True)
        
        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles
    
    def _parse_date(self, entry) -> datetime:
        """Parse the publication date from an entry"""
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                return datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                return datetime(*entry.updated_parsed[:6])
            else:
                return datetime.now()
        except Exception:
            return datetime.now()
    
    def _clean_summary(self, summary: str, max_length: int = 300) -> str:
        """Clean and truncate the summary text"""
        # Remove HTML tags
        import re
        clean_text = re.sub('<[^<]+?>', '', summary)
        
        # Truncate if too long
        if len(clean_text) > max_length:
            clean_text = clean_text[:max_length] + '...'
        
        return clean_text
    
    def get_sources(self) -> List[str]:
        """Get list of all news sources"""
        return list(self.feeds.keys())


def get_latest_news(limit_per_source: int = 10) -> List[Dict]:
    """
    Convenience function to get latest news from all sources
    
    Args:
        limit_per_source: Maximum articles per source
        
    Returns:
        List of article dictionaries
    """
    fetcher = RSSFetcher()
    return fetcher.fetch_all_feeds(limit_per_source)


if __name__ == '__main__':
    # Test the fetcher
    fetcher = RSSFetcher()
    articles = fetcher.fetch_all_feeds(limit_per_feed=5)
    
    print(f"\nFetched {len(articles)} articles:\n")
    for article in articles[:10]:
        print(f"[{article['source']}] {article['title']}")
        print(f"Published: {article['published'].strftime('%Y-%m-%d %H:%M')}")
        print(f"Link: {article['link']}\n")
