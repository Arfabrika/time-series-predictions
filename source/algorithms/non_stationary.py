from statsmodels.tsa.stattools import adfuller, kpss
import numpy as np
import pandas as pd

def checkP(data):
    result = adfuller(data)
    print('p-value: %f' % result[1])

def invboxcox(y,lmbda):
    # обрабтное преобразование Бокса-Кокса
    if lmbda == 0:
        return(np.exp(y))
    else:
        return(np.exp(np.log(lmbda*y+1)/lmbda))
    
def kpssTest(y, name):
    kpsstest = kpss(y, regression='c')
    kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
    for key,value in kpsstest[3].items():
        kpss_output['Critical Value (%s)'%key] = value
    print(f"---\nkpss test for {name}\n")
    print(kpss_output)
    print("---\n")