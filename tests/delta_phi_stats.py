import sys
sys.path.append("src/")
import utilities
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

DATA_PATH = 'data_tests'

mode = 'phi'
L_type = 'L1'
alpha = 0.5
H = 0.75
realizations = 1000
Tf = 10
h = 0.001
sets = 1
start_set=1
kBT = 1

t_ref = 5
t_ref_index = int(t_ref/h)

env = utilities.read_env(L_type, mode, alpha, H, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)

matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()

var_ref = np.var(matrix_ref, axis=0)
time = np.arange(0, len(var_ref))*h
analytics = env.compute_var_an(time=np.abs(time-t_ref))
env.compute_var()

fig, ax = plt.subplots()
ax.plot(time, env.var, label = 'var')
ax.plot(time, env.var_an, label = 'var_an')
ax.plot(time, var_ref, label = 'sim')
ax.plot(time, analytics, label='analy')
ax.legend()
fig.savefig(f"plots/tests/delta_phi_var.png", dpi=100)


mean_cos_deltaphi =  np.mean(np.cos(matrix_ref), axis=0)
# analytics = np.exp(-var_ref/2)
analytics = np.exp(-analytics/2)

fig, ax = plt.subplots()
ax.plot(time, mean_cos_deltaphi, label = 'sim')
ax.plot(time, analytics, label='analy')
fig.savefig(f"plots/tests/delta_cos_phi_var.png", dpi=100)