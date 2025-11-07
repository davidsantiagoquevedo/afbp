
import sys
sys.path.append("src/")
import utilities
import plotting 
import matplotlib.pyplot as plt
import numpy as np
from world import Angular, xDirection, yDirection
from matplotlib import colormaps
import parallelization


DATA_PATH = 'data_tests'
mode = 'r'
L_type = 'L1'
ups=1
AHT=1.
realizations = 2
batch_size = 2
Tf = 50.
start_set = 1
sets = 1
rule = 'N'

h = 0.05
hR = 0.05

alphaT = 0.3
HT = 0.85
alphaR = 0.3
HR = 0.85


phi = Angular(realizations=realizations, alpha=alphaR, H=HR, Tf=Tf, h=hR, L_type=L_type)
phi.run()

x = xDirection(phi=phi, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h, ups=ups, AHT=AHT, rule=rule, L_type=L_type)
# x.run()
x = parallelization.run_trajectories_parallel(x, batch_size)


y = yDirection(phi=phi, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h, ups=ups, AHT=AHT, rule=rule, L_type=L_type)
# y.run()
y = parallelization.run_trajectories_parallel(y, batch_size)


fig, ax = plt.subplots(1, 2, figsize=(15,6))
for i in range(realizations):

    x_val = x.trajectories[i,:]
    y_val = y.trajectories[i,:]
    k=10
    n=len(x_val)
    x_val = np.interp(np.arange(n * k), np.arange(n) * k, x_val)
    y_val = np.interp(np.arange(n * k), np.arange(n) * k, y_val)
    t = np.linspace(0, 100, len(x_val))

    sc = ax[i].scatter(x_val, y_val, s=3, c=t,  cmap=colormaps['summer'])

fig.tight_layout()
fig.colorbar(sc, ax=ax, label='t')
fig.savefig(f"plots/tests/r_ensamble.png", dpi=100)
