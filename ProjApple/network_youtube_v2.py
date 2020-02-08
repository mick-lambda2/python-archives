import numpy as np

class NN():

    def __init__(self):
        np.random.seed(1)
        self.weights = 2 * np.random.random((3, 1)) - 1
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    def sigmoid_grad(self, x):
        return x * (1 - x)

    def train(self, train_inputs, train_outputs, iter):
        for iteration in range(iter):
            outputs = self.think(train_inputs)
            error = train_outputs - outputs
            adjustments = np.dot(train_inputs.T, error*self.sigmoid_grad(outputs))
            self.weights +=adjustments

    def think(self, inputs):
        inputs = inputs.astype(float)
        outputs = self.sigmoid(np.dot(inputs,self.weights))
        return outputs


if __name__ == "__main__":
    # Initialize the single neuron neural network
    nn = NN()

    print("Random starting synaptic weights: ")
    print(nn.weights)

    # The training set, with 4 examples consisting of 3
    # input values and 1 output value
    training_inputs = np.array([[0, 0, 1],
                                [1, 1, 1],
                                [1, 0, 1],
                                [0, 1, 1]])

    training_outputs = np.array([[0, 1, 1, 0]]).T

    # Train the neural network
    nn.train(training_inputs, training_outputs, 10000)

    print("Synaptic weights after training: ")
    print(nn.weights)

    A = str(input("Input 1: "))
    B = str(input("Input 2: "))
    C = str(input("Input 3: "))

    print("New situation: input data = ", A, B, C)
    print("Output data: ")
    print(nn.think(np.array([A, B, C])))