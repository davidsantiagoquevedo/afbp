import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par
import utilities
from matplotlib import colormaps
from mpl_toolkits.mplot3d import Axes3D
import colormaps as cmaps
from matplotlib.colors import ListedColormap
import parallelization

axis_fontsize = 20

DATA_PATH = 'data_tests'
mode = 'r'
Tf = 100.
h=0.01
realizations = 10
start_set=1
sets=1
L_type = 'L1'
AHT=1.
rule='N'

alphaT = [1., 0.3, 0.1]
# alphaT = [1.]
HT = [0.5, 0.85, 0.95]
alphaR = alphaT
HR = HT
upss = [1.]
j = 1

time_sub = [1.4]
time_sup = [12]

hs = [0.01, 0.01, 0.01]
mods = [30, 30, 30]

fig, ax = plt.subplots(1, 2, figsize = (16, 8))
for u, ups in enumerate(upss):
    for t, at in enumerate(alphaT):
        ht = HT[t]
        h = hs[t]
        mod = mods[t]

        x = utilities.read_env(mode='x',
                                L_type = L_type, 
                                alpha=at, H=ht,
                                alphaR=at, HR=ht,
                                ups=ups,
                                AHT=AHT,
                                realizations=realizations,
                                Tf=Tf,
                                h=h, hR=h,
                                start_set=start_set,
                                sets=sets,
                                rule=rule,
                                path=DATA_PATH)
        y = utilities.read_env(mode='y',
                                L_type = L_type, 
                                alpha=at, H=ht,
                                alphaR=at, HR=ht,
                                ups=ups,
                                AHT=AHT,
                                realizations=realizations,
                                Tf=Tf,
                                h=h, hR=h,
                                start_set=start_set,
                                sets=sets,
                                rule=rule,
                                path=DATA_PATH)

        x_val = x.trajectories[j,:]
        y_val = y.trajectories[j,:]

        x_val=x_val[::mod]
        y_val=y_val[::mod]

        k=10
        n=len(x_val)
        x_val = np.interp(np.arange(n * k), np.arange(n) * k, x_val)
        y_val = np.interp(np.arange(n * k), np.arange(n) * k, y_val)
        t = np.linspace(0, 100, len(x_val))

        style = par.traj_style[f'{at}']
        color = par.traj_colors_unique[f'{at}']
        sc = ax[u].scatter(x_val, y_val, color=color)

    ax[u].set_xlabel('x', fontsize = axis_fontsize)
    ax[0].set_ylabel('y', fontsize = axis_fontsize)
    ax[u].tick_params(axis='both', labelsize=par.size_ticks)



fig.tight_layout()
fig.savefig(f"plots/paper/trajectories.png", dpi=100)

