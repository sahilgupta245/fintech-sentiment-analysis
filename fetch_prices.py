# version: 2.0

import yfinance as yf
import pandas as pd

# Define your 5 specific assets with correct Yahoo Finance symbols
# BTC, ETH, USDT, USDC (for STBL), and ^NYA (for NYSC)
assets = ["BTC-USD", "ETH-USD", "USDT-USD", "USDC-USD", "^NYA"]

def get_market_data(tickers):
    print(f"📈 Fetching prices for {tickers}...")
    data = yf.download(tickers, period="30d", interval="1d")
    
    df_long = data.stack(level=1).reset_index()
    df_long.columns = ['Date', 'Ticker', 'Close', 'High', 'Low', 'Open', 'Volume']
    
    # Clean up the names to match your dim_assets table
    mapping = {
        'BTC-USD': 'BTC',
        'ETH-USD': 'ETH',
        'USDT-USD': 'USDT',
        'USDC-USD': 'STBL',
        '^NYA': 'NYSC'
    }
    df_long['Ticker'] = df_long['Ticker'].map(mapping)
    
    return df_long

price_df = get_market_data(assets)
price_df.to_csv("market_prices_cleaned.csv", index=False)
print("✅ Success! 5 Assets saved to market_prices_cleaned.csv")


# version: 1.0

# import yfinance as yf
# import pandas as pd

# # 1. Define assets
# assets = ["BTC-USD", "ETH-USD", "USDT-USD"]

# def get_market_data(tickers):
#     print(f"📈 Fetching and structuring prices for {tickers}...")
    
#     # Download all at once
#     data = yf.download(tickers, period="30d", interval="1d")
    
#     # MAGIC STEP: The 'Stack' operation 
#     # This moves the Ticker names from the columns into the rows
#     df_long = data.stack(level=1).reset_index()
    
#     # Clean up column names
#     df_long.columns = ['Date', 'Ticker', 'Close', 'High', 'Low', 'Open', 'Volume']
    
#     # Simplify Tickers (BTC-USD -> BTC)
#     df_long['Ticker'] = df_long['Ticker'].str.replace('-USD', '')
    
#     return df_long

# # 2. Run and Save
# price_df = get_market_data(assets)
# price_df.to_csv("market_prices_cleaned.csv", index=False)
# print("✅ Success! Cleaned data saved to market_prices_cleaned.csv")
# print(price_df.head())