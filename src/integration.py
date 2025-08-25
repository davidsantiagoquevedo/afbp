import types
import numpy as np
from scipy.special import gamma

def convolution(f, g, t):
    """Computes the convolution between an analytical function f(x) and a secondary function
        that can be: another analytical function or a time series (e.a. noise series) 

    Args:
        f (function): main function to convolve
        g (function or ndarray): secondary function to convolve
        t (ndarray): vector with the domain of integration

    Returns:
        ndarray: result of the convolution along the domain t
    """
    N = len(t)
    if isinstance(g, np.ndarray):
        g_eval = g
    elif isinstance(f, types.FunctionType):
        g_eval = g(t)
    dt = t[1] - t[0]
    conv = np.zeros(N)
    for i in range(N):
        dt = t[1] - t[0]
        g_eval_i = g_eval[:i+1] # subset of g(t)
        t_i = t[:i+1] # subset of the time vector

        s = t[i] - t_i
        s[i] = 1e-4 if s[i] == 0 else s[0]

        f_eval = f(s)
        integrand = f_eval * g_eval_i
        conv[i] = np.trapz(integrand, dx = dt)
            
    return conv

def convolution_by_parts(relax_primitive, d2BH, dBH, t):

    conv_bparts = np.zeros(len(t))
    term2 = convolution(relax_primitive, d2BH, t)
    for i in range(len(t)):

        term1 = dBH[0] * relax_primitive(t[i])

        conv_bparts[i] = term1 + term2[i]
            
    return conv_bparts

# def convolution_weights(dBH, t, alpha):
#     dt = t[1] - t[0]
#     N = len(t)
#     conv = np.zeros(N)

#     weights = np.array([
#         ((k+1)**alpha - k**alpha) for k in range(N)
#     ]) * (dt**alpha / gamma(alpha + 1))

#     for n in range(N):
#         conv[n] = np.sum(weights[:n+1][::-1] * dBH[:n+1])

#     return conv

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