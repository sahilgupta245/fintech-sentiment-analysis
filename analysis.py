#  version: 2.0

import sqlite3
import pandas as pd

# 1. Connect to your database
conn = sqlite3.connect('fintech_market.db')

# 2. UPDATED QUERY: Joining on both Date and Ticker
# This ensures Bitcoin news stays with Bitcoin prices
query = """
SELECT 
    p.Date,
    p.Ticker,
    a.Asset_Name,
    p.Close as Price,
    AVG(s.Sentiment_Score) as Avg_Sentiment,
    a.Risk_Level
FROM fact_prices p
JOIN dim_assets a 
    ON p.Ticker = a.Ticker
LEFT JOIN fact_sentiment s 
    ON p.Date = s.Date AND p.Ticker = s.Ticker
GROUP BY p.Date, p.Ticker, a.Asset_Name
ORDER BY p.Date DESC, p.Ticker ASC;
"""

# 3. Run the query and show the results
print("📊 Fetching Joined Data for 5 Assets...")
df = pd.read_sql_query(query, conn)

if df.empty:
    print("⚠️ The query returned no data. Check if Ticker names (BTC, ETH, NYSC, etc.) match exactly in all tables.")
else:
    print(f"✅ Relationships Verified! Found data for {df['Ticker'].nunique()} unique assets.")
    print("-" * 30)
    # Showing a sample that includes different assets
    print(df.sort_values(by=['Date', 'Ticker'], ascending=[False, True]).head(15))

# 4. Close connection
conn.close()



#  version: 1.0


# import sqlite3
# import pandas as pd

# # 1. Connect to your database
# conn = sqlite3.connect('fintech_market.db')

# # 2. This is the SQL query you provided
# query = """
# SELECT 
#     p.Date,
#     a.Asset_Name,
#     p.Close as Price,
#     AVG(s.Sentiment_Score) as Avg_Sentiment,
#     a.Risk_Level
# FROM fact_prices p
# JOIN dim_assets a ON p.Ticker = a.Ticker
# LEFT JOIN fact_sentiment s ON p.Date = s.Date
# GROUP BY p.Date, a.Asset_Name
# ORDER BY p.Date DESC;
# """

# # 3. Run the query and show the results
# print("📊 Fetching Joined Data...")
# df = pd.read_sql_query(query, conn)

# if df.empty:
#     print("⚠️ The query returned no data. Check if Ticker names match in all tables.")
# else:
#     print("✅ Relationships Verified! Here is your combined data:")
#     print(df.head(10))

# # 4. Close connection
# conn.close()