import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras import layers
import tensorflow as tf

class NARX:
    """
    params:
    0 - sequence_length
    1 - epoch_cnt
    2 - ind_shift
    """
    def __init__(self, data, params = [1, 100, 1000], window_params = {}) -> None:
        # TODO Протестить на разных количествах нейронов и разных метриках
        self.data = data
        self.sequence_length = params[0]
        self.data.insert(0, "Ind",[i + params[2] for i in range(len(data))], True)
        self.epoch_cnt = params[1]
        self.inddata = self.data.iloc[:, [0, -1]]
        self.window_params = window_params

    def predict(self):
        def create_sequences(self, data, flatten=False):
            inputs = []
            targets = []
            data_size = len(data)
            datanumpy = data.to_numpy()
            
            for i in range(data_size - self.sequence_length):
                sequence = datanumpy[i:i + self.sequence_length]
                label_position = i + self.sequence_length
                label = datanumpy[label_position][1]
                if flatten:
                    inputs.append(sequence.flatten())
                else:
                    inputs.append(sequence)
                targets.append(label)
                
            return np.array(inputs), np.array(targets)

        scaler = MinMaxScaler()
        scaler.fit(self.inddata)
        scaled = scaler.fit_transform(self.inddata)
        data = pd.DataFrame(scaled, columns=self.inddata.columns)
        x, y = create_sequences(self, data, flatten=True)

        narx_model = keras.Sequential([
            layers.Dense(2, activation='tanh',input_shape=(x.shape[1],)),
            layers.Dense(1, activation='relu')
        ])

        narx_model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss='mse',
            metrics='mae'
        )

        x_win = x[self.window_params["start_pos"]:self.window_params["stop_pos"]].copy()
        y_win = y[self.window_params["start_pos"]:self.window_params["stop_pos"]].copy()
        print(f"start_pos = {self.window_params}\nx_win = {x_win}\ny_win = {y_win}\n")

        narx_model.fit(x_win,
                       y_win,
                       epochs=self.epoch_cnt, validation_split=0, verbose=1)
        predicted = narx_model(x.copy())

        new_data = self.data[["Ind"]].iloc[self.window_params["start_pos"]:len(predicted)]
        new_data.insert(1, "Data", predicted[self.window_params["start_pos"]:len(predicted)], True)

        unscaled = scaler.inverse_transform(new_data)
        y = []
        for el in unscaled:
            y.append(el[1])
        return predicted