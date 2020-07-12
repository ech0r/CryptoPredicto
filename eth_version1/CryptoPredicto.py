from NeuralNetwork import NeuralNet
import numpy as np
from datetime import datetime
import os

data = np.genfromtxt('trainingdata.csv', delimiter=',', skip_header=True)

X = data[:-1, [1, 2, 7]]
Y = data.T[1][1:]
# normalize data
max = Y.max(axis=0)
input_max = X.max(axis=0)
X = X/X.max(axis=0)
Y = Y/Y.max(axis=0)

NN = NeuralNet([3, 5, 1], "relu")
# use last row of training data as inputs for prediction
input = data[-1, [1, 2, 7]]
input = input/input_max
NN.train(X, Y, learning_rate=0.01, epochs=1000000)
predicted = (NN.predict(input) * max)
date = datetime.today().strftime('%Y-%m-%d')

line = date + "," + str(round(predicted,2))

filename = "predictedprices.csv"

if not os.path.exists(filename):
	price = open(filename, 'w')
	price.write("Date,ETH_Price\n")
	price.close()

price = open(filename, 'a')
price.write(line + '\n')
price.close()

