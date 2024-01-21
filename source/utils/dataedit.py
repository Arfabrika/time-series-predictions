import pandas as pd

def makeDataContinuous(data, indexColumn, freq):
    idx = pd.date_range(data[indexColumn].iloc[0], data[indexColumn].iloc[-1], freq=freq)
    yn = makeDateItemData(data)
    yn.index = pd.DatetimeIndex(yn.index)
    yn = yn.reindex(idx, fill_value=0)
    return yn


def makeDateItemData(y):
    yn = y.copy(True)
    yn.set_index(keys='Date', drop=True, inplace=True)
    yn = yn.squeeze(axis=1).dropna()
    return yn