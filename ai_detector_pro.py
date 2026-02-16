import requests
from playwright.sync_api import sync_playwright
import time
import json

def scrape_website(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=60000)
        text = page.inner_text('body')[:3000]
        browser.close()
        return text

def analyze_with_deepseek(text):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "deepseek-r1:1.5b",
        "prompt": f"Is this text written by a human or AI? Give percentage and brief reason. Text: {text[:1500]}",
        "stream": False
    }
    # 10 minute timeout
    response = requests.post(url, json=data, timeout=600)
    return response.json()['response']

# Get URLs (max 25)
urls = []
print("Enter URLs (one per line). Type 'done' when finished. Max 25:")
while len(urls) < 25:
    url = input("URL: ").strip()
    if url.lower() == 'done':
        break
    if url:
        if not url.startswith('http'):
            url = 'https://' + url
        urls.append(url)

results = []

for i, url in enumerate(urls, 1):
    print(f"\n{'='*60}")
    print(f"[{i}/{len(urls)}] {url}")
    print(f"{'='*60}")
    
    try:
        text = scrape_website(url)
        print(f"Scraped {len(text)} chars")
        
        print("Analyzing (up to 10 minutes)...")
        result = analyze_with_deepseek(text)
        
        print(f"\nVERITAS ANALYSIS:")
        print(result)
        print(f"{'='*60}\n")
        
        results.append({"url": url, "analysis": result, "status": "ok"})
        
        with open('veritas_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        if i < len(urls):
            print("Cooling down (5s)...")
            time.sleep(5)
            
    except Exception as e:
        print(f"\nFAILED: {e}")
        results.append({"url": url, "error": str(e), "status": "fail"})
        with open('veritas_results.json', 'w') as f:
            json.dump(results, f, indent=2)

print(f"\n{'='*60}")
print(f"DONE. {len([r for r in results if r['status']=='ok'])} succeeded.")
print(f"{'='*60}")