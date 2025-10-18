import numpy as np
from scipy.special import gamma
import sys
sys.path.append("src/")
import integration as it
import world as wd
from importlib import reload
reload(wd)
import matplotlib.pyplot as plt
import utilities
import plotting_param as par

def nt_func(phit):
    nt = np.zeros(len(phit))
    for j in range(len(phit)):
        if j==0:
            nt[j] = np.cos(phit[j])
        else:
            nt[j] = nt[j-1] + np.cos(phit[j])
    return nt


data_path = 'data_tests'
out_path = 'tests'#'var'
mode = 'phi'
L_type = 'L1'
realizations = 1000
Tf = 10
start_set = 1
sets = 1

alphaR = 1.
HR = 0.8

h = 0.05
phi = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path=data_path)

phi.make_B_H()
trajectories = phi.trajectories

# PHI TRAJ
fig, ax = plt.subplots()
for realization in [1, 10, 100, 500, 600]:
    trajectory = trajectories[realization]
    ax.plot(phi.t, trajectory)
ax.set_xlabel('t', fontsize = par.axis_fontsize)
ax.set_ylabel(r'$\phi(t)$', fontsize = par.axis_fontsize)
fig.savefig(f"plots/tests/phi_trajectory_alphaR{alphaR}_HR{HR}_h{h}.png", dpi=500)

# COS PHI TRAJ
fig, ax = plt.subplots()
for realization in [1, 10, 100, 500, 600]:
    trajectory = np.cos(trajectories[realization])
    ax.plot(phi.t, trajectory)
ax.set_xlabel('t', fontsize = par.axis_fontsize)
ax.set_ylabel(r'$\cos\phi(t)$', fontsize = par.axis_fontsize)
fig.savefig(f"plots/tests/cosphi_trajectory_alphaR{alphaR}_HR{HR}_h{h}.png", dpi=500)

trajectory = trajectories[realization]
nt = nt_func(trajectory)
nt_ntminus1  = [nt[j]-nt[j-1] for j in range(1,len(nt))]
fig, ax = plt.subplots()
ax.plot(phi.t, nt/10, label=r'$N(t)/10$')
ax.plot(phi.t[1:], nt_ntminus1, label=r'$N(t)-N(t-1)$')
ax.plot(phi.t, np.cos(trajectory), label=r'$\cos\phi(t)$')
ax.set_xlabel('t', fontsize = par.axis_fontsize)
ax.legend()
# ax.set_ylabel(r'$N(t)$', fontsize = par.axis_fontsize)
fig.savefig(f"plots/tests/Ntphi_trajectory_alphaR{alphaR}_HR{HR}_h{h}.png", dpi=500)
