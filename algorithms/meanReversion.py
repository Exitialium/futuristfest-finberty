import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests


def meanReversion(odf,ticker):
    r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey=EN1ZTODVRGORPNBW').json()
    df = pd.DataFrame(r['Time Series (Daily)'], dtype=float).transpose()
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
    df['date'] = pd.to_datetime(df['date'])
    df['ma_200'] = df['close'].rolling(200).mean()
    cols = ['close'] + ['ma_200']
    df['ma_20'] = df['close'].rolling(20).mean()
    df['std'] = df['close'].rolling(20).std()
    df['upper_bollinger'] = df['ma_20'] + (2 * df['std'])
    df['lower_bollinger'] = df['ma_20'] - (2 * df['std'])
    df = df[((df['date'] >= pd.to_datetime('2018-01-01')) & (df['date'] <= pd.to_datetime('2019-12-30')))]
    fig = px.line(df, x='date', y=cols)
    fig.add_trace(go.Scatter(x=df.date, y = df.upper_bollinger,
        fill=None,
        mode='lines',
        line_color='indigo',
    ))
    fig.add_trace(go.Scatter(x=df.date, y = df.lower_bollinger,
        fill='tonexty',
        mode='lines', line_color='indigo'))
    return fig


