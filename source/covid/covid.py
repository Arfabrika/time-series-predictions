import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from source.utils.dataload import loadData
from source.algorythms.algos import arima, linearRegression, movingAverage, sarima

class Covid:
    def __init__(self, path, learn_size) -> None:
        self.data = loadData(path)
        self.learn_size = learn_size
        self.filterData()

    def filterData(self):
        self.data = self.data.drop([ "cdc_report_dt", "pos_spec_dt", "current_status",
                        "cdc_case_earliest_dt ", "age_group", 'medcond_yn', 'sex', 'race_ethnicity_combined' ], axis=1)
        self.data = self.data.loc[(self.data['hosp_yn'] != 'Missing') & (self.data['hosp_yn'] != 'Unknown')]
        self.data = self.data.loc[(self.data['icu_yn'] != 'Missing') & (self.data['icu_yn'] != 'Unknown')]
        self.data = self.data.loc[(self.data['death_yn'] != 'Missing') & (self.data['death_yn'] != 'Unknown')]
        #self.data = self.data.loc[(self.data['medcond_yn'] != 'Missing') & (self.data['medcond_yn'] != 'Unknown')]
        self.data = self.data.dropna()
    
        unique_dates = self.data['onset_dt'].unique()
        deaths = []
        hosps = []
        ills = []
        for el in list(unique_dates):
            fr = self.data[self.data['onset_dt'] == el]
            cur_death = len(fr[fr['death_yn'] == 'Yes'])
            cur_hosp = len(fr[fr['hosp_yn'] == 'Yes'])
            deaths.append(cur_death)
            hosps.append(cur_hosp)
            ills.append(len(fr))
        new_data = pd.DataFrame({'Date': unique_dates, 'death_cnt': deaths, 'hosp_cnt': hosps, 'ill_cnt': ills})
        new_data = new_data.sort_values('Date')
        #print(new_data.head())
        new_data["Date"] = pd.to_datetime(new_data["Date"], format='%Y/%m/%d')
        #print(new_data.head())
        self.data = new_data.copy()

        # tmp draw
        # plt.plot(new_data['date'], new_data['death_cnt'], label='deathes')
        # plt.plot(new_data['date'], new_data['hosp_cnt'], label='hosps')
        # plt.plot(new_data['date'], new_data['ill_cnt'], label='ills')
        # plt.xticks(np.arange(0, len(new_data), len(new_data) // 10))
        # plt.show()

    def makePredictions(self, param):
        linearCoefs = [1,2,3,4,5,10]
        arimaCoefs = [[5, 0, 1], [8, 1, 0], [1, 1, 1]]
        movingAverageCoefs = [1, 2, 4, 7]

        for lc in linearCoefs:
            linearRegression([len(self.data), int(len(self.data) * self.learn_size)], self.data[['Date', param]], lc, f'Linear regression with degree = {lc}')
