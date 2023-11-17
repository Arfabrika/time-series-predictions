import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score 
from statsmodels.tsa.arima.model import ARIMA 
import itertools
import datetime
from source.utils.plots import makePlot

from source.algorythms.algos import arima, linearRegression, movingAverage
from source.utils.dataload import loadData

# 227 strs, from 2004-07-01 to 2023-05-01
#pred size: 250, from 2004-07-01 to 2024-04-01
# training limit: 158 (2017-09-01)
PLOTS_ON = True

class PL:
    def __init__(self, path, sizes) -> None:
        self.data_all = loadData(path)
        self.sizes = sizes

    def analyzeLanguage(self, lang):
        data = self.data_all[["Date", lang]]
        linearCoefs = [1,2,3,4,5,10]
        arimaCoefs = [[5, 0, 1], [8, 1, 0], [1, 1, 1]]
        movingAverageCoefs = [1, 2, 4, 7]
        # for lc in linearCoefs:
        #     linearRegression(sizes, data, lc, f'Linear regression with degree = {lc}')

        # for lc in linearCoefs:
        #     for mac in movingAverageCoefs:
        #         movingAverage(sizes, data, mac, linearRegression, lc, f'Linear regression with degree = {lc}')

        # for ac in arimaCoefs:
        #     arima(sizes, data, ac, f'ARIMA with p = {ac[0]}, d = {ac[1]}, q = {ac[2]}')

        # for ac in arimaCoefs:
        #    for mac in movingAverageCoefs:
        #         movingAverage(sizes, data, mac, arima, ac, f'ARIMA with p = {ac[0]}, d = {ac[1]}, q = {ac[2]}')
        linearRegression(self.sizes, data, 2, f'Linear regression with degree = {2}')
        arima(self.sizes, data, [5, 0, 1], f'ARIMA with p = {5}, d = {0}, q = {1}')