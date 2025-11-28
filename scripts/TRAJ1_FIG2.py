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

DATA_PATH = 'data'
mode = 'r'
Tf = 100.
h=0.005
realizations = 10
start_set=1
sets=1
L_type = 'L1'


alphaT = [1., 0.5, 0.3]
HT = [0.5, 0.75, 0.85]
alphaR = alphaT
HR = HT
ups = 1
js = [4, 1, 2]

time_sub = [1.4]
time_sup = [12]

hs = [0.005, 0.005, 0.001]
mods = [100, 100, 200]

offsets = [[15, 8], [-20, 5], [0, 25]]

fig, ax = plt.subplots()
for i, at in enumerate(alphaT):
    ht = HT[i]
    h = hs[i]
    mod = mods[i]
    j = js[i]

    x = utilities.read_env(mode='x',
                            L_type = L_type, 
                            alpha=at, H=ht,
                            alphaR=at, HR=ht,
                            ups=ups,
                            realizations=realizations,
                            Tf=Tf,
                            h=h, 
                            start_set=start_set,
                            sets=sets,
                            path=DATA_PATH)
    y = utilities.read_env(mode='y',
                            L_type = L_type, 
                            alpha=at, H=ht,
                            alphaR=at, HR=ht,
                            ups=ups,
                            realizations=realizations,
                            Tf=Tf,
                            h=h, 
                            start_set=start_set,
                            sets=sets,
                            path=DATA_PATH)

    x_val = x.trajectories[j,:]
    y_val = y.trajectories[j,:]

    x_val=x_val[::mod]
    y_val=y_val[::mod]

    k=10
    n=len(x_val)
    x_val = np.interp(np.arange(n * k), np.arange(n) * k, x_val)
    y_val = np.interp(np.arange(n * k), np.arange(n) * k, y_val)

    x_val = x_val + offsets[i][0]
    y_val = y_val + offsets[i][1]
    
    t = np.linspace(0, 100, len(x_val))
    sc = ax.scatter(x_val, y_val, s=10, c=t, cmap = par.cmap_black, label=f'{at}')
    
cbar = plt.colorbar(sc, ax=ax, orientation='horizontal')
cbar.set_label(r"$t/\tau$")
ax.set_xlabel(r'$x/L_{\alpha}$', fontsize = axis_fontsize)
ax.set_ylabel(r'$y/L_{\alpha}$', fontsize = axis_fontsize)
ax.tick_params(axis='both', labelsize=par.size_ticks)
ax.set_aspect('equal')

fig.tight_layout()
fig.savefig(f"plots/paper/traj1_fig2.png", dpi=200, transparent=True)

