from fastapi import FastAPI
import pandas as pd

app = FastAPI()

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def generate_signal(prices):
    ema20 = prices.ewm(span=20).mean().iloc[-1]
    ema50 = prices.ewm(span=50).mean().iloc[-1]
    rsi = calculate_rsi(prices).iloc[-1]

    if ema20 > ema50 and rsi > 65:
        return "STRONG CALL"
    elif ema20 < ema50 and rsi < 35:
        return "STRONG PUT"
    return "WAIT"

@app.get("/")
def home():
    return {"message": "Dhruv AI Backend Running"}

@app.get("/signal")
def signal():
    # Dummy data (later Zerodha API add হব)
    prices = pd.Series([22000,22100,22200,22300,22400,22500])
    sig = generate_signal(prices)
    return {"signal": sig}
