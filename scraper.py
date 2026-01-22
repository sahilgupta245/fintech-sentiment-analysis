# This is a web scraper that collects cryptocurrency news headlines from CryptoSlate version 2.0
import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

# --- CONFIGURATION ---
URL = "https://cryptoslate.com/news/" 
OUTPUT_FILE = "crypto_news_sentiment.csv"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def get_sentiment_label(score):
    if score >= 0.05: return 'Positive'
    elif score <= -0.05: return 'Negative'
    return 'Neutral'

def run_scraper():
    print(f"🌐 Connecting to {URL}...")
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    analyzer = SentimentIntensityAnalyzer()
    all_news = []
    
    articles = soup.find_all("div", class_="news-card__body")
    print(f"🔍 Found {len(articles)} headlines. Categorizing and labeling...")

    # Keywords mapping for all 5 assets
    keywords = {
        'BTC': ['bitcoin', 'btc'],
        'ETH': ['ethereum', 'eth', 'vitalik'],
        'USDT': ['tether', 'usdt'],
        'STBL': ['stablecoin', 'usdc', 'dai', 'circle'],
        'NYSC': ['nyse', 'stock', 'market', 'wall street', 'fed', 'inflation']
    }

    for article in articles:
        title_tag = article.find("h2")
        if not title_tag: continue
        
        headline = title_tag.get_text().strip()
        score = analyzer.polarity_scores(headline)['compound']
        
        # Ticker Identification
        found_ticker = "BTC" # Default
        headline_lower = headline.lower()
        for ticker, keys in keywords.items():
            if any(key in headline_lower for key in keys):
                found_ticker = ticker
                break
        
        # Build the full row with all requested columns
        all_news.append({
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Ticker': found_ticker,
            'Headline': headline,
            'Sentiment_Score': score,
            'Sentiment_Label': get_sentiment_label(score), # Restored
            'Source': 'CryptoSlate'                        # Restored
        })

    if all_news:
        df = pd.DataFrame(all_news)
        try:
            df.to_csv(OUTPUT_FILE, index=False)
            print(f"✅ Success! {OUTPUT_FILE} created with 6 columns and all tickers.")
            print(df.head()) 
        except PermissionError:
            print("❌ Permission Denied: Close 'crypto_news_sentiment.csv' in Excel and try again!")
    else:
        print("⚠️ No news found.")

if __name__ == "__main__":
    run_scraper()




# this is a web scraper that collects cryptocurrency news headlines from CryptoSlate version 1.0,

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from datetime import datetime
# import time

# # --- CONFIGURATION ---
# # We target CryptoSlate because it often has a cleaner HTML structure for scraping
# TARGET_URL = "https://cryptoslate.com/news/"
# OUTPUT_FILE = "crypto_news_sentiment.csv"

# # --- HEADERS (The "Pro" Touch) ---
# # Websites block Python requests. This header makes us look like a Chrome Browser.
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# }

# def fetch_html(url):
#     """Fetches raw HTML from the website."""
#     try:
#         response = requests.get(url, headers=HEADERS)
#         response.raise_for_status() # Raises error if status is 404/500
#         print(f"✅ Successfully connected to {url}")
#         return response.text
#     except requests.exceptions.RequestException as e:
#         print(f"❌ Error fetching data: {e}")
#         return None

# def parse_headlines(html_content):
#     """Extracts headlines using the classes found in your screenshot."""
#     soup = BeautifulSoup(html_content, "html.parser")
#     news_data = []

#     # 1. Target the specific container for article text
#     # The screenshot shows 'news-card__body', so we loop through those
#     articles = soup.find_all("div", class_="news-card__body")

#     print(f"🔍 Found {len(articles)} articles. Processing...")

#     for article in articles:
#         try:
#             # 2. Extract Headline (Directly from your screenshot)
#             # We look for h2 with class 'news-card__title'
#             title_tag = article.find("h2", class_="news-card__title")
            
#             # If no headline is found, skip this item
#             if not title_tag:
#                 continue
            
#             headline = title_tag.get_text().strip()
            
#             # 3. Extract Date
#             # It's likely in 'news-card__footer' (bottom) or 'news-card__meta' (top)
#             # We check the footer first
#             date_tag = article.find("div", class_="news-card__footer")
            
#             # Fallback: If footer is missing, check 'news-card__meta'
#             if not date_tag:
#                 date_tag = article.find("div", class_="news-card__meta")
                
#             # If we found a tag, use its text; otherwise use today's date
#             post_date = date_tag.get_text().strip() if date_tag else datetime.now().strftime("%Y-%m-%d")

#             news_data.append({
#                 "Date": post_date,
#                 "Headline": headline,
#                 "Source": "CryptoSlate"
#             })
#         except Exception as e:
#             # In production, we might log this error to a file
#             continue 
            
#     return news_data

# def analyze_sentiment(news_list):
#     """Adds a Sentiment Score to every headline."""
#     analyzer = SentimentIntensityAnalyzer()
    
#     for item in news_list:
#         score = analyzer.polarity_scores(item['Headline'])
#         # Compound score ranges from -1 (Negative) to 1 (Positive)
#         item['Sentiment_Score'] = score['compound']
        
#         # Tagging for the Dashboard
#         if item['Sentiment_Score'] >= 0.05:
#             item['Sentiment_Label'] = 'Positive'
#         elif item['Sentiment_Score'] <= -0.05:
#             item['Sentiment_Label'] = 'Negative'
#         else:
#             item['Sentiment_Label'] = 'Neutral'
            
#     return news_list

# def main():
#     # 1. Get Data
#     html = fetch_html(TARGET_URL)
    
#     if html:
#         # 2. Parse HTML
#         raw_news = parse_headlines(html)
        
#         if not raw_news:
#             print("⚠️ No news found. The website structure might have changed.")
#             return

#         # 3. Analyze Sentiment (NLP)
#         enriched_data = analyze_sentiment(raw_news)
        
#         # 4. Save to CSV (ETL End)
#         df = pd.DataFrame(enriched_data)
        
#         # Clean Date formatting (Optional but recommended)
#         # df['Date'] = pd.to_datetime(df['Date']) 
        
#         df.to_csv(OUTPUT_FILE, index=False)
#         print(f"🚀 Success! Scraped {len(df)} headlines. Saved to {OUTPUT_FILE}")
#         print(df.head()) # Preview for the user

# if __name__ == "__main__":
#     main()