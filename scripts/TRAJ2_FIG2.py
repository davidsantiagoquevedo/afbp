import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par
import utilities
from matplotlib.patches import Circle

axis_fontsize = 20

DATA_PATH = 'data'
mode = 'r'
Tf = 100.
h=0.005
realizations = 10
start_set=1
sets=1
L_type = 'L1'

# alphaT = [1., 0.3, 0.1]
alphaT = 0.7
HT = 0.65
alphaR = [1., 0.5, 0.3]
HR = [0.5, 0.75, 0.85]
ups = 1
j = 3

time_sub = [1.4]
time_sup = [12]

hs = [0.005, 0.005, 0.001]
mods = [100, 100, 200]
colors = [par.colors_main[0], par.colors_main[2], par.colors_main[3]]

fig, ax = plt.subplots(figsize=(6, 6))
for i, ar in enumerate(alphaR):
    hr = HR[i]
    h = hs[i]
    mod = mods[i]

    x = utilities.read_env(mode='x',
                            L_type = L_type, 
                            alpha=alphaT, H=HT,
                            alphaR=ar, HR=hr,
                            ups=ups,
                            realizations=realizations,
                            Tf=Tf,
                            h=h, 
                            start_set=start_set,
                            sets=sets,
                            path=DATA_PATH)
    y = utilities.read_env(mode='y',
                            L_type = L_type, 
                            alpha=alphaT, H=HT,
                            alphaR=ar, HR=hr,
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

    # style = par.traj_style[f'{at}']
    # color = par.traj_colors_unique[f'{at}']
    # x_val = x_val + offsets[i][0]
    # y_val = y_val + offsets[i][1]
    
    t = np.linspace(0, 100, len(x_val))
    sc = ax.scatter(x_val, y_val, s=10, c=colors[i], label=f'{ar}')
    
# circle = Circle((0, 0), radius=10, edgecolor='black', facecolor='none', lw=2)
# ax.add_patch(circle)

ax.set_xlabel(r'$x/L_{\alpha}$', fontsize = axis_fontsize)
ax.set_ylabel(r'$y/L_{\alpha}$', fontsize = axis_fontsize)
ax.tick_params(axis='both', labelsize=par.size_ticks)
ax.legend()
ax.set_aspect('equal') 

fig.tight_layout()
fig.savefig(f"plots/paper/traj2_fig2.png", dpi=200, transparent=True)

