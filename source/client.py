from source.utils.dataload import loadData
import pandas as pd

def makeData(path, param, isMetro = True):
    data_all = loadData(path)

    if isMetro:
         data_all["Date"] = pd.to_datetime(data_all["Date"], format='%Y-%m-%d')
    else:
         raise NotImplementedError()
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
        #"needAvg": True,
        "algos": {
            # "snaive": {
            #     "params": [2],
            #     "window_params": {
            #         "start_pos": 363,
            #         "stop_pos": 726
            #     }
            #     #"fullTrain": True
            # },
            # "AR": {
            #     "params": [3],
            #     # "fullTrain": True
            # },
            # "linearRegression": {
            #     "params": [2],
            #     "window_params": {
            #         "start_pos": 0,
            #         "stop_pos": 517
            #     }
            # },
            # "arima": {
            #     "params": [0, 4, 9],
            #     # "fullTrain": True
            #     "window_params": {
            #         "start_pos": 0,
            #         "stop_pos": 749
            #     }
            # },
            #  "sarimax": {
            #     "params": [1, 1, 1, 1, 1, 1, 10],
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