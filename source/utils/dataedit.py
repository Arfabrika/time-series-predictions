import pandas as pd
from datetime import timedelta

def makeDataContinuous(data, indexColumn):
    freq = abs(data[indexColumn].iloc[1] - data[indexColumn].iloc[0])
    if freq in [timedelta(days=31), timedelta(days=30), timedelta(days=29), timedelta(days=28)]:
        freq = 'MS'
    idx = pd.date_range(data[indexColumn].iloc[0],
                        data[indexColumn].iloc[-1],
                        freq=freq)
   
    yn = makeDateItemData(data)
    yn.index = pd.DatetimeIndex(yn.index)
    yn = yn.reindex(idx, fill_value=0)
    return yn


def makeDateItemData(y):
    yn = y.copy(True)
    yn.set_index(keys='Date', drop=True, inplace=True)
    yn = yn.squeeze(axis=1).dropna()
    return yn


def fillAlgoParams(isStat, isPlot):
    if isStat:
        return {
            "snaive": {
                "isPlot": isPlot,
            },
            "AR": {
                "isPlot": isPlot,
            },
            "linearRegression": {
               "isPlot": isPlot,
            },
            "arima": {
                "isPlot": isPlot,
            },
             "sarimax": {
                "isPlot": isPlot,
            }
        }
    return {
            "arima": {
                "isPlot": isPlot,
            },
            #  "sarimax": {
            #     "isPlot": isPlot,
            # },
            # "narx": {
            #     "isPlot": isPlot,
            # }
    }