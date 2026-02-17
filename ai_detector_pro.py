import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text from main content areas first
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        
        if main_content:
            text = main_content.get_text(separator=' ', strip=True)
        else:
            # Fallback to body text
            text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit to 3000 chars for analysis
        return text[:3000]
        
    except Exception as e:
        return f"Error scraping website: {str(e)}"

def analyze_with_deepseek(text):
    import requests
    import json
    
    url = "https://deena-proadvertizing-XXXX.ngrok-free.app/api/generate"
    
    data = {
        "model": "deepseek-r1:1.5b",
        "prompt": f"Analyze this text and determine if it was written by a human or AI. Give a percentage estimate (0-100%) and brief reasoning. Text: {text[:2000]}",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=600)
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        return f"Error analyzing text: {str(e)}"

