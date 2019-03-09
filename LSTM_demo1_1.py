from numpy import concatenate
from sklearn.metrics import mean_squared_error
from math import sqrt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import numpy as np
from matplotlib import pyplot
import excel_exercise1 as aa1
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

n_train_and_test = 750
numbers_of_datas = 1000  # 所需要载入的一列数据的数量
excelpath = ['氧含量.xlsx', '流量.xlsx', '压力.xlsx']
# 从文件里读取相应的行和列的数据,输入到一个tf.constant里
a = []
for name in excelpath:
    # 每个各读全部所有的数据列,1000行
    a.append(aa1.xls_arrays(name, 3, 1, 1003, -1))
X = []
for elements in a:
    X = np.hstack((X, elements))
Y = aa1.xls_arrays('温度.xlsx', 3, 1, 1003, -1)

train_X = X[:n_train_and_test, :]
train_X = train_X.reshape(train_X.shape[0], 1, train_X.shape[1])
train_Y = Y[:n_train_and_test, :]

test_X = X[n_train_and_test:, :]
test_X = test_X.reshape(test_X.shape[0], 1, test_X.shape[1])
test_Y = Y[n_train_and_test:, :]

# design network
model = Sequential()
model.add(LSTM(100, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(Y.shape[1]))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_Y, epochs=50, batch_size=72, validation_data=(test_X, test_Y), verbose=2,
                    shuffle=False)

# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

# make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
# invert scaling for forecast
inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
# inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:, 0]
# invert scaling for actual
test_Y = test_Y.reshape((len(test_Y), 1))
inv_y = concatenate((test_Y, test_X[:, 1:]), axis=1)
# inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:, 0]
# calculate RMSE
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)
