import numba
from numba import njit
from scipy.special import gamma
import numpy as np

@njit
def run_one_numba(n, phi0, cnj_array, h, alpha, coeff_noise, dB):
    traj = np.ones(n) * phi0

    for time in range(1, n):
        sum_term = 0.0
        for i in range(1, time):
            sum_term += cnj_array[time - i] * (traj[i] - traj[i - 1])
        traj[time] = traj[time - 1] + coeff_noise * dB[time] - sum_term

    return traj