import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score 
import itertools
from source.utils.plots import makePlot

from source.algorythms.algos import arima, linearRegression, movingAverage, sarima
from source.utils.dataload import loadData
from source.algorythms.non_stationary import checkP
import scipy.stats as scs
import statsmodels.tsa.api as smt
import statsmodels.api as sm
from datetime import datetime

# 227 strs, from 2004-07-01 to 2023-05-01
#pred size: 250, from 2004-07-01 to 2024-04-01
# training limit: 158 (2017-09-01)
PLOTS_ON = True

def tsplot(y, lags=None, figsize=(12, 7), style='bmh'):
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    with plt.style.context(style):    
        fig = plt.figure(figsize=figsize)
        layout = (2, 2)
        ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
        acf_ax = plt.subplot2grid(layout, (1, 0))
        pacf_ax = plt.subplot2grid(layout, (1, 1))

        y.plot(ax=ts_ax)
        ts_ax.set_title('Time Series Analysis Plots')
        smt.graphics.plot_acf(y, lags=lags, ax=acf_ax, alpha=0.5)
        smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax, alpha=0.5)

        print("Критерий Дики-Фуллера: p=%f" % sm.tsa.stattools.adfuller(y)[1])

        plt.tight_layout()
        plt.show()
    return

from statsmodels.tsa.stattools import kpss

class PL:
    def __init__(self, path, sizes, learn_size) -> None:
        self.data_all = loadData(path)
        self.sizes = sizes
        self.learn_size = learn_size
        self.sizes[1] = int(self.sizes[0] * self.learn_size)

        for i in range(len(self.data_all["Date"])):
            self.data_all["Date"].iloc[i] = pd.Timestamp(datetime.strptime(self.data_all["Date"].iloc[i], '%B %Y'))

    def analyzeLanguage(self, lang):
        # self.data_all["Date"] = pd.to_datetime(self.data_all["Date"], format='%Y-%m')
        data = self.data_all.loc[:, ["Date", lang]]
        
        # #checkP(data[lang])
        # # tsplot(data[lang], lags=30)
        # data['log'] = np.log(data[lang])
        # #checkP(data['log'])
        # #data['без_тренда'] = data[lang] - data[lang].rolling(window=5).mean()
        # data['без_тренда'] = data['log'] - data['log'].rolling(window=5).mean()
        
        # data.dropna(inplace=True)
        # #checkP(data['без_тренда'])
        # # tsplot(data['без_тренда'], lags=30)
        # data['Users_box'], lmbda = scs.boxcox(data['без_тренда'] + 0.8) # прибавляем единицу, так как в исходном ряде есть нули
        
        # # tsplot(data.Users_box, lags=30)
        # checkP(data['Users_box'])
        # # kpsstest = kpss(data['Users_box'], regression='c')
        # # kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
        # # for key,value in kpsstest[3].items():
        # #     kpss_output['Critical Value (%s)'%key] = value
        # # print (kpss_output)
        # data['Users_box'] += 0.8

        # print("Оптимальный параметр преобразования Бокса-Кокса: %f" % lmbda)
        # plt.plot(data['Date'], data[lang], data['Users_box'])
        # plt.legend()
        # plt.show()
        
        linearCoefs = [1,2,3,4,5,10]
        arimaCoefs = [[5, 0, 1], [8, 1, 0], [1, 1, 1]]
        movingAverageCoefs = [1, 2, 4, 7]
        for lc in linearCoefs:
            linearRegression(self.sizes, data[['Date', lang]], lc, f'Linear regression with degree = {lc}')

        # for lc in linearCoefs:
        #     for mac in movingAverageCoefs:
        #         movingAverage(sizes, data, mac, linearRegression, lc, f'Linear regression with degree = {lc}')

        # for ac in arimaCoefs:
        #     arima(sizes, data, ac, f'ARIMA with p = {ac[0]}, d = {ac[1]}, q = {ac[2]}')

        # for ac in arimaCoefs:
        #    for mac in movingAverageCoefs:
        #         movingAverage(sizes, data, mac, arima, ac, f'ARIMA with p = {ac[0]}, d = {ac[1]}, q = {ac[2]}')
        # linearRegression(self.sizes, data, 2, f'Linear regression with degree = {2}')


        #sarima(self.sizes, data[['Date', lang]], [3, 2, 0, lmbda], f'ARIMA with p = {5}, d = {0}, q = {1}', data[['Date','без_тренда']])