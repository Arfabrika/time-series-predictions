from statsmodels.tsa.stattools import adfuller, kpss

# тесты на стационарность возвращают True, если ряд стационарен
def statCheck(y):
    def adfullerTest(data):
        result = adfuller(data)
        if result[1] < 0.05: 
            return True
        return False

    def kpssTest(y):
        kpsstest = kpss(y, regression='c')
        if kpsstest[1] < 0.05 and kpsstest[0] > kpsstest[3]['5%']:
            return False
        return True

    res1 = adfullerTest(y)
    return res1 & kpssTest(y)
