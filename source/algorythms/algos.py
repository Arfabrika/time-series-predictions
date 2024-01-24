import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA 
import itertools
from source.utils.plots import makePlot
from source.utils.datameasure import DataMeasure
import statsmodels.api as sm
import scipy.stats as scs
from tqdm import tqdm

class Algos:
    def __init__(self, learn_size, namex, namey, plot_status = True) -> None:
        self.learn_size = learn_size
        self.namex = namex
        self.namey = namey
        self.PLOTS_ON = plot_status
        self.dataMeasure = DataMeasure()

    def changeAxisNames(self, newx, newy):
        self.namex = newx
        self.namey = newy

    def linearRegression(self, yn, pow, name = 'Linear regression'):
        x = np.array([yn['Date'].iloc[i].value for i in range(len(yn))])
        coefs = np.polyfit(x[:self.learn_size], yn[yn.columns[1]][:self.learn_size], pow)
        y_pred = np.polyval(coefs, x)
        self.dataMeasure.measurePredictions(yn[yn.columns[1]][self.learn_size:], y_pred[self.learn_size:len(yn)])
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
        func(newData, funcparams,  name + f' with moving average, window size = {windowSize}')

    # ARIMA
    def arima(self, y, coefs, name='ARIMA'):
        import warnings
        warnings.filterwarnings("ignore")
        # подбор коэффициентов
        # import warnings
        # warnings.filterwarnings("ignore")
        # p = range(0,15)
        # d = q = range(0,7)
        # pdq = list(itertools.product(p, d, q))
        # best_pdq = (0,0,0)
        # best_aic = np.inf
        # for params in pdq:
        #     model_test = ARIMA(yn, order = params)
        #     result_test = model_test.fit()
        #     if result_test.aic < best_aic:
        #         best_pdq = params
        #         best_aic = result_test.aic
        # print(best_pdq, best_aic)
        # return
        # 8 1 0 - alg
        # 5 0 1 - myself
        mymodel = ARIMA(y[:self.learn_size], order =(coefs[0], coefs[1], coefs[2])) 
        modelfit = mymodel.fit() 
        pred = modelfit.get_prediction(start = y.index[0], end = y.index[-1], dynamic=False)
        pred_ci = pred.conf_int()
        forecasted = pred.predicted_mean[self.learn_size:len(y)]
        actual = y[self.learn_size:] 
        self.dataMeasure.measurePredictions(actual, forecasted)
        if self.PLOTS_ON:
            makePlot(y.index, y,
                    pred.predicted_mean,
                    self.learn_size, name, pred_ci, xname=self.namex, yname=self.namey
                    )

    # SARIMAX
    def sarimax(self, y, coefs, name='SARIMAX'):
        import warnings
        warnings.filterwarnings("ignore")
        # kpssTest(yn[yn.columns[0]], 'original')
        
        # #yn = yn.squeeze(axis=1).dropna()
        # yn['box'], lmbda = scs.boxcox(yn[yn.columns[0]])

        # kpssTest(yn['box'], 'box')

        # ps = range(0, 5)
        # d=1
        # qs = range(0, 4)
        # Ps = range(0, 5)
        # D=1
        # Qs = range(0, 1)

        #from itertools import product

        # parameters = product(ps, qs, Ps, Qs)
        # parameters_list = list(parameters)
        # results = []
        # best_aic = float("inf")

        # for param in tqdm(parameters_list):
        #     #try except нужен, потому что на некоторых наборах параметров модель не обучается
        #     try:
        #         model=sm.tsa.statespace.SARIMAX(yn['box'], order=(param[0], d, param[1]), 
        #                                         seasonal_order=(param[2], D, param[3], 24*7)).fit(disp=-1)
        #     #выводим параметры, на которых модель не обучается и переходим к следующему набору
        #     except ValueError:
        #         print('wrong parameters:', param)
        #         continue
        #     aic = model.aic
        #     #сохраняем лучшую модель, aic, параметры
        #     if aic < best_aic:
        #         best_model = model
        #         best_aic = aic
        #         best_param = param
        #     results.append([param, model.aic])

        # warnings.filterwarnings('default')

        # result_table = pd.DataFrame(results)
        # result_table.columns = ['parameters', 'aic']
        # print(f'---\nBest is {best_param}\n---')
        # print(result_table.sort_values(by = 'aic', ascending=True).head())
        #return

        mymodel = sm.tsa.statespace.SARIMAX(y[:self.learn_size], order =(coefs[0], coefs[1], coefs[2]))
        modelfit = mymodel.fit(disp=-1)
        pred = modelfit.get_prediction(start = y.index[0], end = y.index[-1], dynamic=False)
        pred_ci = pred.conf_int()
        forecasted = pred.predicted_mean[self.learn_size:len(y)]
        actual = y[self.learn_size:] 
        self.dataMeasure.measurePredictions(actual, forecasted)
        if self.PLOTS_ON:
            makePlot(y.index, y,
                    pred.predicted_mean, self.learn_size,
                    name, pred_ci, xname=self.namex, yname=self.namey
                    )