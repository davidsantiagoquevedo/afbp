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

h_siminset =  [0.005, 0.005, 0.005, 0.0001, 0.0005]   
sets_inset = [3,3,3,1,1]

fig, ax = plt.subplots(2, 2, figsize = (15, 12))

rescales = [1, 400]

y0_long = [2.4, 2]
yloc_long = [4e3, 3e3]

ymax_pers = [0.55, 0.65]

siminset_size = [0.3, 0.27]
siminset_ypos = [0.65, 0.7]
y0_inset = [[2, 7], [3, 6.3]]
yloc_inset = [[0.003, 3], [0.003, 2]]
xloc_insets = [0.005, 0.002]
Tf_insets = [3, 0.1]
xf_insets = [0.1, 0.01]

##########################################################

Tf = 7e4
h = 0.5
ups_vec = [1, 20.]


for column in range(2):
    ups = ups_vec[column]
    
    siminset_ax = ax[0][column].inset_axes([0.1, siminset_ypos[column], siminset_size[column], siminset_size[column]])
    siminset_ax.tick_params(labelsize=15)
    aninset_ax = ax[0][column].inset_axes([0.6, 0.07, 0.35, 0.35])
    aninset_ax.tick_params(labelsize=15)
    index_inset = 0
    for i, ar in enumerate(alphaR):

        r = rModulus(alpha=ar, H=(2 - ar) / 2, alphaR=ar, HR=(2 - ar) / 2, ups=ups, Tf=Tf, h=h)

        r.compute_msd_an()
        color = plot.plot_moment(ax[0][column], r, 'msd', 'an_longlim', legend = True, legend_id='alpha', rescale = rescales[column])

        # INSETS SIM
        if i!=4 and i!=1:
            hsim = h_siminset[i]
            env = utilities.read_env(mode='r',L_type = 'L1', alpha=ar, H=(2 - ar) / 2, alphaR=ar, HR=(2 - ar) / 2, ups=ups, realizations=1000, Tf=20., h=hsim, start_set=1, sets=1, path = 'data')

            env.compute_msd()
            plot.plot_moment(siminset_ax, env, 'msd', 'sim', legend_id='alphaR', color=color, legend=False,  ci=True, sample = True, sample_size = 41,  sampling_type = 'loglin', rescale=rescales[column])
            env.t = np.arange(0, env.n)*hsim
            env.compute_msd_an(total=True)
            plot.plot_moment(siminset_ax, env, 'msd', 'an', color=par.color_analytic, legend = False, rescale=rescales[column])
        
        # INSETS AN
        Tf_inset=Tf_insets[column]
        h_inset = 0.001
        rins = rModulus(alpha=ar, H=(2 - ar) / 2, alphaR=ar, HR=(2 - ar) / 2, ups=ups, Tf=Tf_inset, h=h_inset)
        rins.compute_msd_an()
        plot.plot_moment(aninset_ax, rins, 'msd', 'an_longlim', legend=False)
        if i==0 or i==4:
            text = fr"$~t$" if i==0 else fr"$~t^{{{ar}}}$"
            plot.add_trend(aninset_ax, x0 = h_inset, xf = xf_insets[column], y0=y0_inset[column][index_inset], h = h_inset, func = plot.talpha, text = text, xloc = xloc_insets[column], yloc = yloc_inset[column][index_inset], alpha = ar, fontsize=17)
            index_inset+=1

        # PERSISTENCE TIME
        pers_time = r.calc_persistance_time()
        plot.add_pers_time(ax[0][column], pers_time, ymax=ymax_pers[column], color = color)
        
        # CROSSOVER TIME
        cross_time = r.calc_crossover_time()
        plot.add_cross_time(aninset_ax, cross_time, color = color)

    #T TRENDS    
    plot.add_trend(ax[0][column], x0 = pers_time, xf = Tf, y0=y0_long[column], h=h, func = plot.t, text = fr"$~t$", xloc = 5e3, yloc = yloc_long[column], fontsize=20)
    plot.add_trend(ax[0][column], x0 = pers_time, xf = Tf, y0=1.3e2, h=h, func = plot.t, text = fr"$~t$", xloc = 5e3, yloc = 1.5e6, fontsize=20)
    
    ax[0][column].set_xscale("log")
    ax[0][column].set_yscale("log")
    ax[0][column].set_xlim(xmin = h)

    handles, legend = ax[0][column].get_legend_handles_labels()
    ax[0][column].get_legend().remove()
    
    aninset_ax.set_xscale("log")
    aninset_ax.set_yscale("log")
    aninset_ax.set_xlim(xmin = h_inset)

#T2 TREND
plot.add_trend(ax[0][1], x0 = 0.15, xf = pers_time, y0=0.5, func = plot.t2, text = fr"$~t^2$", xloc = 15, yloc = 2.5e2, fontsize=20)
ax[1][1].remove()

# TRAJECTORIES
hs = [0.005, 0.005, 0.0001]
js = [4, 1, 1]
mods = [10, 10, 400]
ks = [10, 10, 10]
offsets = [[18, 18], [-25, 15], [0, 30]]
color_bar = False
for a, alpha  in enumerate([1., 0.5, 0.3]):
    x = utilities.read_env(mode='x', L_type = 'L1', alpha=alpha, H=(2 - alpha) / 2, alphaR=alpha, HR= (2 - alpha) / 2, ups=1,realizations=10, Tf=100., h=hs[a], start_set=1, sets=1, path='data')
    y = utilities.read_env(mode='y', L_type = 'L1', alpha=alpha, H=(2 - alpha) / 2, alphaR=alpha, HR= (2 - alpha) / 2, ups=1,realizations=10, Tf=100., h=hs[a], start_set=1, sets=1, path='data')
    x_val = x.trajectories[js[a],:]
    y_val = y.trajectories[js[a],:]

    x_val = x_val + offsets[a][0]
    y_val = y_val + offsets[a][1]

    if a==2:
        color_bar=fig

    plot.plot_trajectory(ax[1][0], x_val, y_val, mod=mods[a], k=ks[a], fig=color_bar)

ax[1][0].text(12, 36, r'$\alpha=1$', fontsize = 20)
ax[1][0].text(-25, 27.5, r'$\alpha=0.5$', fontsize = 20)
ax[1][0].text(-12, 25, r'$\alpha=0.3$', fontsize = 20)


ax[1][0].set_xlabel(r'$x/\upsilon\tau_R$')
ax[1][0].set_ylabel(r'$y/\upsilon\tau_R$')

ax[0][0].set_ylabel(fr'$\langle (\boldsymbol{{r}}(t)-\boldsymbol{{r}}_0)^2 \rangle/\upsilon^2\tau_R^2$')
ax[0][0].set_xlabel(r'$t/\tau_R$')
ax[0][1].set_xlabel(r'$t/\tau_{R}$')

fig.legend(handles, legend, bbox_to_anchor = (0.9,1.05), ncol = 5)
fig.savefig(f"plots/paper/rmsd_traj_ups1.png", dpi=100, bbox_inches='tight')
