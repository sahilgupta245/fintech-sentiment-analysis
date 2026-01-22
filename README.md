Multi-Asset Fintech Sentiment & Price Analysis 📈🤖


🎯 Business Problem
In the volatile world of Fintech and Cryptocurrency, investors struggle to keep up with the overwhelming volume of news. The key problem this project solves is: "Does news sentiment actually drive market price, or is it just noise?"
By correlating live news headlines with price movements across different asset classes (BTC, ETH, Stablecoins, and Traditional Stocks), we provide a data-driven dashboard that helps investors:

Identify market trends before they fully materialize in price.
Compare the "emotional health" of different assets (e.g., Bitcoin vs. NYSE).
Reduce emotional trading by quantifying news as a Sentiment Score.


🛠️ The Tech Stack
Language: Python 3.10+
Data Collection: BeautifulSoup4 (Web Scraping) & yfinance (Financial Data)
NLP (AI): VADER Sentiment (Natural Language Processing)
Database: SQLite3 (Relational Data Storage)
Visualization: Power BI (Business Intelligence)
Environment: Virtualenv (Venv)


🏗️ Step-by-Step Implementation
1. Web Scraping & AI Sentiment (scraper.py)
We scrape live news from CryptoSlate. The script uses a keyword-mapping logic to categorize headlines into 5 specific tickers: BTC, ETH, USDT, STBL (Stablecoins), and NYSC (NYSE Index).
Each headline is processed through the VADER model to generate a Sentiment_Score (-1 to 1) and a Sentiment_Label (Positive, Negative, or Neutral).

2. Market Data Fetching (fetch_prices.py)
Using the yfinance API, we pull daily closing prices for all 5 assets. This ensures we have a "Source of Truth" to compare against our news data.

3. Data Engineering & ETL (load_to_sql.py)
This is the "brain" of the project. It cleans the CSV outputs and loads them into a Star Schema database (fintech_market.db):
Fact Tables: fact_sentiment and fact_prices.
Dimension Table: dim_assets (contains Asset Names and Risk Levels).

4. Interactive Dashboard (Power BI)
The data is connected to Power BI via a Python script. We built:
Sentiment vs. Price Correlation: A line chart showing price movement overlaid with sentiment peaks.
Asset Comparison Slicer: Filter all visuals by clicking on a specific asset (e.g., Ethereum).
News Feed Table: A live look at the headlines driving the sentiment scores.


🚀 How to Run
Clone the Repo:

Bash
git clone https://github.com/sahilgupta245/fintech-sentiment-analysis.git
cd fintech-sentiment-analysis
Setup Environment:

Bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Execute Data Pipeline:

Bash
python scraper.py
python fetch_prices.py
python load_to_sql.py
View Dashboard: Open the .pbix file in Power BI Desktop and hit Refresh.

📊 Key Insights Captured
NYSC vs. BTC: Visualizing how traditional market sentiment (NYSE) affects the volatility of high-risk assets (Bitcoin).
Sentiment Lead-Time: Identifying if a spike in "Negative" sentiment precedes a price drop in Ethereum.
