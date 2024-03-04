import pandas as pd
import numpy as np

from source.utils.dataload import loadData
from source.algorithms.algos import Algos
from source.utils.dataedit import makeDataContinuous

class Covid:
    def __init__(self, path, learn_size) -> None:
        self.data = loadData(path)
        self.filterData()
        self.algos = Algos(int(len(self.data) * learn_size), '', '', True)

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
        new_data["Date"] = pd.to_datetime(new_data["Date"], format='%Y/%m/%d')
        self.data = new_data.copy()

        # tmp draw
        # plt.plot(new_data['date'], new_data['death_cnt'], label='deathes')
        # plt.plot(new_data['date'], new_data['hosp_cnt'], label='hosps')
        # plt.plot(new_data['date'], new_data['ill_cnt'], label='ills')
        # plt.xticks(np.arange(0, len(new_data), len(new_data) // 10))
        # plt.show()

    def makePredictions(self, param):
        linearCoefs = [1,2,3,4,5,10]
        arimaCoefs = [[2, 4, 3], [5, 0, 1], [8, 1, 0], [1, 1, 1]]
        movingAverageCoefs = [1, 2, 4, 7]
        sarimaxCoefs = [[3, 2, 0], [8, 1, 0], [1, 1, 1]]

        self.algos.changeAxisNames('Date', param)
        #contData = makeDataContinuous(self.data, 'Date', '1d')
        data = self.data.loc[:, ["Date", param]]

        # coefs = self.algos.findSARIMAXCoefs(contData[param], [0, 3], [0, 3], [0, 3],[0, 3], [0, 3], [0, 3], [0, 30], printFlag=True)
        # print(coefs)

        # for lc in linearCoefs:
        #     self.algos.linearRegression(self.data[['Date', param]], lc, f'Linear regression with degree = {lc}')

        # for lc in linearCoefs:
        #     for mac in movingAverageCoefs:
        #         self.algos.movingAverage(self.data[['Date', param]], mac, self.algos.linearRegression, lc, f'Linear regression with degree = {lc}')

        # for ac in arimaCoefs:
        #     self.algos.arima(contData[param], ac, f'ARIMA with p = {ac[0]}, d = {ac[1]}, q = {ac[2]}')

        # for ac in arimaCoefs:
        #    for mac in movingAverageCoefs:
        #         self.algos.movingAverage(contData[param], mac, self.algos.arima, ac, f'ARIMA with p = {ac[0]}, d = {ac[1]}, q = {ac[2]}')

        # for sc in sarimaxCoefs:
        #     self.algos.sarimax(contData[param], sc, f'SARIMAX with p = {sc[0]}, d = {sc[1]}, q = {sc[2]}')
        for i in range(2):
            self.algos.narx(data, [2, 100, 1000])
            print(i)
        self.algos.outtbl.save()
