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
             "sarimax": {
                "isPlot": isPlot,
            },
            "narx": {
                "isPlot": isPlot,
            }
    }
