import numpy as np
import pandas as pd
import itertools
from datetime import datetime
import matplotlib.pyplot as plt

from statsmodels.tsa.arima.model import ARIMA

timeseries = pd.read_csv('./source/programming-languages/crude-oil-exports-by-type-monthly.csv', header=0,delimiter=',')
# print(timeseries)
timeseries = timeseries.loc[timeseries['Oil Type']=='Total'].filter(['Period','Volume (bbl/d)'])
# print(timeseries)
timeseries['Period'] = timeseries['Period'].transform(lambda x: datetime.strptime(x, '%m/%d/%Y'))
print(timeseries)
timeseries.set_index(keys='Period', drop=True, inplace=True)
print(timeseries)
timeseries = timeseries.squeeze(axis=1)
print(timeseries)
model = ARIMA(timeseries, order=(9,2,1)) #вставьте свои числа вместо p, d и q
result = model.fit()
pred = result.get_prediction(start='2000-01-01', end='2024-01-01', dynamic=False)
pred_ci = pred.conf_int()

ax = timeseries['2000':].plot(label='observed', figsize=(10, 7))
pred.predicted_mean.plot(ax=ax, label='forecast', alpha=.7)
ax.fill_between(pred_ci.index,
pred_ci.iloc[:, 0],
pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Дата')
ax.set_ylabel('Средний объем экспорта нефти (баррелей в день)')
plt.legend()
plt.show()