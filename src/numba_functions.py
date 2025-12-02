import numba
from numba import njit
from scipy.special import gamma
import numpy as np

@njit
def run_one_phi(n, phi0, cnj, coeff_noise, dB):
    traj = np.ones(n) * phi0

    for time in range(1, n):
        sum_term = 0.0
        for i in range(1, time):
            sum_term += cnj[time - i] * (traj[i] - traj[i - 1])
        traj[time] = traj[time - 1] + coeff_noise * dB[time] - sum_term

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
        
        traj[time] = traj[time-1] + coeff_noise * dB[time] - sum_x + ups[time]*sum_phi + ups[time]*(nt[time]-nt[time-1])

    return traj

