import math
from matplotlib import pyplot as plt

import pandas as pd
import numpy as np

import torch

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

import mlflow

from ..core.endpoint import ModelEndpoint
from ..core.trainer import Trainer
from ..models.lstm import LSTM

class LSTMEndpoint(ModelEndpoint):
    path = '/lstm'

    def get(self):
        data = pd.read_csv('src/data/AAPL_2012-1-1_2018-1-1.csv')
        dataset = data[["Timestamp", "Close"]]
        dataset.set_index("Timestamp", inplace=True)
        dataset = dataset.fillna(method="ffill")

        train_set, test_set = train_test_split(dataset, train_size=0.8)
        scaler = MinMaxScaler(feature_range=(-1, 1)).fit(train_set)
        train_scaled = scaler.transform(train_set)
        test_scaled = scaler.transform(test_set)

        lookback = 30
        def create_lookback(stock, lookback):
            Xs, ys = [], []

            for i in range(len(stock)-lookback):
                v = stock[i:i+lookback]
                Xs.append(v)
                ys.append(stock[i+lookback])

            return np.array(Xs), np.array(ys)

        x_train, y_train = create_lookback(train_scaled, lookback)
        x_test, y_test = create_lookback(test_scaled, lookback)
        print('x_train.shape = ', x_train.shape)
        print('y_train.shape = ', y_train.shape)
        print('x_test.shape = ', x_test.shape)
        print('y_test.shape = ', y_test.shape)

        x_train = torch.from_numpy(x_train).type(torch.Tensor)
        x_test = torch.from_numpy(x_test).type(torch.Tensor)
        y_train = torch.from_numpy(y_train).type(torch.Tensor)
        y_test = torch.from_numpy(y_test).type(torch.Tensor)

        model = LSTM(1, 32, 2, 1)
        loss_fn = torch.nn.MSELoss()
        optim = torch.optim.Adam(model.parameters(), lr=0.01)

        trainer = Trainer(model, loss_fn, optim)
        y_train_pred = trainer.train(100, x_train, y_train)

        # invert predictions
        y_train_pred = scaler.inverse_transform(y_train_pred.detach().numpy())
        y_train = scaler.inverse_transform(y_train.detach().numpy())
        # y_test_pred = scaler.inverse_transform(y_test_pred.detach().numpy())
        # y_test = scaler.inverse_transform(y_test.detach().numpy())

        # calculate root mean squared error
        trainScore = math.sqrt(mean_squared_error(y_train[:,0], y_train_pred[:,0]))
        print('Train Score: %.2f RMSE' % (trainScore))
        # testScore = math.sqrt(mean_squared_error(y_test[:,0], y_test_pred[:,0]))
        # print('Test Score: %.2f RMSE' % (testScore))
        mlflow.pytorch.save_model(model, "model")
