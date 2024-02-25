import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras import layers
import tensorflow as tf

from source.utils.plots import makePlot
from source.utils.datameasure import DataMeasure
from source.utils.out_data_table import OutDataTable

PLOTS_ON = True

class NARX:
    def __init__(self, data, target_column, learn_size, sequence_length=1, name = 'NARX') -> None:
        self.data = data
        self.target_column = target_column
        self.sequence_length = sequence_length
        self.learn_size = int(len(data) * learn_size)
        self.dataMeasure = DataMeasure(True)
        columnNames = ['name', 'MAE', 'MAPE', 'MSE', 'R2']
        self.outtbl = OutDataTable(columnNames, 'narx.xlsx', 'MSE')
        self.name = name
        self.data.insert(0, "Ind",[i + 1000 for i in range(len(data))], True)
        self.data = self.data[["Ind", "Rust"]]
        self.old_data = data

    def create_sequences(self, flatten=False):
        inputs = []
        targets = []
        data_size = len(self.data)
        self.datanumpy = self.data.to_numpy()
        
        for i in range(data_size - self.sequence_length):
            sequence = self.datanumpy[i:i + self.sequence_length]
            label_position = i + self.sequence_length
            label = self.datanumpy[label_position][self.target_column]
            if flatten:
                inputs.append(sequence.flatten())
            else:
                inputs.append(sequence)
            targets.append(label)
            
        return np.array(inputs), np.array(targets)
    
    def run(self):
        scaler = MinMaxScaler()
        scaler.fit(self.data)
        scaled = scaler.fit_transform(self.data)
        self.data = pd.DataFrame(scaled, columns=self.data.columns)
        x, y = self.create_sequences(flatten=True)
        # x_train, x_valid = x[:self.learn_size], x[self.learn_size:]
        # y_train, y_valid = y[:self.learn_size], y[self.learn_size:]

        narx_model = keras.Sequential([
            layers.Dense(20, activation='tanh',input_shape=(x.shape[1],)),
            layers.Dense(1, activation='relu')
        ])

        narx_model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss='mse',
            metrics='mae'
        )

        #callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
        narx_model.fit(x,y, epochs=100, validation_split=0.3, verbose=0)
        predicted = narx_model(x)

        new_data = self.data[["Ind"]].iloc[:len(predicted)]
        new_data.insert(1, "Rust", predicted, True)

        unscaled = scaler.inverse_transform(new_data)#[]
        y = []
        # maxval = self.old_data["Rust"].max()
        # TODO reverse from MinMaxScaler
        for i, el in enumerate(unscaled):
            y.append(el[1] )
        metrics = self.dataMeasure.measurePredictions(self.old_data["Rust"].iloc[self.learn_size:len(predicted)],
                                                      y[self.learn_size:])
        out_data = [self.name]
        out_data.extend(metrics.values())
        inds = self.outtbl.makeIndsArr(['name', 'MAE', 'MAPE', 'MSE', 'R2'])
        self.outtbl.add(out_data, inds)
        self.outtbl.write()
        if PLOTS_ON:
            makePlot(self.old_data['Date'].iloc[:len(predicted)], self.old_data["Rust"].iloc[:len(predicted)], 
                     y, self.learn_size,
                     self.name, xname='Date' , yname='Mean popularity in %')