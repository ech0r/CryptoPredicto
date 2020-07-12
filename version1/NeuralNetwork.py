import numpy as np
import pickle
# import matplotlib.pyplot as plt


class NeuralNet:
    def __init__(self, network_architecture, switch=None):
        # create seed for random number generation
        np.random.seed(0)
        self.switch = switch
        self.num_layers = len(network_architecture)
        self.architecture = network_architecture
        self.weights = []
        self.error = 0.0
        self.errorlist = []
        # initialize weight values
        for layer in range(self.num_layers - 1):
            weight = 2 * np.random.rand(network_architecture[layer] + 1, network_architecture[layer + 1]) - 1
            self.weights.append(weight)

    def relu(self, x):
        return np.where(x < 0, 0.01 * x, x)

    def relu_d(self, x):
        return np.where(x < 0, 0.01, 1)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_d(self, x):
        return np.multiply(x, 1.0 - x)

    def tanh(self, x):
        return (1.0 - np.exp(-2 * x)) / (1.0 + np.exp(-2 * x))

    def tanh_d(self, x):
        return (1 + self.tanh(x)) * (1 - self.tanh(x))

    def act(self, x):
        if self.switch == "relu":
            return self.relu(x)
        elif self.switch == "tanh":
            return self.tanh(x)
        else:
            return self.sigmoid(x)

    def act_d(self, x):
        if self.switch == "relu":
            return self.relu_d(x)
        elif self.switch == "tanh":
            return self.tanh(x)
        else:
            return self.sigmoid_d(x)

    def forward(self, x):
        y = x
        for i in range(len(self.weights) - 1):
            weighted_sum = np.dot(y[i], self.weights[i])
            layer_output = self.act(weighted_sum)

            # add bias - always on neuron
            layer_output = np.concatenate((np.ones(1), np.array(layer_output)))
            y.append(layer_output)
        weighted_sum = np.dot(y[-1], self.weights[-1])
        layer_output = self.act(weighted_sum)
        y.append(layer_output)
        return y

    def backward(self, y, known, learning_rate):
        error = known - y[-1]
        error_delta = [error * self.act_d(y[-1])]
        self.error = error
        # starting from 2nd to last layer
        for i in range(self.num_layers - 2, 0, -1):
            error = error_delta[-1].dot(self.weights[i][1:].T)
            error = error * self.act_d(y[i][1:])
            error_delta.append(error)
        # we reverse the list of layer deltas to match the order of our weights
        error_delta.reverse()
        # now we update our weights using the delta from each layer
        for i in range(len(self.weights)):
            layer = y[i].reshape(1, self.architecture[i] + 1)
            delta = error_delta[i].reshape(1, self.architecture[i + 1])
            self.weights[i] += learning_rate * layer.T.dot(delta)

    def train(self, data, labels, learning_rate=0.1, epochs=10000):
        # add bias to input layer - always on
        ones = np.ones((1, data.shape[0]))
        z = np.concatenate((ones.T, data), axis=1)
        for k in range(epochs):
            # if (k + 1) % 10000 == 0:
            #     print('epochs: {}'.format(k + 1))
            sample = np.random.randint(data.shape[0])
            # feed data forward through our network
            x = [z[sample]]
            y = self.forward(x)

            known = labels[sample]
            self.backward(y, known, learning_rate)
            self.errorlist.append(self.error)

    def saveweights(self):
        with open('weights', 'wb') as f:
            pickle.dump(self.weights, f)

    def readweights(self):
        with open('weights', 'rb') as f:
            self.weights = pickle.load(f)

    def predict(self, x):
        result = np.concatenate((np.ones(1).T, np.array(x)))
        for i in range(0, len(self.weights)):
            result = self.act(np.dot(result, self.weights[i]))
            result = np.concatenate((np.ones(1).T, np.array(result)))
        return result[1]


# Below code was for testing/debug
'''
NN = NeuralNet([3, 5, 1], "relu")

data = np.genfromtxt('train.csv', delimiter=',', skip_header=True)
X = data[:-1, [1, 2, 7]]
Y = data.T[1][1:]
max = Y.max(axis=0)
X = X/X.max(axis=0)
Y = Y/Y.max(axis=0)

NN.train(X, Y, learning_rate=0.01, epochs=50000)


data = np.genfromtxt('train.csv', delimiter=',', skip_header=False)
input = data[-1, [1, 2, 7]]
#output = data.T[1][1:]
#input = input/input.max(axis=0)
totalerror = 0
hours = []
predicted_output = []
count = 0
for i in range(len(input)):
    count += 1
    hours.append(count)
    predicted = NN.predict(input[i]) * max
    predicted_output.append(predicted)
    print(predicted)
#    totalerror += abs(predicted - output[i])
#avg_error = totalerror/count
#print("Average error", avg_error)

predicted_output = [x-1722 for x in predicted_output]

trainingpoints = list(range(len(NN.errorlist)))
plt.plot(trainingpoints, NN.errorlist)
plt.ylabel("Error")
plt.xlabel("Training Cycles")
plt.title("Error Convergence During Training")
plt.show()

plt.plot(hours, data.T[1][1:])
plt.plot(hours, predicted_output)
plt.ylabel("BTC Price")
plt.xlabel("Test Data Points")
plt.title("Test Data Results")
plt.show()
'''