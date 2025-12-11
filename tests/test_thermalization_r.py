import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import utilities
from matplotlib.offsetbox import AnchoredText


mode = 'r'
Tf = 100.0
Tth = 70.0

L_type = 'L1'
DATA_PATH = 'data_tests'
eta=1
h = 0.001
realizations = 1000
start_set=1
sets = 1
ups = 1

alphaR = 0.3
HR = (2-alphaR)/2
alphaT = alphaR
HT = HR


##########################################################

env = utilities.read_env(mode=mode,
                        L_type = L_type, 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        ups=1,
                        realizations=realizations,
                        Tf=Tf,
                        Tth=Tth,
                        h=h,
                        start_set=start_set,
                        sets=sets,
                        path = DATA_PATH)


env_th = utilities.read_env(mode=mode,
                        L_type = L_type, 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        ups=1,
                        realizations=realizations,
                        Tf=Tf,
                        Tth=Tth,
                        h=h,
                        start_set=start_set,
                        sets=sets,
                        path = DATA_PATH)

env_th.Tth = 70
thermal_index = int(env_th.Tth/env_th.h)

env_th.trajectories = env_th.trajectories[:,thermal_index:]
env_th.n = env_th.trajectories.shape[1]
env_th.t = np.linspace(0, env_th.Tf-env_th.Tth, env_th.n)

env_th.trajectories.shape
env.trajectories.shape

env_th.compute_msd()
env_th.compute_msd_an()
env.compute_msd()
env.compute_msd_an()


fig, axes = plt.subplots(1,3, figsize = (15,7))
ax = axes[0]
ax.plot(env.t, env.msd)
ax.fill_between(env.t, env.msd_lower_ci, env.msd_upper_ci, alpha = 0.5)
ax.plot(env.t, env.msd_an, color='black', ls='--')
ax.set_xscale('log')
ax.set_yscale('log')
#ax.set_xlim(70)
ax.set_xlim(env.h)


ax = axes[1]
ax.plot(env.t[thermal_index:], env.msd[thermal_index:])
ax.fill_between(env.t[thermal_index:], env.msd_lower_ci[thermal_index:], env.msd_upper_ci[thermal_index:], alpha = 0.5)
ax.plot(env.t[thermal_index:], env.msd_an[thermal_index:], color='black', ls='--')
ax.set_xscale('log')
ax.set_yscale('log')


ax = axes[2]
ax.plot(env_th.t, env_th.msd)
ax.fill_between(env_th.t, env_th.msd_lower_ci, env_th.msd_upper_ci, alpha = 0.5)
ax.plot(env_th.t, env_th.msd_an, color='black', ls='--')
#ax.set_xscale('log')
#ax.set_yscale('log')
fig.tight_layout()
fig.savefig(f"plots/tests/thermalization_r_{alphaR}.png")

