export const algoNames = [
    'snaive', 'AR', 'linearRegression', 'arima',
    'sarimax', 'narx'
]

export const algoEditNames = 'movingAverage'

export const algoParams = {
    'snaive': ['period'],
    'AR': ['step'],
    'linearRegression': ['degree'],
    'arima': ['p', 'd', 'q'],
    'sarimax': ['p', 'd', 'q','ps', 'ds', 'qs', 's'],
    'narx': ['lcnt', 'poldeg', 'neirocnt', 'epochcnt']
}