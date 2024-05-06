import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.api import AutoReg
from itertools import product
import statsmodels.api as sm
import scipy.stats as scs
from tqdm import tqdm
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
        self.PLOTS_ON = config_data["plot_out"]

        self.dataMeasure = DataMeasure(config_data["measure_out"])
        columnNames = config_data["column_names"]
        self.outtbl = OutDataTable(columnNames, 'algorithms.xlsx', 'MSE')
        warnings.filterwarnings("ignore")


    def changeAxisNames(self, newx, newy):
        self.namex = newx
        self.namey = newy


    def snaive(self, y, params = [2], name = 'Naive', window_params = {}):
        period = params[0]
        if not window_params:
            window_params["start_pos"] = self.learn_size - period + 1
            window_params["stop_pos"] = self.learn_size
        y_pred = y[y.columns[1]][:self.learn_size]
        used_interval = y_pred[window_params["start_pos"]:window_params["stop_pos"]]

        for i in range(self.learn_size, len(y)):
            y_pred = pd.concat([y_pred, 
                       pd.Series(used_interval.iloc[(i % len(used_interval)) - period + 1])])

        y_pred = y_pred.fillna(0)
        metrics = self.dataMeasure.measurePredictions(y[y.columns[1]][self.learn_size:], y_pred[self.learn_size:len(y)])
        out_data = [name, period]
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'period', 'MAE', 'MAPE', 'MSE', 'R2'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if self.PLOTS_ON:
            plot = makePlot(y['Date'], y[y.columns[1]], 
                     y_pred[window_params["start_pos"]:], self.learn_size - 1,
                     name=name, xname=self.namex, yname=self.namey,
                     start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1)

        return {
            "pred": y_pred.to_list(),
            "metrics": metrics,
            "plot": None if not self.PLOTS_ON else plot
        }


    def AR(self, y, params, name = 'Autoregressive', window_params = {}):
        p = params[0]
        if not window_params:
            window_params["start_pos"] = 0
            window_params["stop_pos"] = self.learn_size
        model = AutoReg(y[y.columns[1]][window_params["start_pos"]:window_params["stop_pos"]], lags=p)
        y_pred = model.fit().predict(start=y.index[0], end = y.index[-1], dynamic=False).fillna(0)

        metrics = self.dataMeasure.measurePredictions(y[y.columns[1]][self.learn_size:], y_pred[self.learn_size:len(y)])
        out_data = [name, p]
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'ar_p', 'MAE', 'MAPE', 'MSE', 'R2'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if self.PLOTS_ON:
            plot = makePlot(y['Date'], y[y.columns[1]], 
                     y_pred[window_params["start_pos"]:], self.learn_size - 1,
                     name=name, xname=self.namex, yname=self.namey,
                     start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1)

        return {
            "pred": y_pred.to_list(),
            "metrics": metrics,
            "plot": None if not self.PLOTS_ON else plot
        }


    def linearRegression(self, y, params, name = 'Linear regression', window_params = {}):
        pow = params[0]
        if not window_params:
            window_params["start_pos"] = 0
            window_params["stop_pos"] = self.learn_size
        x = np.array([y['Date'].iloc[i].value for i in range(len(y))])
        coefs = np.polyfit(x[window_params["start_pos"]:window_params["stop_pos"]],
                           y[y.columns[1]][window_params["start_pos"]:window_params["stop_pos"]],
                           pow)
        y_pred = np.polyval(coefs, x)
        metrics = self.dataMeasure.measurePredictions(y[y.columns[1]][self.learn_size:], y_pred[self.learn_size:len(y)])
        out_data = [name, pow]
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'lrpow', 'MAE', 'MAPE', 'MSE', 'R2'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if self.PLOTS_ON:
            plot = makePlot(y['Date'], y[y.columns[1]], 
                     y_pred[window_params["start_pos"]:], self.learn_size - 1,
                     name=name, xname=self.namex, yname=self.namey,
                     start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1)
        return {
            "pred": y_pred.tolist(),
            "metrics": metrics,
            "plot": None if not self.PLOTS_ON else plot
        }


    def movingAverage(self, yn, windowSize, func, funcparams, name):
        column = yn[yn.columns[1]] if type(yn) == pd.DataFrame else yn
        y_pred = column.rolling(window=windowSize).mean()
        for i in range(windowSize - 1):
            y_pred.iloc[i] = column.iloc[i]
        newData = (pd.concat([yn['Date'], y_pred], axis=1) if type(yn) == pd.DataFrame else y_pred)
        self.outtbl.add([windowSize], self.outtbl.makeIndsArr(['movAvgWinSize']))
        func(newData, funcparams,  name + f' with moving average, window size = {windowSize}')


    def findARIMACoefs(self, y, p_lims, d_lims, q_lims, printFlag = False):
        p = range(p_lims[0], p_lims[1])
        d = range(d_lims[0], d_lims[1])
        q = range(q_lims[0], q_lims[1])

        parameters = product(p, d, q)
        parameters_list = list(parameters)
        results = []
        best_aic = float("inf")

        for param in parameters_list:
            if printFlag:
                print(f"{param} in progress")
            #try except нужен, потому что на некоторых наборах параметров модель не обучается
            try:
                mdl = self.arima(y, param)
                model = mdl.fit()
            #выводим параметры, на которых модель не обучается и переходим к следующему набору
            except Exception:
                print('wrong parameters:', param)
                continue
            aic = model.aic
            #сохраняем лучшую модель, aic, параметры
            if aic < best_aic:
                best_aic = aic
                best_param = param
            results.append([param, model.aic])
        result_table = pd.DataFrame(results)
        result_table.columns = ['parameters', 'aic']
        if printFlag:
            print(f'---\nBest is {best_param}\n---')
            print(result_table.sort_values(by = 'aic', ascending=True).head())
        return result_table


    def arima(self, y, coefs, name='ARIMA', window_params = {}):
        # 8 1 0 - alg
        # 5 0 1 - myself
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
        forecasted = pred.predicted_mean[self.learn_size - window_params["start_pos"]:len(y)]
        metrics = self.dataMeasure.measurePredictions(y_cont[self.learn_size:], forecasted)

        # data to out table
        out_data = [name]
        out_data.extend(coefs)
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'arima_p', 'arima_d', 'arima_q', 'MAE', 'MAPE', 'MSE', 'R2'])
        self.outtbl.add(out_data, inds) 
        self.outtbl.write()

        if self.PLOTS_ON:
            plot = makePlot(y_cont.index, y_cont,
                    pred.predicted_mean,
                    self.learn_size - 1, pred_ci, name=name, xname=self.namex, yname=self.namey,
                    start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1
                    )
        return {
            "pred": forecasted.tolist(),
            "metrics": metrics,
            "plot": None if not self.PLOTS_ON else plot
        }


    def findSARIMAXCoefs(self, y, p_lims, d_lims, q_lims, ps_lims, ds_lims, qs_lims, period_lims, printFlag = False):
        p = range(p_lims[0], p_lims[1])
        d = range(d_lims[0], d_lims[1])
        q = range(q_lims[0], q_lims[1])
        ps = range(ps_lims[0], ps_lims[1])
        ds = range(ds_lims[0], ds_lims[1])
        qs = range(qs_lims[0], qs_lims[1])
        period = range(period_lims[0], period_lims[1])

        parameters = product(p, d, q, ps, ds, qs, period)
        parameters_list = list(parameters)
        results = []
        best_aic = float("inf")

        for param in parameters_list:
            if printFlag:
                print(f"{param} in progress")
            #try except нужен, потому что на некоторых наборах параметров модель не обучается
            try:
                model=sm.tsa.statespace.SARIMAX(y, order=(param[0], param[1], param[2]), 
                                                 seasonal_order=(param[3], param[4], param[5], param[6])).fit(disp=-1)
            #выводим параметры, на которых модель не обучается и переходим к следующему набору
            except Exception:
                print('wrong parameters:', param)
                continue
            aic = model.aic
            #сохраняем лучшую модель, aic, параметры
            if aic < best_aic:
                best_aic = aic
                best_param = param
            results.append([param, model.aic])
        result_table = pd.DataFrame(results)
        result_table.columns = ['parameters', 'aic']
        if printFlag:
            print(f'---\nBest is {best_param}\n---')
            print(result_table.sort_values(by = 'aic', ascending=True).head())


    def sarimax(self, y, coefs, name='SARIMAX', window_params = {}):
        import warnings
        warnings.filterwarnings("ignore")
        if not window_params:
            window_params["start_pos"] = 0
            window_params["stop_pos"] = self.learn_size

        y_cont = makeDataContinuous(y, 'Date')
        mymodel = sm.tsa.statespace.SARIMAX(y_cont[window_params["start_pos"]:window_params["stop_pos"]],
                                            order =(coefs[0], coefs[1], coefs[2]),
                                            seasonal_order=(coefs[3], coefs[4], coefs[5], coefs[6]))
        modelfit = mymodel.fit(disp=-1)
        pred = modelfit.get_prediction(start = y_cont.index[window_params["start_pos"]],
                                       end = y_cont.index[-1], dynamic=False)
        pred_ci = pred.conf_int()
        forecasted = pred.predicted_mean[self.learn_size - window_params["start_pos"]:len(y)]
        metrics = self.dataMeasure.measurePredictions(y_cont[self.learn_size:], forecasted)

        # data to out table
        out_data = [name]
        out_data.extend(coefs)
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'sarimax_p', 'sarimax_d', 'sarimax_q',
                                        'sarimax_P', 'sarimax_D', 'sarimax_Q', 'period',
                                         'MAE', 'MAPE', 'MSE', 'R2'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()

        if self.PLOTS_ON:
            plot = makePlot(y_cont.index, y_cont,
                    pred.predicted_mean, self.learn_size - 1,
                    pred_ci, name=name, xname=self.namex, yname=self.namey,
                    start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1
                    )

        return {
            "pred": forecasted.tolist(),
            "metrics": metrics,
            "plot": None if not self.PLOTS_ON else plot
        }


    def narx(self, data, params, name = 'NARX', window_params = {}):
        if not window_params:
            window_params["start_pos"] = 0
            window_params["stop_pos"] = self.learn_size
        curdata = data.copy(deep=True)
        narx = NARX(curdata, params, window_params)
        y = narx.predict()
        metrics = self.dataMeasure.measurePredictions(curdata.iloc[:, [-1]].iloc[self.learn_size:],
                                                      y[self.learn_size - window_params["start_pos"]:])
        out_data = [name]
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'MAE', 'MAPE', 'MSE', 'R2'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if self.PLOTS_ON:
            plot = makePlot(data['Date'],
                     data[data.columns[-1]], 
                     y, self.learn_size - 1,
                     name=name, xname=self.namex, yname=self.namey,
                     start_ind = window_params["start_pos"], stop_ind = window_params["stop_pos"] - 1)
        return {
            # y here - list
            "pred": y,
            "metrics": metrics,
            "plot": None if not self.PLOTS_ON else plot
        }