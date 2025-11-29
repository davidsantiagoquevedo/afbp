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

alpha = [1., 0.7, 0.5, 0.3, 0.2]

h_inset =  [0.005, 0.005, 0.005, 0.0001, 0.0005]   
sets_inset = [3,3,3,1,1]

fig, ax = plt.subplots(2, 2, figsize = (15, 12))
inset_ax = [ax[0][0].inset_axes([0.1, 0.57, 0.4, 0.4]), 
            ax[1][0].inset_axes([0.1, 0.54, 0.4, 0.4])]   

y0_long = [2.4, 2.3]
y0_long2 = [0.55, 0.7]
yloc_long = [70, 70]
yloc_long2 = [3e3, 4e3]

##########################################################

Tf = 200
h = 0.05
ups = 5

for row in range(2):

    for column in range(2):

        for i, a in enumerate(alpha):

            if column == 0:
                at = 0.7 if row==0 else 0.3
                ar = a
            else:
                ar = 0.7 if row==0 else 0.3
                at = a

            r = rModulus(alpha=at, H=(2 - at) / 2, alphaR=ar, HR=(2 - ar) / 2, ups=ups, Tf=Tf, h=h)

            r.compute_msd_an()
            color = plot.plot_moment(ax[row][column] , r, 'msd', 'an', pic_in_grid=True, legend_id='alphaR')

        # INSETS
        # if row == 0 and i!=4 and i!=1:
        #     hsim = h_inset[i]
        #     env = utilities.read_env(mode='r',L_type = 'L1', alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, realizations=1000, Tf=20., h=hsim, start_set=1, sets=sets_inset[i], path = 'data')

        #     env.compute_msd()
        #     plot.plot_moment(inset_ax[0], env, 'msd', 'sim', legend_id='alphaR', std=True, color=color, legend=False)
        #     env.compute_msd_an(total=True)
        #     plot.plot_moment(inset_ax[0], env, 'msd', 'an', color='black', legend = False)
            
        # if row == 1 and i!=4 and i!=1:
        #     hsim = h_inset[i]
        #     env = utilities.read_env(mode='r',L_type = 'L1', alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, realizations=1000, Tf=20., h=hsim, start_set=1, sets=sets_inset[i], path = 'data')

        #     env.compute_msd()
        #     plot.plot_moment(inset_ax[1], env, 'msd', 'sim', legend_id='alphaR', std=True, color=color, legend=False)
        #     env.compute_msd_an(total=True)
        #     plot.plot_moment(inset_ax[1], env, 'msd', 'an', color='black', legend = False)
        # TRENDS
        # if row==0:
        #     if i==0:
        #         plot.add_trend(ax[row][0], x0 = 0, xf = 0.3, y0=2.5, func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = 0.15, alpha = at)
        #     if i==4:
        #         plot.add_trend(ax[row][0], x0 = 0, xf = 0.3, y0=6, func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = 4.7, alpha = at)
        # if row==1 and at==0.7 and ar==0.7:
        #         plot.add_trend(ax[row][0], x0 = 0, xf = 0.3, y0=6, func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = 2, alpha = at)
            

    # plot.add_trend(ax[row][0], x0 = 30, xf = Tf, y0=y0_long[row], func = plot.t, text = fr"$~t$", xloc = 60, yloc = yloc_long[row])
    # # plot.add_trend(ax[row][0], x0 = 30, xf = Tf, y0=y0_long2[row], func = plot.t2, text = fr"$~t^2$", xloc = 35, yloc = yloc_long2[row])
    # plot.add_trend(ax[row][0], x0 = 30, xf = Tf, y0=y0_long2[row], func = plot.talpha, text = fr"$~t^{{{1.8}}}$", xloc = 60, yloc = yloc_long2[row], alpha=1.8)  

        ax[row][column].set_xscale("log")
        ax[row][column].set_yscale("log")
        ax[row][column].set_xlim(xmin = h)

        handles, legend = ax[row][column].get_legend_handles_labels()
        ax[row][column].get_legend().remove()

    inset_ax[row].tick_params(axis='both', labelsize=13)

    ax[row][0].set_ylabel(par.ylabel_map['msd_r'], fontsize = par.axis_fontsize)

ax[1][0].set_xlabel(r'$t/\tau_{\alpha}$', fontsize = par.axis_fontsize)

fig.legend(handles, legend, bbox_to_anchor = (0.75,0.95), ncol = 5, fontsize = legend_fontsize)
fig.savefig(f"plots/paper/fig3.png", dpi=200, bbox_inches='tight')
