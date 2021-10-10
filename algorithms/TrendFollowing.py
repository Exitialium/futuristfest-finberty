import numpy as np

def prep_trend(df,  ticker, trend_days=[50, 200]):
    new_df = df.copy(deep=False)
    for days in trend_days:
        ret = []
        sum = 0
        for idx, val in enumerate(df[ticker]):
            sum += val
            if idx >= days:
                sum -= df[ticker][idx-days]
            ret.append(sum/min(idx+1,days))
        new_df[ticker+'_'+str(days)] = ret
    return new_df
