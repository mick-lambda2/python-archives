import numpy as np
import matplotlib.pyplot as plot
from scipy.stats import truncnorm

ivec = np.array([2,4,11])
print(ivec)

ivec = np.array(ivec,ndmin=2).T
print(ivec)
print(ivec.shape)

# UNIFORM FUNCTION
# all values of x are within -1 to 0 (half open interval)
samples = 1200
low = -1
high = 0
x = np.random.uniform(low,high,samples)

# check the above condition
condition = (np.all(x >= -1) and np.all(x < 0))
print(condition)
print(x)
# plot.hist(x)
# plot.show()

# BINOMIAL FUNCTION
x = np.random.binomial(100,0.5,1200)
# plot.hist(x)
# plot.show()

# NORMAL FUNCTION = USE THIS
# NP DOESNT OFFER = UE SCIPY MODULE - bounded in the range [a,b]
a = -2/3.
b = 2/3.
# x = truncnorm(a,b,1,0).rvs(size=1000)
x = truncnorm(a=-2/3., b=2/3., scale=1, loc=0).rvs(size=1000)
# plot.hist(x)
# plot.show()

# ABOVE IS DIFFICULT TO USE = EDIT INSIDE A DEFINED FUNCTION
def truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

X = truncated_normal(mean=0, sd=0.8, low=-0.5, upp=0.5)
s = X.rvs(10000)
# plot.hist(s)
# plot.show()

# MULTIPLE EXAMPLES
X1 = truncated_normal(mean=2, sd=1, low=1, upp=10)
X2 = truncated_normal(mean=5.5, sd=1, low=1, upp=10)
X3 = truncated_normal(mean=8, sd=1, low=1, upp=10)

fig, ax = plot.subplots(3, sharex=True)
ax[0].hist(X1.rvs(10000), normed=True)
ax[1].hist(X2.rvs(10000), normed=True)
ax[2].hist(X3.rvs(10000), normed=True)
# plot.show()

# NOW CREATE THE NEURAL NETWORK
inodes = 3
hnodes = 4
onodes = 2
bound1 = 1/np.sqrt(inodes)
bound2 = 1/np.sqrt(hnodes)

# WEIGHTS MATRIX
X1 = truncated_normal(mean=2, sd=1, low=-bound1, upp=bound1)
X2 = truncated_normal(mean=2, sd=1, low=-bound2, upp=bound2)
wih = X1.rvs((hnodes, inodes))
who = X2.rvs((onodes, hnodes))


