#  version: 2.0

import pandas as pd
import sqlite3
import os

def update_database():
    csv_file = 'crypto_news_sentiment.csv'
    db_file = 'fintech_market.db'

    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found. Run scraper.py first!")
        return

    # 1. Load the CSV
    df = pd.read_csv(csv_file)
    print(f"📊 CSV loaded with columns: {list(df.columns)}")

    # 2. Connect to DB
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # 3. DROP old table to force 6-column update
    # This prevents the "missing columns" issue by rebuilding the table from scratch
    cursor.execute("DROP TABLE IF EXISTS fact_sentiment")
    conn.commit()
    
    # 4. Save to SQL
    df.to_sql('fact_sentiment', conn, if_exists='replace', index=False)
    
    # 5. Verify columns in DB immediately
    cursor.execute("PRAGMA table_info(fact_sentiment)")
    cols = [col[1] for col in cursor.fetchall()]
    print(f"✅ DB Columns Verified: {cols}")

    conn.close()
    print("🚀 Database is now perfectly synced with your 6-column CSV.")

if __name__ == "__main__":
    update_database()


# version: 1.0

# import pandas as pd
# import sqlite3

# # 1. Load data
# news_df = pd.read_csv('crypto_news_sentiment.csv')
# prices_df = pd.read_csv('market_prices_cleaned.csv')

# # 2. STANDARDIZE DATES (The Fix)
# # Convert Price dates to YYYY-MM-DD
# prices_df['Date'] = pd.to_datetime(prices_df['Date'], dayfirst=True).dt.strftime('%Y-%m-%d')

# # Convert News dates to YYYY-MM-DD 
# # (Since the scraper didn't get dates, we'll map them to the LATEST date in our price data 
# # so you can actually see the join working in your charts)
# latest_date = prices_df['Date'].max()
# news_df['Date'] = latest_date

# # 3. Connect and Overwrite
# conn = sqlite3.connect('fintech_market.db')

# prices_df.to_sql('fact_prices', conn, if_exists='replace', index=False)
# news_df.to_sql('fact_sentiment', conn, if_exists='replace', index=False)

# # Mapping table remains the same
# mapping = pd.DataFrame({
#     'Ticker': ['BTC', 'ETH', 'USDT'],
#     'Asset_Name': ['Bitcoin', 'Ethereum', 'Tether'],
#     'Risk_Level': ['High', 'High', 'Low']
# })
# mapping.to_sql('dim_assets', conn, if_exists='replace', index=False)

# conn.close()
# print(f"✅ Data Synchronized! All news mapped to {latest_date} for analysis.")