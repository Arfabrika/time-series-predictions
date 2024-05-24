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

def bytes2csv(bytes):
    """Content-Type: text/csv\\r\n\\r\n,"""
    data_str = str(bytes)
   
    data_str = data_str.replace('\\t', ',').replace('\\n', '\n').replace('\\r', '')
    ind = data_str.find("Content-Type: text/csv\n\n,")
    if ind != -1:
        data_str = data_str[ind + len("Content-Type: text/csv\n\n,"):]
    ind = data_str.find("\n\n")
    if ind != -1:
        csv = data_str[:ind]
    else:
        csv = data_str
    return csv