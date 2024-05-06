from torch import nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sysidentpy.neural_network import NARXNN
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from sysidentpy.basis_function import Polynomial
from sysidentpy.utils.narmax_tools import regressor_code


def makeData(path, param, isPL):
    data_all = pd.read_csv(path)
    if isPL:
        for i in range(len(data_all["Date"])):
            data_all.loc[i, "Date"] = pd.to_datetime(datetime.strptime(data_all["Date"].iloc[i], '%B %Y'))
    else:
         data_all["Date"] = pd.to_datetime(data_all["Date"], format='%Y/%m/%d')
    return data_all[["Date", param]]

class Model(nn.Module):
    def __init__(self, params, input_size):
        super().__init__()
        lay_arr = []
        lay_arr.append(nn.Linear(input_size, params[2]))
        for i in range(1, params[0]):
             lay_arr.append(nn.Linear(params[2], params[2]))
        lay_arr.append(nn.Linear(params[2], 1))
        self.lay_arr = nn.ModuleList(lay_arr)
        self.tanh = nn.Tanh()

    def forward(self, xb):
        z = self.lay_arr[0](xb)
        for i in range(1, len(self.lay_arr)):
            z = self.tanh(z)
            z = self.lay_arr[i](z)
        return z

"""
params:
0 - number of layers
1 - polynom degree
2 - number of neirons
3 - number of epochs
4 - data shift
"""
class NARX:
    def __init__(self, data, params, window_params):
        self.data = data
        inddata = data.copy()
        inddata.insert(0, "Ind",[i + params[4] for i in range(len(data))], True)
        self.inddata = inddata.iloc[:, [0, -1]]
        self.params = params
        self.basis_function=Polynomial(degree=params[1])
        self.startpos = window_params["start_pos"]
        self.stoppos = window_params["stop_pos"]
    
    def predict(self):
        scaler = MinMaxScaler()
        scaler.fit(self.inddata)
        scaled = scaler.fit_transform(self.inddata)
        data_sc = pd.DataFrame(scaled, columns=self.inddata.columns)
        
        arr_x = []
        arr_y = []
        for i in range(len(data_sc)):
            arr_x.append([data_sc['Ind'][i]])
            arr_y.append([data_sc[data_sc.columns[-1]][i]])

        arr_x = np.array(arr_x)
        arr_y = np.array(arr_y)
        
        regressors = regressor_code(
            X=arr_x[self.startpos:self.stoppos],
            xlag=2,
            ylag=2,
            model_type="NARMAX",
            model_representation="neural_network",
            basis_function=self.basis_function
        )

        narx_net = NARXNN(
        net=Model(self.params, regressors.shape[0]),
        ylag=2,
        xlag=2,
        basis_function=self.basis_function,
        model_type="NARMAX",
        loss_func='mse_loss',
        optimizer='Adam',
        epochs=self.params[3],
        verbose=False,
        optim_params={'betas': (0.9, 0.999), 'eps': 1e-05}
        )

        narx_net.fit(X=arr_x[self.startpos:self.stoppos],
                     y=arr_y[self.startpos:self.stoppos])
        yhat = narx_net.predict(X=arr_x[self.startpos:], y=arr_y[self.startpos:])

        y = []
        for el in yhat:
            y.append(el[0])

        new_data = self.inddata[["Ind"]][self.startpos:]
        new_data.insert(1, "Data", y, True)

        unscaled = scaler.inverse_transform(new_data)
        y = []
        for el in unscaled:
            y.append(el[1])

        return y
