import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

df = px.data.stocks()

app = dash.Dash(__name__)

algorithmDict = {
  "Trend-following Strategies": "tfs",
  "Arbitrage Opportunities": "ao",
  "Index Fund Rebalancing": "ifr",
  "Mathematical Model-based Strategies": "mms"
}

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
])

@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"),
    Input("algorithm", "value"))
def display_time_series(ticker,algorithm):
    fig = px.line(df, x='date', y=ticker)
    return fig


app.run_server(debug=True)