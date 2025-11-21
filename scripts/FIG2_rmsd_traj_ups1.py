import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par
import utilities

axinset_ticksize = 15
legend_fontsize = 17
axis_fontsize = 20

alphaR = [1., 0.7, 0.5, 0.3, 0.2]
HR = [(2 - a) / 2 for a in alphaR]   

h_inset =  [0.005, 0.005, 0.005, 0.0005, 0.0005]   

fig, ax = plt.subplots(2, 2, figsize = (15, 12))
inset_ax = [ax[0][0].inset_axes([0.1, 0.57, 0.4, 0.4]), 
            ax[1][0].inset_axes([0.1, 0.54, 0.4, 0.4])]   

y0_long = [2.4, 2.3]
y0_long2 = [0.3, 0.4]
yloc_long = [43, 47]
yloc_long2 = [40, 40]

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
        color = plot.plot_moment(ax[row][0] , r, 'msd', 'an', pic_in_grid=True, legend_id='alphaR')

        # INSETS
        # if row == 0 and i!=4 and i!=1:
        #     hsim = h_inset[i]
        #     env = utilities.read_env(mode='r',L_type = 'L1', alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, realizations=1000, Tf=20., h=hsim, start_set=1, sets=3, path = 'data_tests')

        #     env.compute_msd()
        #     plot.plot_moment(inset_ax[0], env, 'msd', 'sim', legend_id='alphaR', std=True, color=color, legend=False)
        #     env.compute_msd_an(total=True)
        #     plot.plot_moment(inset_ax[0], env, 'msd', 'an', color='black', legend = False)
        # TRENDS
        if row==0:
            if i==0:
                plot.add_trend(ax[row][0], x0 = 0, xf = 0.3, y0=2.5, func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = 0.15, alpha = at)
            if i==4:
                plot.add_trend(ax[row][0], x0 = 0, xf = 0.3, y0=6, func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = 4.7, alpha = at)

    plot.add_trend(ax[row][0], x0 = 15, xf = 150, y0=y0_long[row], func = plot.t, text = fr"$~t$", xloc = 35, yloc = yloc_long[row])
    plot.add_trend(ax[row][0], x0 = 30, xf = 150, y0=y0_long2[row], func = plot.t2, text = fr"$~t^2$", xloc = 35, yloc = yloc_long2[row])
        

    ax[row][0].set_xscale("log")
    ax[row][0].set_yscale("log")
    ax[row][0].set_xlim(xmin = h)

    handles, legend = ax[row][0].get_legend_handles_labels()
    ax[row][0].get_legend().remove()

    inset_ax[row].tick_params(axis='both', labelsize=13)

    ax[row][0].set_ylabel(par.ylabel_map['msd_r'], fontsize = par.axis_fontsize)
    ax[row][0].set_xlabel('t', fontsize = par.axis_fontsize)

fig.legend(handles, legend, bbox_to_anchor = (0.75,0.95), ncol = 5, fontsize = legend_fontsize)
fig.savefig(f"plots/paper/rmsd_traj_ups1.png", dpi=100, bbox_inches='tight')
