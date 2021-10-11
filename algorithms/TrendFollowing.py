import numpy as np

import plotly.express as px
import plotly.graph_objects as go


def prep_trend(df,  ticker, trend_days=[50, 200]):
    new_df = df.copy(deep=False)
    for days in trend_days:
        weeks =  days
        ret = []
        sum = 0
        for idx, val in enumerate(df[ticker]):
            sum += val
            if idx >= weeks:
                sum -= df[ticker][idx-weeks]
            ret.append(sum/min(idx+1, weeks))
        new_df[str(days)+" days Avg"] = ret
    line1 = new_df[str(trend_days[0])+" days Avg"]
    line2 = new_df[str(trend_days[1])+" days Avg"]

    death = []
    golden = []
    for idx in range(len(df[ticker])-1):
        if line1[idx] > line2[idx] and line1[idx+1] < line2[idx+1]:
            death.append([df['date'][idx+1], df[ticker][idx+1]])
        if line1[idx] < line2[idx] and line1[idx+1] > line2[idx+1]:
            golden.append([df['date'][idx+1], df[ticker][idx+1]])

    death = np.transpose(np.array(death))
    golden = np.transpose(np.array(golden))


    cols = [ticker] + [str(days)+" days Avg" for days in trend_days]

    fig = px.line(new_df, x='date', y=cols)

    if not len(death):
        death = np.array([[],[]])
    if not len(golden):
        golden = np.array([[],[]])
    fig.add_traces([go.Scatter(x=death[0], y=death[1], mode = 'markers',
              marker=dict(line=dict(color='black', width = 2),
                          symbol = 'diamond',
                          size = 14,
                          color = 'rgba(255, 0, 255, 0.6)'),
             name = 'Death Cross')])

    fig.add_traces([go.Scatter(x=golden[0], y=golden[1], mode = 'markers',
              marker=dict(line=dict(color='black', width = 2),
                          symbol = 'diamond',
                          size = 14,
                          color = 'rgba(255, 255, 0, 0.6)'),
             name = 'Golden Cross')])



    return fig
