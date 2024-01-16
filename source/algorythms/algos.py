import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score 
from statsmodels.tsa.arima.model import ARIMA 
import itertools
from source.utils.plots import makePlot
import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.pyplot as plt
from source.algorythms.non_stationary import invboxcox, kpssTest
from tqdm import tqdm


PLOTS_ON = True

def linearRegression(sizes, yn, pow, name = 'Linear regression'):
    date_pred = pd.date_range(start=pd.to_datetime(yn["Date"]).min(), freq='1m', periods=sizes[0])
    yn['Date']= pd.to_datetime(yn['Date'])
    x = np.array(pd.to_numeric(yn['Date']))
    coefs = np.polyfit(x[:sizes[1]], yn[yn.columns[1]][:sizes[1]], pow)
    x_pred_arr = pd.to_numeric(date_pred)
    y_pred = np.polyval(coefs, x_pred_arr)
    print(f"mean squared error: {mean_squared_error(yn[yn.columns[1]][:sizes[1]], y_pred[:sizes[1]])}")
    print(f"coefficient of determination: {r2_score(yn[yn.columns[1]][:sizes[1]], y_pred[:sizes[1]])}")
    if PLOTS_ON:
        makePlot(yn['Date'], yn[yn.columns[1]], date_pred, y_pred, date_pred[225:], y_pred[225:], sizes[1], name)

def movingAverage(sizes, yn, windowSize, func, funcparams, name):
    y_pred = yn[yn.columns[1]].rolling(window=windowSize).mean()
    for i in range(windowSize - 1):
        y_pred[i] = yn[yn.columns[1]][i]
    newData = pd.concat([yn['Date'], y_pred], axis=1)
    func(sizes, newData, funcparams,  name + f' with moving average, window size = {windowSize}')

# ARIMA
def arima(sizes, y, coefs, name='ARIMA', ytrain=[]):
    import warnings
    warnings.filterwarnings("ignore")
    
    yn = y.copy(True)
    yn['Date']= pd.to_datetime(yn['Date'])
    yn.set_index(keys='Date', drop=True, inplace=True)
    yn = yn.squeeze(axis=1).dropna()

    ytrain = ytrain.copy(True)
    ytrain['Date']= pd.to_datetime(ytrain['Date'])
    ytrain.set_index(keys='Date', drop=True, inplace=True)
    ytrain = ytrain.squeeze(axis=1).dropna()

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
    mymodel = ARIMA(yn[:sizes[1]], order =(coefs[0], coefs[1], coefs[2])) 
    modelfit = mymodel.fit() 
    #print(modelfit.summary())
    date_pred = pd.date_range(start=pd.to_datetime(yn.index).min(), freq='1m', periods=sizes[0])
    pred = modelfit.get_prediction(start = yn.index[0], end = date_pred[-2], dynamic=False)
    pred_ci = pred.conf_int()
    if PLOTS_ON:        
        makePlot(yn.index, yn,
                 date_pred, pred.predicted_mean,
                 date_pred[len(yn.index):], pred.predicted_mean[len(yn.index):],
                  sizes[1], name, pred_ci
                 )
    forecasted = pred.predicted_mean[:sizes[1]]
    actual = yn[:sizes[1]]
    print(f"mean squared error: {mean_squared_error(actual, forecasted)}")
    print(f"coefficient of determination: {r2_score(actual, forecasted)}")

# SARIMA
def sarima(sizes, y, coefs, name='SARIMA', ytrain=[]):
    import warnings
    warnings.filterwarnings("ignore")
    
    yn = y.copy(True)
    yn['Date']= pd.to_datetime(yn['Date'])
    yn.set_index(keys='Date', drop=True, inplace=True)

    kpssTest(yn[yn.columns[0]], 'original')
    
    #yn = yn.squeeze(axis=1).dropna()
    yn['box'], lmbda = scs.boxcox(yn[yn.columns[0]])

    kpssTest(yn['box'], 'box')

    # ytrain = ytrain.copy(True)
    # ytrain['Date']= pd.to_datetime(ytrain['Date'])
    # ytrain.set_index(keys='Date', drop=True, inplace=True)
    # ytrain = ytrain.squeeze(axis=1).dropna()

    ps = range(0, 5)
    d=1
    qs = range(0, 4)
    Ps = range(0, 5)
    D=1
    Qs = range(0, 1)

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

    mymodel = sm.tsa.statespace.SARIMAX(yn['Rust'][:sizes[1]], order =(coefs[0], coefs[1], coefs[2])).fit(disp=-1)
    sarima_model = invboxcox(mymodel.fittedvalues, lmbda)
    #forecast = invboxcox(mymodel.predict(start = yn.index[1], end = yn.index[-1]), lmbda)
    forecast =mymodel.predict(start = yn.index[1], end = yn.index[-1])
    #forecast = sarima_model._append(forecast).values[-120:]
    actual = yn[yn.columns[0]]
    plt.figure(figsize=(15, 7))
    plt.plot(forecast, color='r', label="model")
    plt.title("SARIMA model\n Mean absolute error {} users".format(1))#round(mean_absolute_error(data.dropna().Users, data.dropna().arima_model))))
    plt.plot(actual, label="actual")
    plt.legend()
    #plt.axvspan(len(actual), len(forecast), alpha=0.5, color='lightgrey')
    plt.grid(True)
    plt.show()
    # modelfit = mymodel.fit()   
    # date_pred = pd.date_range(start=pd.to_datetime(yn.index).min(), freq='1m', periods=sizes[0])
    # pred = modelfit.get_prediction(start = yn.index[0], end = date_pred[-2], dynamic=False)
    # pred_ci = pred.conf_int()
    # if PLOTS_ON:        
    #     makePlot(yn.index, yn,
    #              date_pred, pred.predicted_mean,
    #              date_pred[len(yn.index):], pred.predicted_mean[len(yn.index):],
    #               sizes[1], name, pred_ci
    #              )
    # forecasted = pred.predicted_mean[:sizes[1]]
    # actual = yn[:sizes[1]]
    # print(f"mean squared error: {mean_squared_error(actual, forecasted)}")
    # print(f"coefficient of determination: {r2_score(actual, forecasted)}")