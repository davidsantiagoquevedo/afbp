import numba
from numba import njit
from scipy.special import gamma
import numpy as np

@njit
def run_one_phi_L1(n, phi0, cnj, coeff_noise, dB):

    traj = np.ones(n) * phi0

    for time in range(1, n):
        sum_term = 0.0
        for i in range(1, time):
            sum_term += cnj[time - i] * (traj[i] - traj[i - 1])

        traj[time] = traj[time - 1] + coeff_noise * dB[time] - sum_term

    return traj

@njit
def precompute_ab(n, alpha):
    a = np.zeros(n)
    b = np.zeros(n)

    for l in range(n):
        a[l] = (l+1)**(1-alpha) - l**(1-alpha)
        b[l] = (1/(2-alpha)) * ((l+1)**(2-alpha) - l**(2-alpha)) \
               - 0.5 * ((l+1)**(1-alpha) + l**(1-alpha))
    return a, b

@njit
def precompute_c(n, a, b):

    c = np.zeros((n, n))

    for j in range(n):
        for s in range(j+1):
            k = j - s

            if j <= 1:
                if k == 0:
                    c[j, s] = a[0] + b[0] + b[1]
                elif k == 1:
                    c[j, s] = a[1] - b[1] - b[0]

            elif j == 2:
                if k == 0:
                    c[j, s] = a[0] + b[0]
                elif k == 1:
                    c[j, s] = a[1] + b[1] + b[2] - b[0]
                elif k == 2:
                    c[j, s] = a[2] - b[2] - b[1]

            else:  # j >= 3
                if k == 0:
                    c[j, s] = a[0] + b[0]
                elif 1 <= k <= j-2:
                    c[j, s] = a[k] + b[k] - b[k-1]
                elif k == j-1:
                    c[j, s] = a[j-1] + b[j-1] + b[j] - b[j-2]
                elif k == j:
                    c[j, s] = a[j] - b[j] - b[j-1]

    return c

@njit
def run_one_phi_L2(n, phi0, c, coeff_noise_arr, dB):

    traj = np.ones(n) * phi0

    for time in range(1, n):

        c0 = c[time, time]

        sum_term = 0.0
        for s in range(1, time):
            sum_term += c[time, s] * (traj[s] - traj[s-1])
 
        traj[time] = traj[time-1] + coeff_noise_arr[time] * dB[time] - sum_term / c0

    return traj


@njit
def nxt_func(phit, h):
    nt = np.zeros(len(phit))
    for j in range(len(phit)):
        if j==0:
            nt[j] = np.cos(phit[j])*h
        else:
            nt[j] = nt[j-1] + np.cos(phit[j])*h
    return nt
@njit
def nyt_func(phit, h):
    nt = np.zeros(len(phit))
    for j in range(len(phit)):
        if j==0:
            nt[j] = np.sin(phit[j])*h
        else:
            nt[j] = nt[j-1] + np.sin(phit[j])*h
    return nt
@njit
def run_one(n, ups, nt, cnj, coeff_noise, dB, traj0=0):

    traj = np.ones(n) * traj0

    for time in range(1, n):

        sum_x = 0.0
        for i in range(1, time): 
            sum_x += cnj[time - i] * (traj[i] - traj[i-1])
        
        sum_phi = 0.0
        for i in range(1, time):
            sum_phi += cnj[time - i] * (nt[i]-nt[i-1]) 
        
        traj[time] = traj[time-1] + coeff_noise * dB[time] - sum_x + ups*sum_phi + ups*(nt[time]-nt[time-1])

    return traj

@njit
def run_one_L2(n, ups, nt, c, coeff_noise_arr, dB, traj0=0):

    traj = np.ones(n) * traj0

    for time in range(1, n):

        sum_x = 0.0
        for i in range(1, time): 
            sum_x += c[time, i] * (traj[i] - traj[i-1])
        
        sum_phi = 0.0
        for i in range(1, time):
            sum_phi += c[time, i] * (nt[i]-nt[i-1]) 
        
        traj[time] = traj[time-1] + coeff_noise_arr[time] * dB[time] - sum_x + ups*sum_phi + ups*(nt[time]-nt[time-1])

    return traj
