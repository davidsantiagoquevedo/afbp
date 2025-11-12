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

DATA_PATH = 'data_tests'
mode = 'r'
Tf = 100.
h=0.001
realizations = 10
start_set=1
sets=1
L_type = 'L1'
AHT=1.
ups=1.
rule='N'

alphaT = [0.3]
HT = [0.85]
alphaR = alphaT
HR = HT
color_index = [0, 1, 2]
j = 5

time_sub = [1.4]
time_sup = [12]

fig, ax = plt.subplots()
u=0
for t, at in enumerate(alphaT):
    ht = HT[t]

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

    print(len(x_val))

    mod = 100
    x_val=x_val[::mod]
    y_val=y_val[::mod]
    print(len(x_val))


    k=10
    n=len(x_val)
    x_val = np.interp(np.arange(n * k), np.arange(n) * k, x_val)
    y_val = np.interp(np.arange(n * k), np.arange(n) * k, y_val)
    t = np.linspace(0, 100, len(x_val))

    sub = int(time_sub[u]/(mod*h))*k
    sup = int(time_sup[u]/(mod*h))*k
    colors = par.traj_colors[f'{at}']
    segments = [(0, sub, colors[0]), (sub, sup, colors[1]), (sup, n*k, colors[3])]

    for start, end, col in segments:
        print(start, end)
        ax.scatter(x_val[start:end], y_val[start:end], s=3, color=col)



fig.savefig(f"plots/paper/trajectory_periods.png", dpi=100)

