import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests


def meanReversion(df, ticker):
    
    df['date'] = pd.to_datetime(df['date'])
    df['ma_200'] = df[ticker].rolling(200).mean()
    cols = [ticker] + ['ma_200']
    df['ma_20'] = df[ticker].rolling(20).mean()
    df['std'] = df[ticker].rolling(20).std()
    df['upper_bollinger'] = df['ma_20'] + (2 * df['std'])
    df['lower_bollinger'] = df['ma_20'] - (2 * df['std'])
    df = df[((df['date'] >= pd.to_datetime('2018-01-01')) & (df['date'] <= pd.to_datetime('2019-12-30')))]
    #df = df[((df['date'] >= '2018-01-01') & (df['date'] <= '2019-12-30'))]
    
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


