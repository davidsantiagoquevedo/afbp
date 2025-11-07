import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import utilities
import plotting_param as par
import seaborn as sns
import colormaps as cmaps
cmap = cmaps.greenorange_6
palette = sns.color_palette([cmap(i) for i in range(cmap.N)])
sns.set_palette(palette)

DATA_PATH = 'data_tests'
# DATA_PATH = 'data_cluster2'
mode = 'r'
L_type = 'L1'
ups = 1
AHT = 1.
total = True
if AHT<1:
    total = False
Tf = 20.
realizations = 1000
start_set=1
sets=1
L_type = 'L1'

rule = 'N'

fig, ax = plt.subplots()

alphaT = 0.5
HT = 0.75
alphaR = 1.
HR = 0.5 

startset_vec = range(1, 20)
h = 0.005

for start_set in startset_vec:

    env = utilities.read_env(L_type=L_type, mode=mode, alpha=alphaT, H=HT, alphaR=alphaR, HR=HR, ups=ups, realizations=realizations,Tf=Tf,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT, rule=rule, path=DATA_PATH)

    env.make_B_H()
    time = env.t
    env.compute_msd()
    ax.plot(time, env.msd, label=f'{start_set} sets')
    env.compute_msd_an(total=total)
    plot.plot_moment(ax, env, variable='an', mom_type='msd', pic_in_grid=True, color = 'black', legend_label=False)
      

fig.savefig(f"plots/tests/testsets_alphaT{alphaT}_HT{HT}_alphaR{alphaR}_HR{HR}_AHT{AHT}_h{h}_Tf{Tf}.png", dpi=100)
