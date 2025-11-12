import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par

axinset_ticksize = 15
legend_fontsize = 17
axis_fontsize = 20

alphaT = [1, 0.7, 0.5, 0.3, 0.1]
# alphaT = [1, 0.7, 0.5, 0.3]
HT = [(2 - a) / 2 for a in alphaT]       

fig, ax = plt.subplots(1, 2, figsize = (10, 5.5))

##########################################################

Tf = 150
h = 0.05
upss = [1, 20]

y0_long = [3.7, 9.9e2]
y0_long2 = [0.5, 180]

yloc_long = [70, 2e4]
yloc_long2 = [1.6e3, 6.5e5]

x_pointsub = [1.4, 1e-1]
y_pointsub = [5, 5]
x_pointsup = [12, 1e1]
y_pointsup = [55, 1.5e4]

for u, ups in enumerate(upss):

    if u==1:
        inset_ax = ax[u].inset_axes([0.57, 0.08, 0.4, 0.4])  

    for t, at in enumerate(alphaT):
        ht = HT[t]

        ar = at
        hr = ht

        r = rModulus(alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, Tf=Tf, h=h)

        r.compute_msd_an()
        plot.plot_moment(ax[u], r, 'msd', 'an', pic_in_grid=True, legend_id='alphaR')

        if u==0:
            if t==0:
                plot.add_trend(ax[u], x0 = 0, xf = 0.3, y0=1.5, func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = 0.1, alpha = at)
            if t==4:
                plot.add_trend(ax[u], x0 = 0, xf = 0.3, y0=5, func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = 5, alpha = at)

        if u==1:
            plot.add_trend(ax[u], x0 = 0.2, xf = 4, y0=650, func = plot.t2, text = fr"$~t^2$", xloc = 0.5, yloc = 5.5e2)

            Tf_inset=0.2
            h_inset = 0.001
            r = rModulus(alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, Tf=Tf_inset, h=h_inset)
            r.compute_msd_an()
            plot.plot_moment(inset_ax, r, 'msd', 'an', pic_in_grid=True, legend=False)
            # if t==0:
            #     plot.add_trend(inset_ax, x0 = 0, xf = 1e-2, y0=1.8, func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = 0.1, alpha = at)
            # if t==4:
            #     plot.add_trend(inset_ax, x0 = 0, xf = 1e-2, y0=5.5, func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = 6, alpha = at)

        plot.add_trend(ax[u], x0 = 23, xf = 150, y0=y0_long[u], func = plot.t, text = fr"$~t$", xloc = 35, yloc = yloc_long[u])
        plot.add_trend(ax[u], x0 = 30, xf = 150, y0=y0_long2[u], func = plot.t2, text = fr"$~t^2$", xloc = 35, yloc = yloc_long2[u])

    handles, legend = ax[u].get_legend_handles_labels()
    ax[u].get_legend().remove()
        
    ax[u].set_title(fr'$\upsilon$={ups}', fontsize = par.title_fontsize)
    ax[u].set_xscale("log")
    ax[u].set_yscale("log")
    ax[u].set_xlim(xmin = h)

    ax[u].scatter(x_pointsub[u], y_pointsub[u], marker='*', s=280, c='black')
    ax[u].scatter(x_pointsup[u], y_pointsup[u], marker='D', s=150, c='black')

    ax[u].set_xlabel('t', fontsize = axis_fontsize)
    ax[0].set_ylabel(par.ylabel_map['msd_r'], fontsize = axis_fontsize)

inset_ax.set_xscale("log")
inset_ax.set_yscale("log")
inset_ax.set_xlim(xmin = h_inset)
inset_ax.tick_params(axis='both', labelsize=axinset_ticksize)

fig.legend(handles, legend, bbox_to_anchor = (0.9,0), ncol = 5, fontsize = legend_fontsize)
# fig.tight_layout()
fig.savefig(f"plots/tests/rmsd_long_analy_fdt_ups.png", dpi=100, bbox_inches='tight')
