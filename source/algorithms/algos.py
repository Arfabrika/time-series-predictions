import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA 
from itertools import product
import statsmodels.api as sm
import scipy.stats as scs
from tqdm import tqdm
import warnings

from source.utils.plots import makePlot
from source.utils.datameasure import DataMeasure
from source.utils.out_data_table import OutDataTable

from source.algorithms.narx import NARX

class Algos:
    def __init__(self, learn_size, namex, namey, plot_status = True) -> None:
        self.learn_size = learn_size
        self.namex = namex
        self.namey = namey
        self.PLOTS_ON = plot_status
        self.dataMeasure = DataMeasure(True)
        columnNames = ['name', 'lrpow', 'movAvgWinSize', 
                       'arima_p', 'arima_d', 'arima_q',
                       'sarimax_p', 'sarimax_d', 'sarimax_q',
                       'sarimax_P', 'sarimax_D', 'sarimax_Q', 'period',
                        'MAE', 'MAPE', 'MSE', 'R2']
        self.outtbl = OutDataTable(columnNames, 'algorithms.xlsx', 'MSE')
        warnings.filterwarnings("ignore")

    def changeAxisNames(self, newx, newy):
        self.namex = newx
        self.namey = newy

    def linearRegression(self, yn, pow, name = 'Linear regression'):
        x = np.array([yn['Date'].iloc[i].value for i in range(len(yn))])
        coefs = np.polyfit(x[:self.learn_size], yn[yn.columns[1]][:self.learn_size], pow)
        y_pred = np.polyval(coefs, x)
        metrics = self.dataMeasure.measurePredictions(yn[yn.columns[1]][self.learn_size:], y_pred[self.learn_size:len(yn)])
        out_data = [name, pow]
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'lrpow', 'MAE', 'MAPE', 'MSE', 'R2'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if self.PLOTS_ON:
            makePlot(yn['Date'], yn[yn.columns[1]], 
                     y_pred, self.learn_size,
                     name, xname=self.namex, yname=self.namey)

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

    # ARIMA
    def arima(self, y, coefs, name='ARIMA'):
        # 8 1 0 - alg
        # 5 0 1 - myself
        mymodel = ARIMA(y[:self.learn_size], order =(coefs[0], coefs[1], coefs[2])) 
        modelfit = mymodel.fit() 
        pred = modelfit.get_prediction(start = y.index[0], end = y.index[-1], dynamic=False)
        pred_ci = pred.conf_int()
        forecasted = pred.predicted_mean[self.learn_size:len(y)]
        actual = y[self.learn_size:] 
        metrics = self.dataMeasure.measurePredictions(actual, forecasted)

        # data to out table
        out_data = [name]
        out_data.extend(coefs)
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'arima_p', 'arima_d', 'arima_q', 'MAE', 'MAPE', 'MSE', 'R2'])
        self.outtbl.add(out_data, inds) 
        self.outtbl.write()

        if self.PLOTS_ON:
            makePlot(y.index, y,
                    pred.predicted_mean,
                    self.learn_size, name, pred_ci, xname=self.namex, yname=self.namey
                    )
        return mymodel

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

    # SARIMAX
    def sarimax(self, y, coefs, name='SARIMAX'):
        import warnings
        warnings.filterwarnings("ignore")
        # kpssTest(yn[yn.columns[0]], 'original')
        
        # #yn = yn.squeeze(axis=1).dropna()
        # yn['box'], lmbda = scs.boxcox(yn[yn.columns[0]])

        # kpssTest(yn['box'], 'box')

        mymodel = sm.tsa.statespace.SARIMAX(y[:self.learn_size], order =(coefs[0], coefs[1], coefs[2]),
                                            seasonal_order=(coefs[3], coefs[4], coefs[5], coefs[6]))
        modelfit = mymodel.fit(disp=-1)
        pred = modelfit.get_prediction(start = y.index[0], end = y.index[-1], dynamic=False)
        pred_ci = pred.conf_int()
        forecasted = pred.predicted_mean[self.learn_size:len(y)]
        actual = y[self.learn_size:] 
        metrics = self.dataMeasure.measurePredictions(actual, forecasted)

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
            makePlot(y.index, y,
                    pred.predicted_mean, self.learn_size,
                    name, pred_ci, xname=self.namex, yname=self.namey
                    )

    def narx(self, data, params, name = 'NARX'):
        curdata = data.copy(deep=True)
        narx = NARX(curdata, self.learn_size, params, name)
        y = narx.predict()
        metrics = self.dataMeasure.measurePredictions(curdata.iloc[:, [-1]].iloc[self.learn_size:len(y)],
                                                      y[self.learn_size:])
        out_data = [name]
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'MAE', 'MAPE', 'MSE', 'R2'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if self.PLOTS_ON:
            makePlot(curdata['Date'].iloc[:len(y)], curdata[curdata.columns[-1]].iloc[:len(y)], 
                     y, self.learn_size,
                     name, xname=self.namex , yname=self.namey)