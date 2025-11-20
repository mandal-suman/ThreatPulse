"""
Severity Analyzer using Google Gemini API
Classifies cybersecurity news articles by severity level
"""

import google.generativeai as genai
import logging
import json
from typing import Dict, Optional
import time

logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = "Paste-Your-API-Key-Here"
genai.configure(api_key=GEMINI_API_KEY)

# List available models and use the first suitable one
try:
    available_models = genai.list_models()
    logger.info("Available Gemini models:")
    for m in available_models:
        if 'generateContent' in m.supported_generation_methods:
            logger.info(f"  - {m.name} (supports generateContent)")
    
    # Try to find a suitable model (prefer gemini-2.5-flash or gemini-2.0-flash)
    model_name = None
    preferred_models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-flash-latest']
    
    # First, try preferred models
    for preferred in preferred_models:
        for m in available_models:
            if 'generateContent' in m.supported_generation_methods:
                # Use the full model name with 'models/' prefix
                if preferred in m.name:
                    model_name = m.name
                    break
        if model_name:
            break
    
    # If no preferred model found, use the first available
    if not model_name:
        for m in available_models:
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name
                break
    
    if not model_name:
        raise Exception("No suitable model found")
    
    logger.info(f"Using model: {model_name}")
    model = genai.GenerativeModel(model_name)
except Exception as e:
    logger.error(f"Error initializing Gemini model: {e}")
    # Fallback
    model = genai.GenerativeModel('models/gemini-2.5-flash')

# Cache for severity classifications
severity_cache: Dict[str, Dict] = {}


def classify_severity(article: Dict) -> Dict:
    """
    Classify the severity of a cybersecurity news article using Gemini API.
    
    Args:
        article: Dictionary containing article data (title, description, link)
    
    Returns:
        Dictionary with severity level and reasoning
    """
    # Create a cache key from article title
    cache_key = article.get('title', '')
    
    # Check cache first
    if cache_key in severity_cache:
        return severity_cache[cache_key]
    
    try:
        # Prepare the prompt for Gemini
        prompt = f"""
You are a cybersecurity expert. Analyze the following cybersecurity news article and classify its severity level based on industry standards.

Article Title: {article.get('title', '')}
Article Description: {article.get('description', '')}

Classification criteria:
- HIGH: Critical vulnerabilities, active exploits, widespread attacks, data breaches affecting many users, zero-day vulnerabilities, ransomware campaigns, nation-state attacks
- MEDIUM: Important security updates, newly discovered vulnerabilities (not yet exploited), significant security incidents, emerging threats, security tool releases
- LOW: General security news, minor updates, educational content, security tips, company announcements, minor patches

Provide your response in the following JSON format only (no additional text):
{{
    "severity": "HIGH" or "MEDIUM" or "LOW",
    "reasoning": "Brief explanation (max 100 characters) why this classification was chosen"
}}
"""
        
        # Call Gemini API
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Try to extract JSON from the response
        # Handle cases where response might have markdown code blocks
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        elif '```' in response_text:
            json_start = response_text.find('```') + 3
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        
        # Parse the JSON response
        result = json.loads(response_text)
        
        # Validate the response
        if 'severity' not in result or 'reasoning' not in result:
            raise ValueError("Invalid response format from Gemini")
        
        # Ensure severity is uppercase and valid
        severity = result['severity'].upper()
        if severity not in ['HIGH', 'MEDIUM', 'LOW']:
            severity = 'MEDIUM'  # Default to MEDIUM if invalid
        
        classification = {
            'severity': severity,
            'reasoning': result['reasoning'][:150]  # Limit reasoning length
        }
        
        # Cache the result
        severity_cache[cache_key] = classification
        
        logger.info(f"Classified article '{article.get('title', '')[:50]}...' as {severity}")
        
        return classification
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response: {e}")
        logger.error(f"Response text: {response_text}")
        return {
            'severity': 'MEDIUM',
            'reasoning': 'Classification unavailable'
        }
    except Exception as e:
        logger.error(f"Error classifying article severity: {str(e)}")
        return {
            'severity': 'MEDIUM',
            'reasoning': 'Classification unavailable'
        }


def classify_articles_batch(articles: list, delay: float = 1.0) -> list:
    """
    Classify multiple articles with rate limiting to avoid API quota issues.
    
    Args:
        articles: List of article dictionaries
        delay: Delay in seconds between API calls
    
    Returns:
        List of articles with severity classifications added
    """
    classified_articles = []
    
    for i, article in enumerate(articles):
        # Add severity classification
        classification = classify_severity(article)
        article['severity'] = classification['severity']
        article['severity_reasoning'] = classification['reasoning']
        
        classified_articles.append(article)
        
        # Add delay between API calls (except for last article)
        if i < len(articles) - 1:
            time.sleep(delay)
    
    return classified_articles


def clear_cache():
    """Clear the severity classification cache."""
    global severity_cache
    severity_cache = {}
    logger.info("Severity classification cache cleared")


def get_cache_size() -> int:
    """Get the number of cached classifications."""
    return len(severity_cache)
