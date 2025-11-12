import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par

axinset_ticksize = 15
legend_fontsize = 17
axis_fontsize = 20

alphaR = [1, 0.7, 0.5, 0.3]
HR = [(2 - a) / 2 for a in alphaR]       

fig, ax = plt.subplots(2, 2, figsize = (15, 12))
inset_ax = [ax[0][0].inset_axes([0.1, 0.57, 0.4, 0.4]), ax[1][0].inset_axes([0.1, 0.54, 0.4, 0.4])]   

##########################################################

Tf = 150
h = 0.05
ups = 1

for row in range(2):


    for i, ar in enumerate(alphaR):
        hr = HR[i]

        if row == 0:
            # T=R   
            at = ar
            ht = hr
        else:
            at = 0.7
            ht = 0.65

        r = rModulus(alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, Tf=Tf, h=h)

        r.compute_msd_an()
        plot.plot_moment(ax[row][0] , r, 'msd', 'an', pic_in_grid=True, legend_id='alphaR')

        # inset
        Tf_inset=0.2
        h_inset = 0.001
        r = rModulus(alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, Tf=Tf_inset, h=h_inset)
        r.compute_msd_an()
        plot.plot_moment(inset_ax[row], r, 'msd', 'an', pic_in_grid=True, legend=False)

    ax[row][0].set_xscale("log")
    ax[row][0].set_yscale("log")

    ax[row][0].set_xlim(xmin = h)

    handles, legend = ax[row][0].get_legend_handles_labels()
    ax[row][0].get_legend().remove()


fig.legend(handles, legend, bbox_to_anchor = (0.75,0.95), ncol = 5, fontsize = legend_fontsize)
fig.savefig(f"plots/paper/rmsd_traj_ups1.png", dpi=100, bbox_inches='tight')
