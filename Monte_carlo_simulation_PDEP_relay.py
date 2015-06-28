# Libraries needed

import math
import numpy as np

# Computers are good at generating Uniform distribution of numbers
# So we prefer to transform Uniform distribution to Weibull distribution

def wblg(b,a):
    x = (1./float(b))*((-math.log(np.random.uniform()))**(1./a))
    return x

    