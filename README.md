# ThreatPulse 🛡️

A modern, responsive web application that aggregates cybersecurity news from multiple trusted sources using RSS feeds. Built with Python, Flask, and Google Gemini AI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Core Features
- **Multi-Source Aggregation**: Fetches news from 7 sources (The Hacker News, Krebs on Security, Bleeping Computer, Dark Reading, Threatpost, Security Week, Cybersecurity Insiders)
- **Auto-Refresh**: Automatically fetches new articles every 5 minutes in the background
- **Smart Pagination**: Choose how many articles to display per page (6, 12, 24, 48, or All)
- **Search Functionality**: Keyword search across article titles and descriptions with clear button
- **Sort Options**: View articles by newest or oldest first
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

### 🤖 AI-Powered Features
- **Severity Classification**: Google Gemini AI automatically classifies articles as HIGH 🔴, MEDIUM 🟠, or LOW 🟢 severity
- **Intelligent Reasoning**: Hover over severity badges to see AI's explanation for classification
- **Background Processing**: Articles load instantly, AI classification happens asynchronously
- **Smart Caching**: Prevents redundant API calls for previously classified articles
- **Industry Standards**: Classifications based on cybersecurity best practices

### 🎨 User Interface
- **Desktop Top Taskbar**: All filters, search, and controls organized in a clean top bar
- **Mobile Bottom Bar**: Touch-optimized navigation with filter drawer
- **8+ Color Palettes**: Blue, Purple, Green, Orange, Red, Pink, Teal, Indigo themes
- **Dark/Light Mode**: Toggle between themes with persistent localStorage
- **In-App Reading Panel**: Preview articles without leaving the page
- **Smooth Animations**: Fade-in effects and transitions throughout
- **Font Awesome Icons**: Professional visual indicators

### 🔍 Filtering & Organization
- **Source Filtering**: Filter by specific news sources or view all
- **Severity Filtering**: Filter articles by AI-classified severity level
- **Combined Filters**: Stack source, severity, and search filters
- **Filter Persistence**: Filters maintained across pagination
- **Results Summary**: Clear display of current page and total articles

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key (free tier available)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/cybersecurity-news-webapp.git
   cd cybersecurity-news-webapp
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Gemini API**:
   - Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Open `severity_analyzer.py`
   - Replace `"Paste-Your-API-Key-Here"` with your actual API key

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📚 Usage

### Web Interface

#### Desktop View
- **Top Taskbar**: All filters, search, per-page, and sort controls in organized rows
- **Severity Badges**: Color-coded badges (🔴 HIGH, 🟠 MEDIUM, 🟢 LOW) with AI reasoning on hover
- **Search Bar**: Full-width search with clear button
- **Filter Buttons**: Source and severity filters with active state highlighting

#### Mobile View
- **Bottom Navigation Bar**: 70/15/15 split for search/search-button/filter-button
- **Filter Drawer**: Slide-up panel with all filtering options
- **Optimized Layout**: Single-column article grid for easy scrolling

#### Common Features
- **Source Filtering**: Filter by specific news sources or view all
- **Severity Filtering**: Filter by HIGH/MEDIUM/LOW classification
- **Keyword Search**: Search across titles and descriptions
- **Pagination**: Navigate pages with numbers or first/prev/next/last buttons
- **Reading Panel**: In-app article preview without leaving the page
- **Scroll to Top**: Quick return button (positioned above mobile bar)
- **Color Themes**: 8+ palettes plus dark/light mode toggle

### API Endpoints

#### Get All Articles
```
GET /api/articles?source=all&limit=50
```

#### Get Classification Status
```
GET /api/classification-status
```
Returns: `{"classified": true/false, "article_count": 73}`

#### Force Refresh
```
GET /api/refresh
```
{
  "success": true,
  "articles_count": 105,
  "last_updated": "2025-11-20T10:30:00"
}
```

#### Get Article Content
```
GET /api/article-content?url=<article_url>
```

**Query Parameters**:
- `url` (required): The URL of the article to fetch

**Response**:
```json
{
  "success": true,
  "title": "Article Title",
  "content": "<html>...</html>",
  "url": "https://..."
}
```

## 📋 News Sources

The application aggregates news from:

- **The Hacker News** - Latest cybersecurity and hacking news
- **Krebs on Security** - In-depth security news and investigation
- **Bleeping Computer** - Technology news and security alerts
- **Dark Reading** - Cybersecurity news for infosec professionals
- **Threatpost** - The first stop for security news
- **Security Week** - Enterprise security news
- **Cybersecurity Insiders** - Latest cybersecurity trends

## 🛠️ Technology Stack

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Flask 3.0.0
- **AI/ML**: Google Gemini API (gemini-2.5-flash)
- **RSS Parsing**: feedparser 6.0.11, BeautifulSoup4
- **Frontend**: HTML5, CSS3 (Custom Properties), Vanilla JavaScript
- **Icons**: Font Awesome 6.4.0
- **HTTP Client**: requests 2.31.0
- **Server**: Flask development server / Gunicorn (production)

## 📁 Project Structure

```
cybersecurity-news-webapp/
├── app.py                    # Main Flask application with routes
├── rss_fetcher.py           # RSS feed aggregation logic
├── severity_analyzer.py     # Gemini AI integration for classification
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── README.md               # Project documentation
├── templates/              # Jinja2 HTML templates
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Main article feed page
│   ├── about.html         # About page
│   ├── 404.html           # 404 error page
│   └── 500.html           # 500 error page
└── static/                # Static assets
    └── css/
        └── style.css      # Main stylesheet (2700+ lines)
```

## 🤖 AI Classification Details

### How It Works
1. Articles load instantly on page load
2. Gemini AI classifies articles in background (0.3s delay between calls)
3. Status indicator shows "AI severity classification in progress..."
4. Page auto-reloads when classification completes
5. Severity badges appear with hover tooltips explaining classification

### Classification Criteria
- **HIGH** 🔴: Critical vulnerabilities, active exploits, zero-days, ransomware, nation-state attacks
- **MEDIUM** 🟠: Important security updates, newly discovered vulnerabilities, security tool releases
- **LOW** 🟢: General security news, tips, educational content, minor patches

### Caching & Performance
- In-memory cache prevents duplicate API calls
- Cached by article title
- Rate limiting respects API quotas
- Background threading ensures non-blocking UI

## ⚙️ Configuration

### Environment Variables (Optional)
Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

Then edit `.env` with your values.

### Customizing RSS Feeds

Edit the `RSS_FEEDS` dictionary in `rss_fetcher.py`:

```python
RSS_FEEDS = {
    'Source Name': 'https://source.com/feed.xml',
    # Add more sources...
}
```

### Auto-Refresh Interval

Modify the refresh interval in `app.py`:

```python
CACHE_DURATION_MINUTES = 5  # Change to your preferred duration (in minutes)
```

**Note**: Both backend and frontend will automatically use this interval for synchronization.

## 🚀 Production Deployment

For production use, it's recommended to use a production-ready WSGI server:

### Using Gunicorn

```powershell
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Waitress (Windows-friendly)

```powershell
pip install waitress
waitress-serve --port=5000 app:app
```

## 🔧 Troubleshooting

### Issue: RSS feeds not loading

- Check your internet connection
- Some RSS feeds may be temporarily unavailable
- Verify RSS feed URLs are correct in `rss_fetcher.py`

### Issue: Port 5000 already in use

Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Use different port
```

### Issue: Module not found errors

Ensure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions

- Add more RSS news sources
- Implement user authentication
- Add article bookmarking
- Create email alerts for specific keywords
- Add search functionality
- Implement article categories/tags
- Add notification system for breaking news
- Customize auto-refresh intervals per user
- Add article read/unread tracking

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Created with ❤️ for the cybersecurity community

## 🙏 Acknowledgments

- All the cybersecurity news sources for providing RSS feeds
- Flask framework developers
- feedparser library maintainers
- Font Awesome for the icons

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review existing issues on GitHub
3. Open a new issue with detailed information

## 🔮 Future Enhancements

- [ ] Database integration for article history
- [ ] User accounts and personalized feeds
- [ ] Email notifications for breaking news
- [ ] Advanced search and filtering
- [ ] Article sentiment analysis
- [ ] Related articles suggestions
- [ ] Export articles to PDF/CSV
- [ ] Mobile app version
- [ ] Dark/Light theme toggle
- [ ] Keyword highlighting

---

**Stay informed, stay secure!** 🛡️
