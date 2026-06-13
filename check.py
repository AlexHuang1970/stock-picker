import yfinance as yf
symbols = ["2330.TW","2317.TW","2454.TW","2308.TW","2303.TW","2412.TW","2301.TW","2327.TW","2353.TW","2382.TW"]
for sym in symbols:
    t = yf.Ticker(sym)
    info = t.info
    pe = info.get('trailingPE')
    dy = info.get('dividendYield')
    beta = info.get('beta')
    print(f"{sym}: PE={pe}, DY={dy}, beta={beta}")