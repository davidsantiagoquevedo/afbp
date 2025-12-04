import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par
import utilities
from scipy.special import gamma
plt.style.use("src/plotting_style.mplstyle")


fig, ax = plt.subplots() 

##########################################################

Tf = 1e4
h = 0.05
ups = 20.

at = 0.5
ar = 0.5

r = rModulus(alpha=at, H=(2 - at) / 2, alphaR=ar, HR=(2 - ar) / 2, ups=ups, Tf=Tf, h=h)

color = plot.plot_moment(ax , r, 'msd', 'an_longlim', legend_id='alpha', legend=True, rescale=ups**2, total_msd=False)
color = plot.plot_moment(ax , r, 'msd', 'an_longlim', legend_id='alpha', legend=True, rescale=ups**2, total_msd=True)

pers_time = r.calc_persistance_time()
plot.add_pers_time(ax, pers_time, ymax=1, color = 'black')
pers_time_gamma = pers_time/gamma(1/ar + 1)
plot.add_pers_time(ax, pers_time_gamma, ymax=1, color = 'blue')

# CROSSOVER TIME
cross_time = r.calc_crossover_time()
plot.add_cross_time(ax, cross_time, ymax=1, color = 'red')

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(xmin = h)

plot.add_trend(ax, x0 = pers_time, xf = Tf, y0=1, func = plot.t, text = fr"$~t$", xloc = 7e2, yloc = 2e2)
plot.add_trend(ax, x0 = pers_time, xf = Tf, y0=150, func = plot.t, text = fr"$~t$", xloc = 7e2, yloc = 2.5e5)
plot.add_trend(ax, x0 = cross_time, xf = pers_time_gamma, y0=0.8, func = plot.t2, text = fr"$~t^2$", xloc = 1e1, yloc = 1e2)
plot.add_trend(ax, x0 = pers_time_gamma, xf = pers_time, y0=0.5, func = plot.talpha, text = fr"$~t^{{{2-ar}}}$", xloc = 1e1, yloc = 1e2, alpha=(2-ar))
# plot.add_trend(ax, x0 = 0, xf = cross_time, h=0.01, y0=0.15, func = plot.talpha, alpha=0.2, text = fr"$~t^{{{0.2}}}$", xloc = 0.06, yloc = 0.007)

ax.set_ylabel(fr'$\langle (\boldsymbol{{r}}(t)-\boldsymbol{{r}}_0)^2 \rangle/\upsilon^2\tau_R^2$')
ax.set_xlabel(r'$t/\tau_{R}$')
fig.savefig(f"plots/tests/test_regimes{at}_ups{ups}.png", dpi=200, bbox_inches='tight')
