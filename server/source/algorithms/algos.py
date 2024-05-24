import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.api import AutoReg, SARIMAX
from itertools import product
import warnings

from source.utils.plots import makePlot
from source.utils.dataload import loadConfig
from source.utils.datameasure import DataMeasure
from source.utils.out_data_table import OutDataTable
from source.utils.dataedit import makeDataContinuous

from source.algorithms.narx import NARX

class Algos:
    def __init__(self, learn_size, namex, namey) -> None:
        self.learn_size = learn_size
        self.namex = namex
        self.namey = namey
        config_data = loadConfig('./config.json')

        self.dataMeasure = DataMeasure(config_data["measure_out"])
        columnNames = config_data["column_names"]
        self.outtbl = OutDataTable(columnNames, 'algorithms.xlsx', 'MSE')
        self.limits = config_data.get("limits", {})
        warnings.filterwarnings("ignore")


    def changeAxisNames(self, newx, newy):
        self.namex = newx
        self.namey = newy


    def makeParamsList(self, algo_name, maxlen):
        cur_limits = self.limits.get(algo_name, {})
        iter_list = []
        for limit in cur_limits:
            start = limit["start"]
            end = maxlen if limit['stop'] == 'len' else limit['stop']
            step = limit.get("step", 1)
            iter_list.append(range(start, end, step))
        main_list = list(product(*iter_list))
        tmp_list = list(product(*[range(0, 5), range(0, 5), range(0, 5)]))
        final_list = [x for x in main_list if x not in tmp_list]
        return final_list


    def snaive(self, y, params, **kwargs):
        period = params[0]
        window_params = kwargs.get("window_params", None)
        name = f"Seasonal naive, period {period}" + kwargs.get("name", "")
        isPlot = kwargs.get("isPlot", False)
        if not window_params:
            window_params["start_pos"] = 0
            window_params["stop_pos"] = self.learn_size
        y_pred = y[y.columns[1]][:window_params["stop_pos"]]
        used_interval = y_pred[window_params["stop_pos"] - period:window_params["stop_pos"]]

        for i in range(window_params["stop_pos"], len(y)):
            y_pred = pd.concat([y_pred, 
                       pd.Series(used_interval.iloc[(i % len(used_interval)) - period + 1])])

        y_pred = y_pred.fillna(0)
        metrics = self.dataMeasure.measurePredictions(y[y.columns[1]][self.learn_size:], y_pred[self.learn_size:len(y)])
        out_data = ["Seasonal naive", window_params["start_pos"], window_params["stop_pos"], period]
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', "learn_start_ind", "learn_stop_ind",
                                        'naive_period', 'MAE', 'MAPE', 'MSE'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if isPlot:
            plot = makePlot(y['Date'], y[y.columns[1]], 
                     y_pred[window_params["start_pos"]:], self.learn_size - 1,
                     name=name, xname=self.namex, yname=self.namey,
                     start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1)

        return {
            "pred": y_pred.to_list(),
            "metrics": metrics,
            "plot": None if not isPlot else plot
        }


    def AR(self, y, params, **kwargs):
        p = params[0]
        window_params = kwargs.get("window_params", None)
        name = f"Autoregression, parameter: {p}" + kwargs.get("name", "")
        isPlot = kwargs.get("isPlot", False)
        if not window_params:
            window_params["start_pos"] = 0
            window_params["stop_pos"] = self.learn_size
        model = AutoReg(y[y.columns[1]][window_params["start_pos"]:window_params["stop_pos"]], lags=p)
        y_pred = model.fit().predict(start=y.index[0], end = y.index[-1], dynamic=False).fillna(0)

        metrics = self.dataMeasure.measurePredictions(y[y.columns[1]][self.learn_size:], y_pred[self.learn_size:len(y)])
        out_data = ['Autoregression', window_params["start_pos"], window_params["stop_pos"], p]
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', "learn_start_ind", "learn_stop_ind",
                                        'AR_p', 'MAE', 'MAPE', 'MSE'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if isPlot:
            plot = makePlot(y['Date'], y[y.columns[1]], 
                     y_pred[window_params["start_pos"]:], self.learn_size - 1,
                     name=name, xname=self.namex, yname=self.namey,
                     start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1)

        return {
            "pred": y_pred.to_list(),
            "metrics": metrics,
            "plot": None if not isPlot else plot
        }


    def linearRegression(self, y, params, **kwargs):
        pow = params[0]
        window_params = kwargs.get("window_params", None)
        name = f"Polynomical regression, degree: {pow}" + kwargs.get("name", "")
        isPlot = kwargs.get("isPlot", False)
        if not window_params:
            window_params["start_pos"] = 0
            window_params["stop_pos"] = self.learn_size
        x = np.array([y['Date'].iloc[i].value for i in range(len(y))])
        coefs = np.polyfit(x[window_params["start_pos"]:window_params["stop_pos"]],
                           y[y.columns[1]][window_params["start_pos"]:window_params["stop_pos"]],
                           pow)
        y_pred = np.polyval(coefs, x)
        metrics = self.dataMeasure.measurePredictions(y[y.columns[1]][self.learn_size:], y_pred[self.learn_size:len(y)])
        out_data = ['Polynomical regression', window_params["start_pos"], window_params["stop_pos"], pow]
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', "learn_start_ind", "learn_stop_ind",
                                        'lr_pow', 'MAE', 'MAPE', 'MSE'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if isPlot:
            plot = makePlot(y['Date'], y[y.columns[1]], 
                     y_pred[window_params["start_pos"]:], self.learn_size - 1,
                     name=name, xname=self.namex, yname=self.namey,
                     start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1)
        return {
            "pred": y_pred.tolist(),
            "metrics": metrics,
            "plot": None if not isPlot else plot
        }


    def movingAverage(self, y, params, func, funcparams, **kwargs):
        windowSize = params[0]
        name = f' with moving average, window size = {windowSize}'
        column = y[y.columns[1]]
        y_pred = column.rolling(window=windowSize).mean()
        for i in range(windowSize - 1):
            y_pred.iloc[i] = column.iloc[i]
        newData = pd.concat([y['Date'], y_pred], axis=1)
        self.outtbl.add([windowSize], self.outtbl.makeIndsArr(['movAvg_WinSize']))
        return func(newData, funcparams, **kwargs, name=name)


    def arima(self, y, coefs, **kwargs):
        window_params = kwargs.get("window_params", None)
        name = f"ARIMA, parameters: {coefs}" + kwargs.get("name", "")
        isPlot = kwargs.get("isPlot", False)

        if not window_params:
            window_params["start_pos"] = 0
            window_params["stop_pos"] = self.learn_size

        y_cont = makeDataContinuous(y, 'Date')
        mymodel = ARIMA(y_cont[window_params["start_pos"]:window_params["stop_pos"]],
                        order =(coefs[0], coefs[1], coefs[2])) 
        modelfit = mymodel.fit() 
        pred = modelfit.get_prediction(start = y_cont.index[window_params["start_pos"]],
                                       end = y_cont.index[-1], dynamic=False)
        pred_ci = pred.conf_int()
        forecasted = pred.predicted_mean
        metrics = self.dataMeasure.measurePredictions(y_cont[self.learn_size:],
                                                      forecasted[self.learn_size - window_params["start_pos"]:])

        # data to out table
        out_data = ["ARIMA", window_params["start_pos"], window_params["stop_pos"]]
        out_data.extend(coefs)
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', "learn_start_ind", "learn_stop_ind",
                                        'arima_p', 'arima_d', 'arima_q', 'MAE', 'MAPE', 'MSE'])
        self.outtbl.add(out_data, inds) 
        self.outtbl.write()

        if isPlot:
            plot = makePlot(y_cont.index, y_cont,
                    pred.predicted_mean,
                    self.learn_size - 1, pred_ci, name=name, xname=self.namex, yname=self.namey,
                    start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1
                    )
        return {
            "pred": forecasted.tolist(),
            "metrics": metrics,
            "plot": None if not isPlot else plot
        }


    def sarimax(self, y, coefs, **kwargs):
        import warnings
        warnings.filterwarnings("ignore")

        window_params = kwargs.get("window_params", None)
        name = f"SARIMAX, parameters: {coefs}" + kwargs.get("name", "")
        isPlot = kwargs.get("isPlot", False)

        if not window_params:
            window_params["start_pos"] = 0
            window_params["stop_pos"] = self.learn_size

        y_cont = makeDataContinuous(y, 'Date')
        mymodel = SARIMAX(y_cont[window_params["start_pos"]:window_params["stop_pos"]],
                                            order =(coefs[0], coefs[1], coefs[2]),
                                            seasonal_order=(coefs[3], coefs[4], coefs[5], coefs[6]))
        modelfit = mymodel.fit(disp=-1)
        pred = modelfit.get_prediction(start = y_cont.index[window_params["start_pos"]],
                                       end = y_cont.index[-1], dynamic=False)
        pred_ci = pred.conf_int()
        forecasted = pred.predicted_mean
        metrics = self.dataMeasure.measurePredictions(y_cont[self.learn_size:],
                                                      forecasted[self.learn_size - window_params["start_pos"]:])

        # data to out table
        out_data = ['SARIMAX', window_params["start_pos"], window_params["stop_pos"]]
        out_data.extend(coefs)
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', "learn_start_ind", "learn_stop_ind",
                                        'sarimax_p', 'sarimax_d', 'sarimax_q',
                                        'sarimax_P', 'sarimax_D', 'sarimax_Q', 'sarimax_period',
                                        'MAE', 'MAPE', 'MSE'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()

        if isPlot:
            plot = makePlot(y_cont.index, y_cont,
                    pred.predicted_mean, self.learn_size - 1,
                    pred_ci, name=name, xname=self.namex, yname=self.namey,
                    start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1
                    )

        return {
            "pred": forecasted.tolist(),
            "metrics": metrics,
            "plot": None if not isPlot else plot
        }


    def narx(self, data, params, **kwargs):
        window_params = kwargs.get("window_params", None)
        name = f"NARX, parameters: {params}" + kwargs.get("name", "")
        isPlot = kwargs.get("isPlot", False)

        if not window_params:
            window_params["start_pos"] = 0
            window_params["stop_pos"] = self.learn_size
        curdata = data.copy(deep=True)
        narx = NARX(curdata, params, window_params)
        y = narx.predict()
        metrics = self.dataMeasure.measurePredictions(curdata.iloc[:, [-1]].iloc[self.learn_size:],
                                                      y[self.learn_size - window_params["start_pos"]:])
        out_data = [name, window_params["start_pos"], window_params["stop_pos"]]
        out_data.extend(params)
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', "learn_start_ind", "learn_stop_ind",
                                        "NARX_lay_cnt", "NARX_degree", "NARX_neiron_cnt", "NARX_epoch_cnt", "NARX_data_shift",
                                        'MAE', 'MAPE', 'MSE'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if isPlot:
            plot = makePlot(data['Date'],
                     data[data.columns[-1]], 
                     y, self.learn_size - 1,
                     name=name, xname=self.namex, yname=self.namey,
                     start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1)
        return {
            # y here - list
            "pred": y,
            "metrics": metrics,
            "plot": None if not isPlot else plot
        }


    def averange(self, data, algdata, **kwargs):
        isPlot = kwargs.get("isPlot", True)

        df = pd.DataFrame(algdata)
        y = df.mean()
        metrics = self.dataMeasure.measurePredictions(data.iloc[:, [-1]].iloc[self.learn_size:], y)
        out_data = ['Averange']
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'MAE', 'MAPE', 'MSE'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if isPlot:
            plot = makePlot(data['Date'],
                     data[data.columns[-1]], 
                     y, self.learn_size,
                     name="Averange from used algorithms", xname=self.namex, yname=self.namey,
                     start_ind = 0, stop_ind = self.learn_size, only_predict=True)
        return {
            "pred": y.to_list(),
            "metrics": metrics,
            "plot": None if not isPlot else plot
        }