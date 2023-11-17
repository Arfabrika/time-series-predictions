import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score 
from statsmodels.tsa.arima.model import ARIMA 
import itertools
from source.utils.plots import makePlot

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
def arima(sizes, y, coefs, name='ARIMA'):
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
    mymodel = ARIMA(yn[:sizes[1]], order =(coefs[0], coefs[1], coefs[2])) 
    modelfit = mymodel.fit() 
    #print(modelfit.summary())
    date_pred = pd.date_range(start=pd.to_datetime(yn.index).min(), freq='1m', periods=sizes[0])
    pred = modelfit.get_prediction(start = yn.index[0], end = date_pred[-2], dynamic=False)
    pred_ci = pred.conf_int()
    if PLOTS_ON:
        # ax = yn.plot(label='input data', figsize=(10, 7))
        # pred.predicted_mean.plot(ax=ax, label='prediction', alpha=.7)
        # ax.fill_between(pred_ci.index,
        #     pred_ci.iloc[:, 0],
        #     pred_ci.iloc[:, 1], color='k', alpha=.2)
        # plt.legend()
        # plt.title(name)
        # plt.ylim(5, 15) # 5, 15 for C++
        # plt.show()
        
        makePlot(yn.index, yn,
                 date_pred, pred.predicted_mean,
                 date_pred[len(yn.index):], pred.predicted_mean[len(yn.index):],
                  sizes[1], name, pred_ci
                 )
    forecasted = pred.predicted_mean[:sizes[1]]
    actual = yn[:sizes[1]]
    print(f"mean squared error: {mean_squared_error(actual, forecasted)}")
    print(f"coefficient of determination: {r2_score(actual, forecasted)}")