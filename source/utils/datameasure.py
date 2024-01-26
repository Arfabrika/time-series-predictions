from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error

class DataMeasure:
    def __init__(self, consoleFlag = True, roundFlag = True) -> None:
        self.consoleFlag = consoleFlag
        self.roundFlag = roundFlag

    def measurePredictions(self, y, y_pred):
        metrics = {}

        MAE = mean_absolute_error(y, y_pred)
        metrics['MAE'] = MAE

        MAPE = mean_absolute_percentage_error(y, y_pred)
        metrics['MAPE'] = MAPE

        MSE = mean_squared_error(y, y_pred)
        metrics['MSE'] = MSE

        R2 = r2_score(y, y_pred)
        metrics['R2'] = R2

        if self.consoleFlag:
            print(metrics)

        if self.roundFlag:
            for key in metrics.keys():
                metrics[key] = round(metrics[key], 3)
        return metrics