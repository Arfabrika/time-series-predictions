import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools

from source.algorithms.algos import Algos
from source.utils.dataload import loadData
from source.utils.dataedit import makeDataContinuous
from source.algorithms.non_stationary import checkP
from source.algorithms.narx import NARX

import scipy.stats as scs
import statsmodels.tsa.api as smt
import statsmodels.api as sm
from datetime import datetime

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

class PL:
    def __init__(self, path, learn_size) -> None:
        self.data_all = loadData(path)
        self.algos = Algos(int(len(self.data_all) * learn_size), 'Date', 'Mean popularity in %')

        for i in range(len(self.data_all["Date"])):
            self.data_all.loc[i, "Date"] = pd.to_datetime(datetime.strptime(self.data_all["Date"].iloc[i], '%B %Y'))

    def analyzeLanguage(self, lang):
        data = self.data_all.loc[:, ["Date", lang]]
        contData = makeDataContinuous(data, 'Date', 'MS')
        
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
        
        linearCoefs = [3]#[i + 1 for i in range(10)]#[1,2,3,4,5,10]
        # arimaCoefs = [[0, 4, 9]]#[[2, 10, 5], [2, 8, 1]]#[[5, 0, 1], [8, 1, 0], [1, 1, 1]] [[1, 3, 3]]
        # movingAverageCoefs = [1, 2, 4, 7]
        sarimaxCoefs = [[0, 4, 9, 3, 0, 1, 25]]# [[0, 4, 9, 3, 0, 1, 20]] [[3, 2, 0], [8, 1, 0], [1, 1, 1]]
        for lc in linearCoefs:
            self.algos.linearRegression(data[['Date', lang]], lc, f'Linear regression with degree = {lc}')

        # for lc in linearCoefs:
        #     for mac in movingAverageCoefs:
        #         self.algos.movingAverage(data, mac, self.algos.linearRegression, lc, f'Linear regression with degree = {lc}')

        # for ac in arimaCoefs:
        #     self.algos.arima(contData, ac, f'ARIMA with p = {ac[0]}, d = {ac[1]}, q = {ac[2]}')

        # for ac in arimaCoefs:
        #    for mac in movingAverageCoefs:
        #         self.algos.movingAverage(contData, mac, self.algos.arima, ac, f'ARIMA with p = {ac[0]}, d = {ac[1]}, q = {ac[2]}')

        # for sc in sarimaxCoefs:
        #     self.algos.sarimax(contData, sc, f'SARIMAX with p = {sc[0]}, d = {sc[1]}, q = {sc[2]}')
        # coefs = self.algos.findARIMACoefs(contData, [0, 11], [0, 11], [0, 11], printFlag=True)
        # coefs.to_excel('pl_coefs_arima.xlsx')
        for i in range(2):
            self.algos.narx(data, [2, 100, 1000])
            print(i)
        #coefs = self.algos.findSARIMAXCoefs(contData, [0, 1], [4, 5], [9, 10], [0, 1], [0, 1], [0, 1], [20, 21], printFlag=True)
        self.algos.outtbl.save()