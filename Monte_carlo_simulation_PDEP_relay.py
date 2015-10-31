# This is project to evaluate the reliability of BSN
# BSN stands for body sensor network.
# Explanation

import math
import numpy as np


def weib(x, n, a):
    """
    Weibul PMF function
    @param x:
    @param n:
    @param a:
    """
    return (a * n) * (x * n) ** (a - 1) * np.exp(-(x * n) ** a)


def wblg(b, a):
    """
    Weibul Random number generator.
    The below equation transforms the uniform distribution to Weibull
    Note: Computers can generate uniform distribution easily hence the need
          for transformation.

    @param b :
    @param a :
    @return x :
    """
    x = (1. / float(b)) * ((-math.log(np.random.uniform())) ** (1. / a))
    return x


def qweib(x, n, a):
    """
    Weibull CDF function

    @param x:
    @param n:
    @param a:

    """
    return (1 - np.exp(-(x * n) ** a))

# Sample function returning random 1 and 0 with p and p-1 probability
sample = lambda y: np.random.choice([1, 0], p=[y, 1 - y])

# time instances at which we calculate the reliability and check with
# alalytical values
times = [1000, 3000, 6000, 10000]

"""
IFP is a list of isolation factor probablities with (q_RA,q_RC)
q_RA is probability of isolation of component A
q RC is the probability of isolation of component C
"""

IFP = [(1, 1), (0, 0), (1, 0), (0, 1), (0.1, 0.9), (0.1, 0.1), (0, 0)]

# we require these q_RA and q_RC for the seventh case of IFP where the
# q_RA and q_RC are time dependent. Meaning the isolation factor for components
# A and C are time dependent.

q_RA = lambda t: qweib(t, 1e-4, 2.)
q_RC = lambda t: qweib(t, 1e-4, 1.)

# Table to hold the data from iterations
table = []

for index, case in enumerate(IFP):
    Usys = []
    FCE_sys = []
    for t in times:
        if(index == 6):
            qRA = q_RA(t)
            qRC = q_RC(t)
        else:
            (qRA, qRC) = case
        pfge_count = 0
        FCE1_count = 0.
        FCE2_count = 0.
        FCE3_count = 0
        sys = []
        sys_fce1 = []
        sys_fce2 = []
        sys_fce3 = []
        N = 10000
        for i in range(1, N + 1):
        	# probability that the sensor of a component fails
            # shortform probability_Asensor_fails at time t
            t_As = lambda t: qweib(t, 1.5e-4, 1.)
            t_Bs = lambda t: qweib(t, 1.5e-4, 1.)
            t_Cs = lambda t: qweib(t, 1.2e-4, 2.)
            t_Ds = lambda t: qweib(t, 1.2e-4, 2.)
            # sample the sensor failure return 1 or 0
            s_As = sample(t_As(t))
            s_Bs = sample(t_Bs(t))
            s_Cs = sample(t_Cs(t))
            s_Ds = sample(t_Ds(t))
            # probability of transmission of component fails
            t_At = lambda t :qweib(t,2.2e-4,1.)
            t_Bt = lambda t :qweib(t,2.2e-4,1.)
            t_Ct = lambda t :qweib(t,2.0e-4,2.)
            t_Dt = lambda t :qweib(t,2.0e-4,2.)
            # sample the corresponding transmission failure
            # return 1 or 0
            s_At = sample(t_At(t))
            s_Bt = sample(t_Bt(t))
            s_Ct = sample(t_Ct(t))
            s_Dt = sample(t_Dt(t))
            # Propagation failure random time generator
            Ap = wblg(1e-5,2.)
            Bp = wblg(1e-5,2.)
            Cp = wblg(1e-5,2.)
            Dp = wblg(1e-5,2.)
            # Relay failure random time
            R  = wblg(1e-4,1.)
            # probability of propagation failure at time t
            t_Ap = lambda t : qweib(t,1e-5,2.)
            t_Bp = lambda t : qweib(t,1e-5,2.)
            t_Cp = lambda t : qweib(t,1e-5,2.)
            t_Dp = lambda t : qweib(t,1e-5,2.)                          
            # corresponding sample
            # return 1 or 0
            s_Ap = sample(t_Ap(t))
            s_Bp = sample(t_Bp(t))
            s_Cp = sample(t_Cp(t))
            s_Dp = sample(t_Dp(t))

			# relay propagation failure
            rp = lambda t :qweib(t,1e-5,1.)
            # corresponding relay sample
            Rp = sample(rp(t))
            # sampling isolation factors for component A and C
            RA = sample(qRA)
            RC = sample(qRC)
            if(Rp == 1):
                sys.append(1)
                
                pfge_count = pfge_count+1
                Pr_pfge_r = sum(sys)/float(pfge_count)
            else:
                if (R>t):
                    if(s_Ap|s_Bp|s_Cp|s_Dp):
                        #print "FCE2"
                        sys_fce1.append(1)
                        FCE1_count = FCE1_count + 1
                        #print "prop"
                        sys.append(1)
                    else:
                        FCE1_count = FCE1_count + 1
                        sys_fce1.append(((s_As|s_At)&(s_Bs|s_Bt)) | ((s_Cs|s_Ct)&(s_Ds|s_Dt)))
                        sys.append(((s_As|s_At)&(s_Bs|s_Bt)) | ((s_Cs|s_Ct)&(s_Ds|s_Dt)))
                elif(R<t):
                    if(s_Bp|s_Dp):
                        #print "FCE2"
                        sys_fce2.append(1)
                        FCE2_count = FCE2_count + 1
                        #print "prop"
                        sys.append(1)
                    else:
                        if((Ap<R)|(Cp<R)):
                            sys_fce3.append(1)
                            sys.append(1)
                        elif((Ap>R)&(Cp>R)):
                            if(s_At==0):
                                s_At = RA
                            if(s_Ct==0):
                                s_Ct = RC
                        #print 'r'
                            sys_fce3.append(((s_As|s_At)&(s_Bs|s_Bt)) | ((s_Cs|s_Ct)&(s_Ds|s_Dt)))
                            FCE3_count = FCE3_count + 1
                            sys.append(((s_As|s_At)&(s_Bs|s_Bt)) | ((s_Cs|s_Ct)&(s_Ds|s_Dt)))
                        #sys.append(1)
                        else:
                            print "wrong"
            
            
            #fgfg = sum(sys)/10000)   
            if(i==N):
                Usys.append(float(sum(sys))/N)
                FCE_sys.append(( float(sum(sys_fce1))/(sum(sys)-pfge_count),float(sum(sys_fce2))/(sum(sys)-pfge_count),float(sum(sys_fce3))/(sum(sys)-pfge_count)))
                #print float(sum(sys_fce1))/(FCE1_count),float(sum(sys_fce2))/(FCE2_count),float(sum(sys_fce3))/FCE3_count
                #print FCE1_count/t,FCE2_count/t,FCE3_count/t
                #print float(sum(sys))/10000,(float(sum(sys_fce1))/(FCE1_count))*(FCE1_count/t),(float(sum(sys_fce2))/(FCE2_count))*(FCE2_count/t),(float(sum(sys_fce3))/FCE3_count)*(FCE3_count/t)
                #print "------------------"
    
    print Usys
table.append(Usys)
table.append(FCE_sys)
table

