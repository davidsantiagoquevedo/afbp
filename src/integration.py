import types
import numpy as np
from scipy.special import gamma

def cnj(k, alpha):
    return (k+1)**(alpha) - k**(alpha)

def convolution_weights(dBH, t, alpha):
    dt = t[1] - t[0]
    N = len(t)
    conv = np.zeros(N)

    for time in range(1, N):
            
            # Sum term
            sum_term = 0
            for i in range(1, time+1):
                
                sum_term += cnj(time-i, alpha) * (dBH[i-1] + dBH[i])/2

            conv[time] = (dt**alpha)*sum_term/gamma(alpha+1)

    return conv