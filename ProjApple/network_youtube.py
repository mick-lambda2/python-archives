import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_grad(x):
    return x*(1-x)

training_inputs = np.array([[0, 0, 1],
                           [1, 1, 1],
                           [1, 0, 1],
                           [0, 1, 1]])

# default np array is row, thus transpose for column
actual_outputs = np.array([[0,1,1,0]]).T

# initialize weights
np.random.seed(1)

# 3x1 matrix. we have 3 inputs and 1 output
# rand values -1 to 1 and mean 0
synaptic_weights = 2*np.random.random((3,1)) - 1
print('random starting weights: ')
print(synaptic_weights)

# main loop
# 1 iter for no BP mode! just guessing first output
for iteration in range(50000):
    input_layer = training_inputs

    # outputs = weighted sum then through sigmoid function
    outputs = sigmoid(np.dot(input_layer,synaptic_weights))

    error = actual_outputs - outputs

    adjustments = error*sigmoid_grad(outputs)

    # why is it +=? thought it would be refreshed
    synaptic_weights += np.dot(input_layer.T, adjustments)

    print('weights after training: ')
    print(synaptic_weights)

print('outputs after training: ')
print(outputs)
