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
h = 0.0005
ups = 5.

at = 1
ar = 1

r = rModulus(alpha=at, H=(2 - at) / 2, alphaR=ar, HR=(2 - ar) / 2, ups=ups, Tf=Tf, h=h)

color = plot.plot_moment(ax , r, 'msd', 'an_longlim', legend_id='alpha', legend=True, rescale=ups**2, total_msd=False)
color = plot.plot_moment(ax , r, 'msd', 'an_longlim', legend_id='alpha', legend=True, rescale=ups**2, total_msd=True)

pers_time = r.calc_persistance_time()
plot.add_pers_time(ax, pers_time, ymax=1, color = 'black')
pers_time_gamma = pers_time/gamma(1/ar + 1)
plot.add_pers_time(ax, pers_time_gamma, ymax=1, color = 'blue')
rela_time = gamma(2/ar)*pers_time/gamma(1/ar)
plot.add_pers_time(ax, rela_time, ymax=1, color = 'brown')

# CROSSOVER TIME
cross_time = r.calc_crossover_time()
plot.add_cross_time(ax, cross_time, ymax=1, color = 'red')

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(xmin = h)

plot.add_trend(ax, x0 = h, xf = cross_time, h=h, y0=0.01, func = plot.talpha, alpha=ar, text = fr"$~t^{{{ar}}}$", xloc = (h+cross_time)*0.5, yloc = 0.007)
plot.add_trend(ax, x0 = cross_time, xf = pers_time_gamma, y0=0.8, func = plot.t2, text = fr"$~t^2$", xloc = (cross_time+pers_time_gamma)*0.5, yloc = 1e2)
if pers_time != pers_time_gamma:
    plot.add_trend(ax, x0 = pers_time_gamma, xf = pers_time, y0=0.5, func = plot.talpha, text = fr"$~t^{{{2-ar}}}$", xloc = (pers_time_gamma+pers_time)*0.5, yloc = 1e2, alpha=(2-ar))
plot.add_trend(ax, x0 = rela_time, xf = Tf, y0=150, func = plot.t, text = fr"$~t$", xloc = (Tf+pers_time)*0.5, yloc = 2.5e5)

ax.set_ylabel(fr'$\langle (\boldsymbol{{r}}(t)-\boldsymbol{{r}}_0)^2 \rangle/\upsilon^2\tau_R^2$')
ax.set_xlabel(r'$t/\tau_{R}$')
fig.savefig(f"plots/tests/test_regimes{at}_ups{ups}.png", dpi=200, bbox_inches='tight')
