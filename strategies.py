import requests

def fetch_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=15"
    response = requests.get(url).json()
    data = [{'close': float(item[4])} for item in response]
    return data

def get_signal(price_data):
    closes = [p['close'] for p in price_data]
    if len(closes) < 14:
        return "HOLD"

    ma5 = sum(closes[-5:])/5
    ma10 = sum(closes[-10:])/10

    gains = [closes[i]-closes[i-1] for i in range(1,len(closes)) if closes[i]-closes[i-1]>0]
    losses = [- (closes[i]-closes[i-1]) for i in range(1,len(closes)) if closes[i]-closes[i-1]<0]

    avg_gain = sum(gains[-14:])/14 if gains else 0.0001
    avg_loss = sum(losses[-14:])/14 if losses else 0.0001

    rsi = 100 - (100/(1 + avg_gain/avg_loss))

    if rsi < 30 and ma5 > ma10:
        return "BUY"
    elif rsi > 70 and ma5 < ma10:
        return "SELL"
    else:
        return "HOLD"
