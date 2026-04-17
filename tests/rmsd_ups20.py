import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par
import utilities
plt.style.use("src/plotting_style.mplstyle")


alphaR = [1., 0.7, 0.5, 0.3, 0.2]
HR = [(2 - a) / 2 for a in alphaR]   

fig, ax = plt.subplots(figsize=(10,8))


##########################################################

Tf = 7e4
h = 0.5
 
for i, ar in enumerate(alphaR):

    r = rModulus(alpha=ar, H=(2 - ar) / 2, alphaR=0.7, HR=(2 - 0.7) / 2, ups=20, Tf=Tf, h=h)

    r.compute_msd_an()
    color = plot.plot_moment(ax, r, 'msd', 'an_longlim', legend = True, legend_id='alpha')

    # PERSISTENCE TIME
    pers_time = r.calc_persistance_time()
    plot.add_pers_time(ax, pers_time, ymax=1, color = color)
    
    # CROSSOVER TIME
    cross_time = r.calc_crossover_time()
    plot.add_cross_time(ax, cross_time, color = color)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(xmin = h)

handles, legend = ax.get_legend_handles_labels()
ax.get_legend().remove()


#T2 TREND
plot.add_trend(ax, x0 = pers_time, xf = Tf, y0=8e4, func = plot.t, text = fr"$~t$", xloc = 1e4, yloc = 1e9, fontsize=20)
# plot.add_trend(ax, x0 = 0.15, xf = pers_time, y0=1.8e2, func = plot.t2, text = fr"$~t^2$", xloc = 3, yloc = 4e3, fontsize=20)
plot.add_trend(ax, x0 = 0.15, xf = pers_time, y0=1.8e2, func = plot.talpha, text = fr"$~t^{{1.8}}$", xloc = 3, yloc = 4e3, fontsize=20, alpha=1.8)
plot.add_trend(ax, x0 = 0.15, xf = pers_time, y0=1.8e2, func = plot.talpha, text = fr"$~t^{{1.8}}$", xloc = 3, yloc = 4e3, fontsize=20, alpha=1.3)



fig.legend(handles, legend, bbox_to_anchor = (1.3,0.8), ncol = 1)
fig.savefig(f"plots/tests/rmsd_ups20_lpahR0.7.png", dpi=100, bbox_inches='tight')
