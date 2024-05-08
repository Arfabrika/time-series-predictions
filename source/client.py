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

"""
Имитация данных с фронта
{
    "algos": - информация об алгоритме
    {
        "params": [...] - массив параметров или None, если параметры считаем автоматически
        "isPlot": true/false - отображаем ли график (не реализовано)
        "fullTrain": bool - обучается ли алгоритм на всей обучающей выборке (если да, то окна не перебираются)
        "window_params": {
            start_pos: int - начало обучающего окна
            stop_pos: int - конец обучающего окна
        } - необязательный параметр, если задан, то окна не перебираются
    }
    "needAvg": bool - нужен ли усредняющий алгоритм
}
"""
def makeAlgoData():
    return {
        "needAvg": True,
        "algos": {
            # "snaive": {
            #     "params": [2],
            #     "fullTrain": True
            # },
            # "AR": {
            #     "params": [3],
            #     "fullTrain": True
            # },
            "linearRegression": {
                "params": [4],
                "fullTrain": True
            },
            # "arima": {
            #     "params": [0, 4, 9],
            #     "fullTrain": True
            # },
            #  "sarimax": {
            #     "params": [0, 4, 9, 3, 0, 1, 25],
            #     "fullTrain": True
            # },
            "narx": {
                "params": [2, 2, 42, 100, 1000],
                "fullTrain": True,
                # "window_params": {
                #     "start_pos": 2,
                #     "stop_pos": 22
                # }
            }
        }
    }