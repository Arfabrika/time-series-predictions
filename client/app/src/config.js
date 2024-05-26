export const algoNames = [
    'snaive', 'AR', 'linearRegression', 'arima',
    'sarimax', 'narx', 'movingAverange'
]

export const algoNamesRus = [
    'Наивное прогнозирование', 'Авторегрессия', 'Полиномиальная регрессия',
    'ARIMA', 'SARIMAX', 'NARX', 'Среднее  скользящее арифметическое'
]

export const algoParamsList = [
    ['period'],
    ['step'],
    ['degree'],
    ['p', 'd', 'q'],
    ['p', 'd', 'q','ps', 'ds', 'qs', 's'],
    ['lcnt', 'poldeg', 'neirocnt', 'epochcnt'],
    ['size']
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
    'epochcnt': 'Количество обучающих эпох',
    'size': 'Размер окна',
    'learn_size': 'Размер обучающей выборки (в процентах)'
}