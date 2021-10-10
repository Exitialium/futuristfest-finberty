import numpy as np

def prep_trend(df, trend_days=[50, 200], ticker):
    new_df = df.copy(deep=False)
    for days in trend_days:
        ret = []
        sum = 0
        for idx, val in enum(df[ticker]):
            sum += val
            if idx >= days:
                sum -= df[ticker][idx-50]
            ret.append(sum/days)
        new_df[ticker+'_'+str(days)] = ret
    return new_df
