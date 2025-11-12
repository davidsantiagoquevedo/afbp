import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par

axinset_ticksize = 15

alphaT = [1, 0.7, 0.5, 0.3, 0.1]
HT = [(2 - a) / 2 for a in alphaT]       

fig, ax = plt.subplots(1, 2, figsize = (10, 5.5))

##########################################################

Tf = 150
h = 0.05
upss = [1, 20]

y0_long = [3, 7e2]
y0_long2 = [0.3, 130]

yloc_long = [40, 8e3]
yloc_long2 = [900, 5e5]

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
            if t==3:
                plot.add_trend(ax[u], x0 = 0, xf = 0.3, y0=5, func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = 3, alpha = at)

        if u==1:
            plot.add_trend(ax[u], x0 = 0.2, xf = 4, y0=700, func = plot.t2, text = fr"$~t^2$", xloc = 0.5, yloc = 8e2)
            Tf_inset=0.2
            h_inset = 0.001
            r = rModulus(alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, Tf=Tf_inset, h=h_inset)
            r.compute_msd_an()
            plot.plot_moment(inset_ax, r, 'msd', 'an', pic_in_grid=True, legend=False)

        plot.add_trend(ax[u], x0 = 15, xf = 150, y0=y0_long[u], func = plot.t, text = fr"$~t$", xloc = 35, yloc = yloc_long[u])
        plot.add_trend(ax[u], x0 = 30, xf = 150, y0=y0_long2[u], func = plot.t2, text = fr"$~t^2$", xloc = 35, yloc = yloc_long2[u])
        
    ax[u].set_title(fr'$\upsilon$={ups}', fontsize = par.title_fontsize)
    ax[u].set_xscale("log")
    ax[u].set_yscale("log")
    ax[u].set_xlim(xmin = h)

inset_ax.set_xscale("log")
inset_ax.set_yscale("log")
inset_ax.set_xlim(xmin = h_inset)
inset_ax.tick_params(axis='both', labelsize=axinset_ticksize)

fig.tight_layout()
fig.savefig(f"plots/paper/rmsd_long_analy_fdt_ups.png", dpi=100)
