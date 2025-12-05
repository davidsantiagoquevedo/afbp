import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par
import utilities
plt.style.use("src/plotting_style.mplstyle") 
from matplotlib.gridspec import GridSpec

alpha = [0.7, 0.5, 0.3]
ups = 20.
Tf = 1e4
h = 0.005
h_siminset = [0.005, 0.005, 0.0001]

ymax_cross = [0.4, 0.4, 1]
ymax_pers = [0.6, 0.6, 1]
ymax_pers_gamma = [0.6, 0.6, 1]
ymin_rel = [0,0,0.6]

xloc_sub = [0.006, 0.007, 0.009]
yloc_sub = [0.003, 0.007, 0.02]

xloc_insets = [0.05, 0.16]
yloc_insets = [0.35, 0.65]

xloc_rel = [70, 4e2, 2e3]
yloc_rel = [6e2, 4e3, 9e4]

y0_pers = [0.3, 0.27, 0.2]
y0_relax = [4.5, 6.5, 25]

fig = plt.figure(figsize=(15, 8))

outer = GridSpec(2, 1, height_ratios=[1, 1], figure=fig)
top = outer[0].subgridspec(1, 3) 
bottom = outer[1].subgridspec(1, 3, width_ratios=[1, 0.5, 1.5])

for i, a in enumerate(alpha):

    ax = fig.add_subplot(top[0, i])

    r = rModulus(alpha=a, H=(2 - a) / 2, alphaR=a, HR=(2 - a) / 2, ups=ups, Tf=Tf, h=h)

    plot.plot_moment(ax , r, 'msd', 'an_a', legend=False, rescale=ups**2, total_msd=False)
    plot.plot_moment(ax , r, 'msd', 'an_tot', legend=False, rescale=ups**2, total_msd=True)

    pers_time = r.calc_persistance_time()
    pers_time_gamma = pers_time/gamma(1/a + 1)
    cross_time = r.calc_crossover_time()
    relax_time = gamma(2/a)*(pers_time)/gamma(1/a)

    ax.axvline(x = cross_time, ymax = ymax_cross[i], color = 'gray', lw = 3.5, ls='-')
    ax.axvline(x = pers_time_gamma, ymax = ymax_pers[i], color = 'gray', lw = 3.5, ls='--')
    ax.axvline(x = pers_time, ymax = ymax_pers_gamma[i], color = 'gray', lw = 3.5, ls=':')
    ax.axvline(x = relax_time, ymax = 1, ymin=ymin_rel[i], color = 'gray', lw = 3.5, ls='-.')

    plot.add_trend(ax, x0 = h, xf = cross_time, h=0.005, y0=0.03, func = plot.talpha, alpha=a, text = fr"$~t^{{{a}}}$", xloc = xloc_sub[i], yloc = yloc_sub[i])

    plot.add_trend(ax, x0 = cross_time, xf = pers_time_gamma, y0=y0_pers[i], func = plot.t2, text = fr"$~t^2$", xloc = 2e-1, yloc = 1e-3)

    plot.add_trend(ax, x0 = relax_time, xf = Tf, y0=y0_relax[i], func = plot.t, text = fr"$~t$", xloc = xloc_rel[i], yloc = yloc_rel[i])

    if i==2:
        plot.add_trend(ax, x0 = pers_time_gamma, xf = pers_time, y0=1.4, func = plot.talpha, text = fr"$~t^{{{2-a}}}$", xloc = 1.5, yloc = 2e1, alpha=(2-a))
    else:
    # ANALYTICAL INSETS
        axinset = ax.inset_axes([0.08, 0.59, 0.3, 0.35])

        plot.plot_moment(axinset, r, 'msd', 'an_a', legend=False, rescale=ups**2, total_msd=False)
        plot.plot_moment(axinset, r, 'msd', 'an_tot', legend=False, rescale=ups**2, total_msd=False)
        axinset.axvline(x = pers_time, ymax = 1, color = 'gray', lw = 3.5, ls=':')
        axinset.axvline(x = pers_time_gamma, ymax = 1, color = 'gray', lw = 3.5, ls='--')

        axinset.set_xscale("log")
        axinset.set_yscale("log")
        axinset.set_xlim(pers_time_gamma-pers_time_gamma/10, pers_time+pers_time/10)
        xmin_index = int((pers_time_gamma-pers_time_gamma/10)/r.h)
        xmax_index = int((pers_time+pers_time/3)/r.h)
        axinset.set_ylim(r.msd_an[xmin_index]/ups**2, r.msd_an[xmax_index]/ups**2)

        axinset.tick_params(labelsize=12)
        axinset.tick_params(which='minor', labelbottom=False, labelleft=False)
        
        plot.add_trend(axinset, x0 = pers_time_gamma, xf = pers_time, h=0.001, y0=0.75, func = plot.talpha, text = fr"$~t^{{{2-a}}}$", xloc = (pers_time_gamma+pers_time)/2-xloc_insets[i], yloc = r.msd_an[xmin_index]/ups**2+yloc_insets[i], alpha=(2-a))

    # SIM INSETS
    axinset = ax.inset_axes([0.6, 0.15, 0.35, 0.4])
        
    hsim = h_siminset[i]
    env = utilities.read_env(mode='r',L_type = 'L1', alpha=a, H=(2 - a) / 2, alphaR=a, HR=(2 - a) / 2, ups=ups, realizations=1000, Tf=20., h=hsim, start_set=1, sets=1, path = 'data')
    env.compute_msd()
    plot.plot_moment(axinset, env, 'msd', 'sim', legend_id='alphaR', color=par.colors_main_black[1], legend=False,  ci=True, sample = True, sample_size = 41,  sampling_type = 'loglin', rescale=ups**2)
    env.t = np.arange(0, env.n)*hsim
    env.compute_msd_an(total=True)
    plot.plot_moment(axinset, env, 'msd', 'an_tot', legend = False, rescale=ups**2)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(xmin = h)
    ax.set_yscale("log")
    ax.set_title(rf"$\alpha={a}$")

    if i==0:
        ax.set_ylabel(fr'$\langle (\boldsymbol{{r}}(t)-\boldsymbol{{r}}_0)^2 \rangle/\upsilon^2\tau_R^2$')
    ax.set_xlabel(r'$t/\tau_R$')


ax = fig.add_subplot(bottom[0, 2])
# TRAJECTORIES
hs = [0.005, 0.005, 0.0001]
js = [3, 5, 1]
mods = [10, 10, 10]
ks = [10, 10, 10]
offsets = [[5, 5], [25, -8], [0, 0]]
color_bar = False
for a, alpha  in enumerate([0.7, 0.5, 0.3]):
    y = utilities.read_env(mode='x', L_type = 'L1', alpha=alpha, H=(2 - alpha) / 2, alphaR=alpha, HR= (2 - alpha) / 2, ups=20.,realizations=10, Tf=100., h=hs[a], start_set=1, sets=1, path='data_tests')
    x = utilities.read_env(mode='y', L_type = 'L1', alpha=alpha, H=(2 - alpha) / 2, alphaR=alpha, HR= (2 - alpha) / 2, ups=20.,realizations=10, Tf=100., h=hs[a], start_set=1, sets=1, path='data_tests')
    x_val = x.trajectories[js[a],:]/ups
    y_val = y.trajectories[js[a],:]/ups

    x_val = x_val + offsets[a][0]
    y_val = y_val + offsets[a][1]

    if a==2:
        color_bar=fig

    plot.plot_trajectory(ax, x_val, y_val, mod=mods[a], k=ks[a], fig=color_bar)

ax.text(14, 9, r'$\alpha=0.7$', fontsize = 20)
ax.text(15, -11, r'$\alpha=0.5$', fontsize = 20)
ax.text(0, -7, r'$\alpha=0.3$', fontsize = 20)


ax.set_xlabel(r'$x/\upsilon\tau_R$')
ax.set_ylabel(r'$y/\upsilon\tau_R$')

# fig.legend(handles, legend, bbox_to_anchor = (0.9,1.05), ncol = 5)
fig.savefig(f"plots/paper/fig2_v2.png", dpi=100, bbox_inches='tight')
