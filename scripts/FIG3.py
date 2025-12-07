import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par
import utilities
plt.style.use("src/plotting_style.mplstyle")


alpha = [1., 0.7, 0.5, 0.3, 0.2]

fig, ax = plt.subplots(2, 1, figsize = (6, 8.5), sharex = True) 
inset_ax = [ax[0].inset_axes([0.10, 0.6, 0.33, 0.33]), ax[1].inset_axes([0.6, 0.2, 0.33, 0.33])]

y0_long = [2.4, 2.3]
y0_long2 = [0.55, 0.7]
yloc_long = [70, 70]
yloc_long2 = [3e3, 4e3]

ymax_pers02 = [0.8, 0.5]

##########################################################

Tf = 1e4
h = 0.005
ups = 5.

h_sim = 0.001

for column in range(2):


    for i, a in enumerate(alpha):

        if column == 0:
            at = 0.7 
            ar = a
        else:
            ar = 0.7
            at = a

        r = rModulus(alpha=at, H=(2 - at) / 2, alphaR=ar, HR=(2 - ar) / 2, ups=ups, Tf=Tf, h=h)

        r.compute_msd_an()
        legend_id = 'alphaR' if column==0 else 'alphaT'
        color = plot.plot_moment(ax[column] , r, 'msd', 'an', legend_id=legend_id, legend=True, rescale=ups**2)

    # INSETS
        if i!=4 and i!=1:
            hinset = h_sim
            if i==3:
                hinset=0.0001

            env = utilities.read_env(mode='r', L_type = 'L1', alpha=at, H=(2 - at) / 2, alphaR=ar, HR=(2 - ar) / 2, ups=ups, realizations=1000, Tf=20., h=hinset, start_set=1, sets=1, path = 'data_tests')

            env.compute_msd()
            plot.plot_moment(inset_ax[column], env, 'msd', 'sim', color=par.colors_main_black[1], legend=False,  ci=True, sample = True, sample_size = 41,  sampling_type = 'loglin', rescale=ups**2)
            env.t = np.arange(0, env.n)*env.h
            env.compute_msd_an(total=True)
            plot.plot_moment(inset_ax[column], env, 'msd', 'an', color=color, legend = False, rescale=ups**2)

            if column==1:
            #     inset_ax[column].set_xlim(h, 0.1)
            #     inset_ax[column].set_ylim(0, 0.1)

                inset_ax[column].set_xscale("log")
                inset_ax[column].set_yscale("log")
                inset_ax[column].set_xlim(xmin = 0.005)

        pers_time = r.calc_persistance_time()
        if i==3:
            perstime03 = pers_time
        ymax_pers = ymax_pers02[column] if i==4 else 0.5
        color_pers = color if column==0 else 'gray'
        ax[column].axvline(x = pers_time, ymax = ymax_pers, color = color_pers, lw = 4, ls=':')

        # CROSSOVER TIME
        cross_time = r.calc_crossover_time()
        color_cross= 'gray' if column==0 else color
        ymax_cross = 0.3 if column==0 else 0.4
        ax[column].axvline(x = cross_time, ymax = ymax_cross, color = color_cross, lw = 4, ls='-')

    ax[column].set_xscale("log")
    ax[column].set_yscale("log")
    ax[column].set_xlim(xmin = h)

    if column==0:
        plot.add_trend(ax[0], x0 = perstime03, xf = Tf, y0=1, func = plot.t, text = fr"$~t$", xloc = 7e2, yloc = 2e2)
        plot.add_trend(ax[0], x0 = pers_time, xf = Tf, y0=150, func = plot.t, text = fr"$~t$", xloc = 7e2, yloc = 2.5e5)
        plot.add_trend(ax[0], x0 = h, xf = cross_time, h=0.01, y0=0.1, func = plot.talpha, alpha=0.7, text = fr"$~t^{{{0.7}}}$", xloc = 0.04, yloc = 0.003)
        plot.add_trend(ax[0], x0 = perstime03, xf = pers_time, y0=1, func = plot.talpha, text = fr"$~t^{{1.8}}$", xloc = 2e1, yloc = 7e2, alpha=1.8)
    else:
        plot.add_trend(ax[1], x0 = pers_time, xf = Tf, y0=4, func = plot.t, text = fr"$~t$", xloc = 1e2, yloc = 8e2)
        plot.add_trend(ax[1], x0 = h, xf = cross_time, h=0.01, y0=0.3, func = plot.talpha, alpha=0.2, text = fr"$~t^{{{0.2}}}$", xloc = 0.02, yloc = 0.3)
        plot.add_trend(ax[1], x0 = h, xf = cross_time, h=0.003, y0=0.1, func = plot.t, text = fr"$~t$", xloc = 0.02, yloc = 0.0008)


ax[0].set_ylabel(fr'$\langle (\boldsymbol{{r}}(t)-\boldsymbol{{r}}_0)^2 \rangle/\upsilon^2\tau_R^2$')
ax[1].set_ylabel(fr'$\langle (\boldsymbol{{r}}(t)-\boldsymbol{{r}}_0)^2 \rangle/\upsilon^2\tau_R^2$')


ax[1].set_xlabel(r'$t/\tau_{R}$')
# ax[1].set_xlabel(r'$t/\tau_{\alpha}$')
ax[0].set_title(r'$\alpha_T=0.7$')
ax[1].set_title(r'$\alpha_R=0.7$')

ax[0].legend(loc = 'lower right', fontsize=14)
ax[1].legend(loc = 'upper left', fontsize=14)
plot.add_caption_letter(ax[0], '(a)', xloc=-0.15, yloc=1.05)
plot.add_caption_letter(ax[1], '(b)', xloc=-0.15, yloc=1.05)

fig.savefig(f"plots/paper/fig3.png", dpi=200, bbox_inches='tight')
