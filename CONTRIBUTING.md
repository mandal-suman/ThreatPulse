# Contributing to Cybersecurity News Web Application

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs
- Use GitHub Issues to report bugs
- Include detailed steps to reproduce
- Specify your environment (OS, Python version, browser)
- Include screenshots if applicable

### Suggesting Features
- Open a GitHub Issue with the "enhancement" label
- Clearly describe the feature and its benefits
- Explain potential use cases

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 Code Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Handle exceptions appropriately

### Frontend Code
- Use semantic HTML5
- Keep CSS organized by component
- Comment complex logic
- Ensure responsive design
- Test across browsers

### Commits
- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issues when applicable

## 🧪 Testing
- Test all new features before submitting
- Verify mobile responsiveness
- Check dark/light mode compatibility
- Test with multiple color palettes
- Validate API endpoints

## 📋 Adding New RSS Sources
To add a new cybersecurity news source:
1. Open `rss_fetcher.py`
2. Add to `RSS_FEEDS` dictionary:
   ```python
   'Source Name': 'https://example.com/feed.rss'
   ```
3. Test feed parsing
4. Update documentation

## 🎨 UI/UX Improvements
When making UI changes:
- Maintain consistent design language
- Ensure accessibility (ARIA labels, contrast ratios)
- Test keyboard navigation
- Verify mobile responsiveness
- Keep performance in mind

## 🔒 Security
- Never commit API keys or secrets
- Use environment variables for sensitive data
- Report security vulnerabilities privately
- Follow secure coding practices

## 📄 Documentation
- Update README.md for major features
- Add comments to complex code
- Update API documentation
- Include usage examples

## ❓ Questions?
Feel free to open a GitHub Discussion or Issue for any questions!

Thank you for contributing! 🎉
