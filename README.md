# Stock Market Analyzer

An interactive dashboard to analyze Indian stocks (NSE): price trends, moving averages, volatility, and comparison between stocks.

# Live app:

 https://stock-analyzer-dxjtvk68ffufrb3kkgea7k.streamlit.app/

> For learning only, not financial advice.

## Features

- Pick a stock and a date range from the sidebar
- Metric cards: current price, total return, average daily return, volatility
- Price chart with 20-day and 50-day moving averages
- Candlestick chart, trading volume, and daily returns distribution
- Compare page: growth of Rs 1, correlation heatmap, risk vs return, summary table

## Data Source

Live stock prices from Yahoo Finance, fetched with the yfinance library. No CSV file is needed. Stocks used: Reliance, TCS, Infosys, HDFC Bank, ICICI Bank, ITC.

## Tools Used

Python, pandas, NumPy, Plotly, Streamlit, yfinance, Jupyter Notebook (VS Code)

## What I Calculated

- Daily return: percentage price change from the previous day
- Moving averages (20-day and 50-day): average of the last 20 / 50 closing prices
- Volatility: standard deviation of daily returns
- Cumulative return: how much Rs 1 grew over time
- Correlation: how closely two stocks move together

## Key Findings

- TCS was the most volatile stock

## Run Locally

## Run Locally

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```