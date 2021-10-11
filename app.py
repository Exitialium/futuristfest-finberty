import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
#from algorithms.deltaNeutral import EuropeanCall
from algorithms.TrendFollowing import prep_trend
from algorithms.meanReversion import meanReversion
from algorithms import FetchData as FD

import pandas as pd

df = px.data.stocks()

app = dash.Dash(__name__)

algorithmDict = {
  "Trend-following Strategies": "tfs",
  "Mean Reversion": "mr"}
#   ,
#   "Index Fund Rebalancing": "ifr",
#   "Mathematical Model-based Strategies": "mms"
# }

#dataFetcher = DataFetcher()
app.layout = html.Div([
    dcc.Dropdown(
        id="ticker",
        options=[{"label": x, "value": x} 
                 for x in df.columns[1:]],
        value=df.columns[1],
        clearable=False,
    ),
    dcc.Dropdown(
        id="algorithm",
        options=[{"label": x, "value": algorithmDict[x]} 
                 for x in algorithmDict],
        value="none",
        clearable=False,
    ),
    dcc.Graph(id="time-series-chart"),

    dcc.Store(id='intermediate-value'),#dataFetcher.df),
    dcc.Interval(
            id='interval-component',
            interval= 5*1000, # in milliseconds
            n_intervals=0
        )
])

@app.callback(Output('intermediate-value', 'data'),
              Input('interval-component', 'n_intervals'),
              State('intermediate-value', 'data'))
def update_dataframe(n, df):
    #print("Updated:",n)
    df = df or FD.init().to_json()
    df = pd.read_json(df)
    ddf, isGood = FD.update_data(n, df)
    if isGood:
      df = ddf
    return df.to_json()


@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"),
    Input("algorithm", "value"),
    State('intermediate-value', 'data'))
def display_time_series(ticker, algorithm, df):
    ##Todo: Different algorithms triggers different methods
    df = df or FD.init().to_json()
    df = pd.read_json(df)
    if algorithm == "mr":
      return meanReversion(df, ticker)
    elif algorithm == "tfs":
      trend_days = [50, 200]
      return prep_trend(df, ticker, trend_days)
        
    fig = px.line(df, x='date', y=ticker)
    return fig


app.run_server(debug=True)