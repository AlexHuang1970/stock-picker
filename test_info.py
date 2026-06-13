import yfinance as yf
import pandas as pd

sym = "2330.TW"
t = yf.Ticker(sym)
info = t.info
print("Info keys:", list(info.keys())[:10])
print("shortName:", info.get('shortName'))
print("trailingPE:", info.get('trailingPE'))
print("dividendYield:", info.get('dividendYield'))
print("beta:", info.get('beta'))
hist = t.history(period="6mo")
print("Hist length:", len(hist))
if not hist.empty:
    print("Last close:", hist['Close'].iloc[-1])
    print("Close 20 days ago:", hist['Close'].iloc[-20] if len(hist) >=20 else None)