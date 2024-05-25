export const algoNames = [
    'snaive', 'AR', 'linearRegression', 'arima',
    'sarimax', 'narx'
]

export const algoNamesRus = [
    'Наивное прогнозирование', 'Авторегрессия', 'Полиномиальная регрессия',
    'ARIMA', 'SARIMAX', 'NARX'
]

export const algoEditNames = 'movingAverage'

export const algoParamsList = [
    ['period'],
    ['step'],
    ['degree'],
    ['p', 'd', 'q'],
    ['p', 'd', 'q','ps', 'ds', 'qs', 's'],
    ['lcnt', 'poldeg', 'neirocnt', 'epochcnt']
]

export const algoParamsRus = {
    'period': 'Период',
    'step': 'Шаг',
    'degree': 'Степень',
    'p': 'Параметр P',
    'd': 'Параметр D',
    'q': 'Параметр Q',
    'ps': 'Параметр Ps',
    'ds': 'Параметр Ds',
    'qs': 'Параметр Qs',
    's': 'Параметр s',
    'lcnt': 'Количество слоев в нейронной сети',
    'poldeg': 'Степень',
    'neirocnt': 'Количество нейронов в слое',
    'epochcnt': 'Количество обучающих эпох'
}