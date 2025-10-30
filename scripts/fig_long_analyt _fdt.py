import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par

alphaT = [1, 0.7, 0.5, 0.3]
HT = [(2 - a) / 2 for a in alphaT]    
alphaR = [1, 0.7, 0.5, 0.3]
HR = [(2 - a) / 2 for a in alphaR]    

fig, ax = plt.subplots(1, 4, figsize = (20, 5.5))

##########################################################

Tf = 100
h = 0.05
ups = 1

for t, at in enumerate(alphaT):
    ht = HT[t]

    for r, ar in enumerate(alphaR):
        hr = HR[r]

        r = rModulus(alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, Tf=Tf, h=h)

        r.compute_msd_an()
        plot.plot_moment(ax[t], r, 'msd', 'an', pic_in_grid=True, legend_id='alphaR')
        

    ax[t].set_title(fr'$\alpha_T$={at}', fontsize = par.title_fontsize)
    ax[t].set_xscale("log")
    ax[t].set_yscale("log")
    ax[t].set_xlim(xmin = h)

fig.tight_layout()
fig.savefig(f"plots/paper/rmsd_long_analy_fdt.png", dpi=100)
