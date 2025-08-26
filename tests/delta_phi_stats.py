import sys
sys.path.append("src/")
import utilities
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

mode = 'phi'
alpha = 0.5
H = (2-alpha)/2
realizations = 1200
Tf = 10
h = 0.01
sets = 5
kBT = 1

t_ref = 5
t_ref_index = int(t_ref/h)

env = utilities.read_env(mode, alpha, H, sets, Tf, h, realizations)

matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()

var_ref = np.var(matrix_ref, axis=0)
time = np.arange(0, len(var_ref))*h
analytics = (2*kBT/(gamma(alpha+1)))*np.abs(time-t_ref)**(alpha)

fig, ax = plt.subplots()
ax.plot(time, var_ref, label = 'sim')
ax.plot(time, analytics, label='analy')
fig.savefig(f"plots/tests/delta_phi_var.png", dpi=100)


mean_cos_deltaphi =  np.mean(np.cos(matrix_ref), axis=0)
analytics = np.exp(-var_ref/2)

fig, ax = plt.subplots()
ax.plot(time, mean_cos_deltaphi, label = 'sim')
ax.plot(time, analytics, label='analy')
fig.savefig(f"plots/tests/delta_cos_phi_var.png", dpi=100)