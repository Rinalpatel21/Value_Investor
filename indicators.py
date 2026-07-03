from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator
from ta.trend import MACD



def add_indicators(df):



    atr = AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )

    df["ATR"] = atr.average_true_range()

    rsi = RSIIndicator(
        close=df["Close"],
        window=14
    )


    df["RSI"] = rsi.rsi()

    macd = MACD(
        close=df["Close"]
    )

    df["MACD"] = macd.macd()

    df["SMA50"] = df["Close"].rolling(50).mean()

    df["EMA50"] = df["Close"].ewm(span=50).mean()

    df["VOL_AVG"] = df["Volume"].rolling(20).mean()

    df["VOL_RATIO"] = df["Volume"] / df["VOL_AVG"]

    df = df.dropna()

    return df