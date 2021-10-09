import plotly.express as px
import pandas as pd
df = px.data.stocks()
fig = px.line(df, x='date', y="GOOG")
fig.show()