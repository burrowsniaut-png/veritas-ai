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





