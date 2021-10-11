import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests


def init(all_tickers=['GOOG','AAPL','AMZN','FB','NFLX','MSFT']):
    #print("kk")
    goog, isGood = fetch('GOOG')
    if isGood:
        df = pd.DataFrame(goog['date'])
        df['kk'] = pd.DataFrame([0]*753)
    else:
        df = pd.DataFrame([0]*753)
        df['date'] = pd.DataFrame([0]*753)
    for ticker in all_tickers:
        df[ticker] = pd.DataFrame([0]*753)
    df.reset_index(level=0, inplace=True)
    return df
    #fetch_n = 0


def fetch(ticker):
    #print(ticker)
    r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey=EN1ZTODVRGORPNBW').json()
    try: 
        df = pd.DataFrame(r['Time Series (Daily)'], dtype=float).transpose()
    except:
        return None, False
    df = df.reindex(index=df.index[::-1])
    df.reset_index(level=0, inplace=True)
    df = df.rename({
        'index': 'date',
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. adjusted close': 'adjusted_close',
        '6. volume': 'volume',
        '7. dividend amount': 'dividend_amount',
        '8. split coefficient': 'split_coefficient'
    },axis=1)
    df = df[((df['date'] >= '2017-01-01') & (df['date'] <= '2019-12-30'))]
    return df, True

# def fetch_data(all_tickers=['GOOG','AAPL','AMZN','FB','NFLX','MSFT']):
#     bb = pd.DataFrame([0]*753)
#     try:
#         ret = pd.DataFrame(fetch('GOOG')['date'])
#     except:
#         ret = bb
#     for ticker in all_tickers:
#         fetched, isGood = fetch(ticker)
#         if(isGood != "Failed"):
#             ret[ticker] = fetched['close'] #is this the same as 
#         else:
#             print("Yee:", ticker)
#             ret[ticker] = bb # this?
#     return ret

def update_data(n, df):
    updated_col = df.columns[(n % (len(df.columns)-3))+3]
    updated_col = exists_front(df) or updated_col
    fetched, isGood =fetch(updated_col)
    if isGood:
        df[updated_col] = list(fetched['close'])
        df['date'] = list(fetched['date'])
        print("Fetch Succeeded:", updated_col)
        return df, True
    else:
        print("Fetch Failed:", updated_col)
        return None, False


def exists_front(df):
    for i in range(3,len(df.columns)):
        col = df.columns[i]
        if df[col][0] == 0:
            return col
    return None



