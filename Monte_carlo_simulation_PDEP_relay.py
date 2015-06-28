# Libraries needed

import math
import numpy as np

# Computers are good at generating Uniform distribution of numbers
# So we prefer to transform Uniform distribution to Weibull distribution

# webull Random number generator
def wblg(b,a):
    x = (1./float(b))*((-math.log(np.random.uniform()))**(1./a))
    return x

# Weibull PDF 

def weib(x,n,a):
    return (a * n) * (x*n)**(a - 1) * np.exp(-(x*n)**a)


# Weibull CDF

def qweib(x,n,a):
    return (1-np.exp(-(x*n)**a))




