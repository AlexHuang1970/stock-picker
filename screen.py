import yfinance as yf

# List of Taiwanese stocks (TWSE) symbols with .TW suffix
STOCKS = [
    "2330.TW",  # TSMC
    "2317.TW",  # Hon Hai
    "2454.TW",  # MediaTek
    "2308.TW",  # Delta Electronics
    "2303.TW",  # United Microelectronics
    "2412.TW",  # Chunghwa Telecom
    "2301.TW",  # Liteon
    "2327.TW",  # Yageo
    "2353.TW",  # Acer
    "2382.TW",  # Quanta Computer
    "2395.TW",  # Ruentex
    "2302.TW",  # Cathay Financial
    "2881.TW",  # Fubon Financial
    "2882.TW",  # Cathay Financial Holding
    "2886.TW",  # Mega Financial
    "2891.TW",  # SinoPac Financial
    "2892.TW",  # First Financial
    "2880.TW",  # China Development Financial
    "2884.TW",  # E.SUN Financial
]

def fetch_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="6mo")
        if hist.empty:
            return None
        price = info.get('regularMarketPrice', None)
        pe = info.get('trailingPE', None)
        dividend_yield = info.get('dividendYield', None)
        # dividendYield from yfinance is already a percentage (e.g., 2.75 for 2.75%)
        beta = info.get('beta', None)
        if len(hist) >= 20:
            price_change_1m = (hist['Close'].iloc[-1] / hist['Close'].iloc[-20] - 1) * 100
        else:
            price_change_1m = None
        return {
            'symbol': symbol.replace('.TW', ''),
            'name': info.get('shortName', symbol),
            'price': price,
            'pe': pe,
            'dividend_yield': dividend_yield,
            'beta': beta,
            'price_change_1m': price_change_1m,
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def screen_stocks(risk_preference, investment_goal):
    results = []
    for sym in STOCKS:
        data = fetch_data(sym)
        if data is None:
            continue
        pe = data['pe']
        dy = data['dividend_yield']
        beta = data['beta']
        pc1m = data['price_change_1m']
        risk_match = False
        goal_match = False
        # Risk filters
        if risk_preference == 'low':
            if beta is not None and beta < 1.0 and (dy is not None and dy >= 2.0):
                risk_match = True
        elif risk_preference == 'medium':
            if beta is not None and 1.0 <= beta <= 1.5 and (pe is not None and pe < 25):
                risk_match = True
        elif risk_preference == 'high':
            if beta is not None and beta > 1.5:
                risk_match = True
            elif pe is not None and pe > 30:
                risk_match = True
        # Goal filters (adjusted)
        if investment_goal == 'growth':
            if pe is not None and pe < 50 and (pc1m is not None and pc1m > 0):
                goal_match = True
        elif investment_goal == 'dividend':
            if dy is not None and dy >= 2.0:
                goal_match = True
        elif investment_goal == 'value':
            if pe is not None and pe < 25 and (dy is not None and dy >= 1.5):
                goal_match = True
        if risk_match and goal_match:
            results.append({
                'symbol': data['symbol'],
                'name': data['name'],
                'price': round(data['price'], 2) if data['price'] else None,
                'pe': round(data['pe'], 2) if data['pe'] else None,
                'dividend_yield': round(data['dividend_yield'], 2) if data['dividend_yield'] else None,
                'beta': round(data['beta'], 2) if data['beta'] else None,
                'price_change_1m': round(data['price_change_1m'], 2) if data['price_change_1m'] else None,
            })
    return results

if __name__ == "__main__":
    # quick test
    res = screen_stocks('medium', 'growth')
    print(f"Found {len(res)} stocks")
    for r in res[:5]:
        print(r)