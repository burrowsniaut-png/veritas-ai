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
def analyze_with_deepseek(text):
    import requests
    
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": "Bearer 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"}
    
    prompt = f"Analyze this text and determine if it was written by a human or AI. Give a percentage estimate (0-100%) and brief reasoning. Text: {text[:1000]}"
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', 'No analysis generated')
        else:
            return str(result)
            
    except Exception as e:
        return f"Error analyzing text: {str(e)}"        
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





