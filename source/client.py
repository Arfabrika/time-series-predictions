from source.utils.dataload import loadData
import pandas as pd
from datetime import datetime

def makeData(path, param, isPL):
    data_all = loadData(path)

    if isPL:
        for i in range(len(data_all["Date"])):
            data_all.loc[i, "Date"] = pd.to_datetime(datetime.strptime(data_all["Date"].iloc[i], '%B %Y'))
    else:
         data_all["Date"] = pd.to_datetime(data_all["Date"], format='%Y/%m/%d')
    return data_all[["Date", param]]

def makeAlgoData():
    return {
        # "snaive": {
        #     "params": [3]
        # },
        # "AR": {
        #     "params": [3]
        # }
        # "linearRegression": {
        #     "params": [4]
        # }
        # "arima": {
        #     "params": [0, 4, 9]
        # }
        #  "sarimax": {
        #     "params": [0, 4, 9, 3, 0, 1, 25]
        # }
         "narx": {
            "params": [2, 2, 42, 100, 1000]
        }
    }