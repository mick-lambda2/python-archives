import numpy as np
from scipy.stats import truncnorm
import matplotlib.pyplot as plot
from scipy.special import expit as activ_fn


class NeuralNetwork:
    def __init__(self,inodes,onodes,hnodes,learn_rate):
        # MAIN INPUTS TO CLASS - others like the boundaries are extrapolations
        self.inodes = inodes
        self.onodes = onodes
        self.hnodes = hnodes
        self.learn_rate = learn_rate
        self.create_wmatrix()

    # always pass self into def fn of a class
    def create_wmatrix(self):
        bound1 = 1 / np.sqrt(self.inodes)
        bound2 = 1 / np.sqrt(self.hnodes)

        # WEIGHTS MATRIX -- THIS COULD ALL BE INSIDE INIT FUNCTION
        # self means we can use wih and who elsewhere now
        Xih = truncated_normal(mean=2, sd=1, low=-bound1, upp=bound1)
        Xho = truncated_normal(mean=2, sd=1, low=-bound2, upp=bound2)
        self.wih = Xih.rvs((self.hnodes, self.inodes))
        self.who = Xho.rvs((self.onodes, self.hnodes))

    def train(self):
        pass

    def run(self, ivec):
        # TURN IVEC INTO COLUMN VECTOR
        ivec =np.array(ivec,ndmin=2).T
        # STAGE 1
        ovec = np.dot(self.wih,ivec)
        ovec = activ_fn(ovec)
        # STAGE 2 - FINAL OUTPUT
        ovec = np.dot(self.who,ovec)
        ovec = activ_fn(ovec)
        return ovec


def truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


# LOOK AT SIGMOID FUNCTION - now same as activ_fn(x)
def sigma(x):
    return 1/(1+np.exp(-x))

X = np.linspace(-5,5,100)
print(X)

plot.plot(X,sigma(X),'b')
plot.xlabel('X Axis')
plot.ylabel('Y Axis')
plot.title('Sigmoid Function')
plot.grid()
plot.text(4,0.8,r'$\sigma(x)=\frac{1}{1+e^{-x}}$',fontsize=16)
plot.show()

# MAIN LOOP - CREATE THE NEURAL NETWORK
inodes = 3
hnodes = 4
onodes = 2
ivec = [1,3,5]
nwork = NeuralNetwork(inodes,onodes,hnodes,0.1)
# print(nwork.wih)
# print(nwork.who)

# RUN THE NETWORK WITH INITIAL WEIGHTS IN IVEC
output = nwork.run(ivec)
