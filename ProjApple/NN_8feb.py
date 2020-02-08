import numpy as np
import pandas as pd


data = pd.read_csv('training_inputs.csv')
print(data)

data = data.sample(frac=1).reset_index(drop=True)
print(data)

train_data = data.head(12)
test_data = data.tail(4)
print(train_data)
print('hello')
print(test_data)

train_inputs = train_data.drop(['Output'],axis=1).values
train_outputs = train_data.drop(['A','B','C','D'],axis=1).values
print(train_inputs)

# df = train_inputs.values
# print(df)


# for i in df:
#     print('value: ', i)

class NN():
    def __init__(self):
        self.w1 = 2 * np.random.random((4, 4)) - 1
        self.w2 = 2 * np.random.random((4, 1)) - 1

    def sigmoid(self, x):
        return 1 / (1+np.exp(-x))

    def sigmoid_grad(self, x):
        return x*(1-x)

    def process(self, input):
        predict_output = []
        for i in range(len(input)):
            input1 = input[i]
            out1 = self.sigmoid(np.dot(input1.T, self.w1))
            out2 = self.sigmoid(np.dot(out1, self.w2))
            predict_output.append(out2)
        return np.array(predict_output)

    def train(self, train_input, actual_output, iter):
        # for i in range(iter):
        x = 5
        predict_output = self.process(train_input)
        error = np.subtract(actual_output, predict_output)
        # print(actual_output)
        # print('hhh')
        # print(predict_output)
        # print(error)
        adjust = np.dot(train_input.T, error*self.sigmoid_grad(predict_output))
        print(adjust)








network = NN()
# print(network.w1)
# print(network.w2)
# print(type(df[0]))
output = network.process(train_inputs)
network.train(train_inputs, train_outputs, 50)
# print(output)





