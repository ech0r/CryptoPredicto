from NeuralNetwork import NeuralNet
import numpy as np
from datetime import datetime
import os

data = np.genfromtxt('trainingdata.csv', delimiter=',', skip_header=True)

X = data[:-1, [1, 2, 7, 8, 9]]

Y_high = data.T[9][1:]
Y_low = data.T[8][1:]
Y_mid = data.T[1][1:]

input_max = X.max(axis=0)
X = X/X.max(axis=0)

output_max_high = Y_high.max(axis=0)
output_max_low = Y_low.max(axis=0)
output_max_mid = Y_mid.max(axis=0)

Y_high = Y_high/output_max_high
Y_low = Y_low/output_max_low
Y_mid = Y_mid/output_max_mid

NN = NeuralNet([5, 7, 1], "relu")

# use last row of data as inputs for prediction - not part of training data
input = data[-1, [1, 2, 7, 8, 9]]
input = input/input_max

NN.train(X, Y_high, learning_rate=0.01, epochs=1000000)
predicted_high = (NN.predict(input) * output_max_high)

NN.train(X, Y_low, learning_rate=0.01, epochs=1000000)
predicted_low = (NN.predict(input) * output_max_low)

NN.train(X, Y_mid, learning_rate=0.01, epochs=1000000)
predicted_mid = (NN.predict(input) * output_max_mid)

date = datetime.today().strftime('%Y-%m-%d')

line = date + "," + str(round(predicted_high,2)) + "," + str(round(predicted_low,2)) + "," + str(round(predicted_mid,2))

filename = "predictedprices.csv"

if not os.path.exists(filename):
	price = open(filename, 'w')
	price.write("Date,BTC_Price_High,BTC_Price_Low,BTC_Price_Mid\n")
	price.close()

price = open(filename, 'a')
price.write(line + '\n')
price.close()
