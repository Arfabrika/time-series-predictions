import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score 
from statsmodels.tsa.arima.model import ARIMA 
import itertools

# 227 strs, from 2004-07-01 to 2023-05-01
#pred size: 250, from 2004-07-01 to 2024-04-01
# training limit: 158
data_all = pd.read_csv("./datasets/programming languages.csv")
date = pd.to_datetime(data_all["Date"])
date_pred = pd.date_range(start=date.min(), freq='1m', periods=238)
data = data_all[["Date",'C/C++']]
PLOTS_ON = True

def linearRegression(yn, pow, name = 'Linear regression'):
    yn['Date']= pd.to_datetime(yn['Date'])
    x = np.array(pd.to_numeric(yn['Date']))
    coefs = np.polyfit(x[:int(len(x) * 0.7)], yn['C/C++'][:int(len(yn) * 0.7)], pow)
    x_pred_arr = pd.to_numeric(date_pred)
    y_pred = np.polyval(coefs, x_pred_arr)
    print(f"mean squared error: {mean_squared_error(yn['C/C++'][:158], y_pred[:158])}")
    print(f"coefficient of determination: {r2_score(yn['C/C++'][:158], y_pred[:158])}")
    if PLOTS_ON:
        makePlot(yn['Date'], yn['C/C++'], date_pred, y_pred, date_pred[225:250], y_pred[225:250], name)

def movingAverage(yn, windowSize, func, funcparams, name):
    y_pred = yn['C/C++'].rolling(window=windowSize).mean()
    for i in range(windowSize - 1):
        y_pred[i] = yn['C/C++'][i]
    newData = pd.concat([yn['Date'], y_pred], axis=1)
    func(newData, funcparams,  name + f' with moving average, window size = {windowSize}')

# ARIMA
def arima(y, coefs, name='ARIMA'):
    import warnings
    warnings.filterwarnings("ignore")
    
    yn = y.copy(True)
    yn['Date']= pd.to_datetime(yn['Date'])
    yn.set_index(keys='Date', drop=True, inplace=True)
    yn = yn.squeeze(axis=1).dropna()

    # подбор коэффициентов
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
    mymodel = ARIMA(yn[:158], order =(coefs[0], coefs[1], coefs[2])) 
    modelfit = mymodel.fit() 
    #print(modelfit.summary())

    pred = modelfit.get_prediction(start='2004-07-01', end='2024-04-01', dynamic=False)
    pred_ci = pred.conf_int()
    if PLOTS_ON:
        ax = yn.plot(label='input data', figsize=(10, 7))
        pred.predicted_mean.plot(ax=ax, label='prediction', alpha=.7)
        ax.fill_between(pred_ci.index,
            pred_ci.iloc[:, 0],
            pred_ci.iloc[:, 1], color='k', alpha=.2)
        plt.legend()
        plt.title(name)
        plt.ylim(5, 15) # 5, 15 for C++
        plt.show()
    forecasted = pred.predicted_mean[:'2023-05-01']
    actual = yn[:158]
    mape = np.mean(np.abs((actual - forecasted)/actual))*100
    print(mape)

def makePlot(x, y, x_ext, y_ext, x_pred, y_pred, title=''):
    plt.plot(x, y, label='input data')
    plt.plot(x_ext, y_ext, label='model')
    plt.plot(x_pred, y_pred, label='prediction')
    plt.axvline(x = x[int(len(x) * 0.7)], label = 'training border', color='r')
    plt.legend()
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Mean popularity in %")
    plt.show()

def mainfunc():
    linearCoefs = [1,2,3,4,5,10]
    arimaCoefs = [[5, 0, 1], [8, 1, 0], [1, 1, 1]]
    movingAverageCoefs = [1, 2, 4, 7]
    # for lc in linearCoefs:
    #     linearRegression(data, lc, f'Linear regression with degree = {lc}')

    for lc in linearCoefs:
        for mac in movingAverageCoefs:
            movingAverage(data, mac, linearRegression, lc, f'Linear regression with degree = {lc}')

    # for ac in arimaCoefs:
    #     arima(data, ac, f'ARIMA with p = {ac[0]}, d = {ac[1]}, q = {ac[2]}')

    # for ac in arimaCoefs:
    #    for mac in movingAverageCoefs:
    #         movingAverage(data, mac, arima, ac, f'ARIMA with p = {ac[0]}, d = {ac[1]}, q = {ac[2]}')

if __name__ == '__main__':
    mainfunc()