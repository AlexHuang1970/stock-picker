import yfinance as yf
sym = "2317.TW"
t = yf.Ticker(sym)
info = t.info
pe = info.get('trailingPE')
dy = info.get('dividendYield')
if dy is not None:
    dy = dy * 100
beta = info.get('beta')
hist = t.history(period="6mo")
print("PE:", pe)
print("DY:", dy)
print("beta:", beta)
if len(hist) >= 20:
    pc = (hist['Close'].iloc[-1] / hist['Close'].iloc[-20] - 1) * 100
    print("price_change_1m:", pc)
else:
    print("hist len <20")
print("Hist tail:", hist['Close'].tail())