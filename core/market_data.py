import yfinance as yf

def download_btc_data():

    df = yf.download(
        "BTC-USD",
        period="60d",
        interval="30m",
        )

    # Flatten MultiIndex columns
    if hasattr(df.columns, "levels"):  
        df.columns = df.columns.get_level_values(0)

    return df


