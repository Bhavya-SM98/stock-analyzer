import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Stock Market Analyzer", layout="wide")
st.title("Stock Market Analyzer")
st.caption("For learning only, not financial advice.")

STOCKS = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "ITC": "ITC.NS",
}


@st.cache_data(ttl=3600)
def load_stock(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    if df.empty:
        return df
    df.columns = df.columns.get_level_values(0)
    df["Daily Return"] = df["Close"].pct_change()
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["Cumulative Return"] = (1 + df["Daily Return"]).cumprod()
    return df


@st.cache_data(ttl=3600)
def load_prices(tickers, start, end):
    prices = yf.download(list(tickers), start=start, end=end, auto_adjust=True)["Close"]
    return prices.dropna()


# sidebar
st.sidebar.header("Settings")
page = st.sidebar.radio("Page", ["Single stock", "Compare stocks"])
start = st.sidebar.date_input("Start date", datetime.date(2020, 1, 1))
end = st.sidebar.date_input("End date", datetime.date.today())

if start >= end:
    st.error("Start date must be before end date.")
    st.stop()

if page == "Single stock":
    name = st.sidebar.selectbox("Stock", list(STOCKS.keys()))
    df = load_stock(STOCKS[name], start, end)

    if df.empty:
        st.error("No data found for this date range.")
        st.stop()

    # metric cards
    total_return = (df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current price (Rs)", f"{df['Close'].iloc[-1]:.2f}")
    c2.metric("Total return", f"{total_return:.1f}%")
    c3.metric("Avg daily return", f"{df['Daily Return'].mean() * 100:.3f}%")
    c4.metric("Volatility (daily)", f"{df['Daily Return'].std() * 100:.2f}%")

    # charts
    st.plotly_chart(
        px.line(df, x=df.index, y=["Close", "MA20", "MA50"], title=f"{name} Price with Moving Averages"),
        use_container_width=True,
    )

    candle = go.Figure(data=[go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"]
    )])
    candle.update_layout(title=f"{name} Candlestick", xaxis_rangeslider_visible=False)
    st.plotly_chart(candle, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.plotly_chart(px.bar(df, x=df.index, y="Volume", title="Trading Volume"), use_container_width=True)
    with right:
        st.plotly_chart(
            px.histogram(df.dropna(), x="Daily Return", nbins=50, title="Distribution of Daily Returns"),
            use_container_width=True,
        )

else:
    names = st.sidebar.multiselect(
        "Stocks (pick 2 or more)", list(STOCKS.keys()), default=["Reliance", "TCS", "Infosys", "HDFC Bank"]
    )
    if len(names) < 2:
        st.warning("Pick at least 2 stocks.")
        st.stop()

    tickers = tuple(STOCKS[n] for n in names)
    prices = load_prices(tickers, start, end)
    if prices.empty:
        st.error("No data found for this date range.")
        st.stop()

    returns = prices.pct_change().dropna()

    growth = prices / prices.iloc[0]
    st.plotly_chart(px.line(growth, title="Growth of Rs 1 in Each Stock"), use_container_width=True)

    left, right = st.columns(2)
    with left:
        corr = returns.corr()
        st.plotly_chart(
            px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", title="Correlation of Daily Returns"),
            use_container_width=True,
        )
    with right:
        summary = pd.DataFrame({
            "Avg Daily Return %": returns.mean() * 100,
            "Volatility %": returns.std() * 100,
        })
        summary["Stock"] = summary.index
        st.plotly_chart(
            px.scatter(summary, x="Volatility %", y="Avg Daily Return %", text="Stock", title="Risk vs Return"),
            use_container_width=True,
        )

    st.subheader("Summary")
    st.dataframe(summary[["Avg Daily Return %", "Volatility %"]].round(3))