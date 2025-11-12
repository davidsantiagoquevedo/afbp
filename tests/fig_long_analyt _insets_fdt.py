import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par
import utilities

def plot_sim_data(ax, at, ht, ar, hr):
    L_type = 'L1'
    mode = 'r'
    rule = 'N'
    start_set = 1
    realizations = 1000
    AHT = 1.
    DATA_PATH = 'data_tests'
    std = True
    Tf_inset = 20.
    if ar == 0.3:
        sets = 3
        h = 0.001
    else:
        if at==1.:
            sets = 10
        else:
            sets = 19
        h = 0.005

    env = utilities.read_env(L_type=L_type, mode=mode, alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, realizations=realizations,Tf=Tf_inset,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT,  rule=rule, path=DATA_PATH)

    env.compute_msd()
    color = plot.plot_moment(ax, env, variable='sim', mom_type='msd', pic_in_grid=True, legend = False, std=std)
    color = par.lighten_color(color, 0.5)
    env.compute_msd_an()
    plot.plot_moment(ax, env, variable='an', mom_type='msd', pic_in_grid=True, color = color, legend_label=False, legend=False)


alphaT = [1., 0.7, 0.5, 0.3]
HT = [(2 - a) / 2 for a in alphaT]    
alphaR = [1., 0.7, 0.5, 0.3]
HR = [(2 - a) / 2 for a in alphaR]    

title_fontsize = 22
legend_fontsize = 18
legend_position = 'upper center'
axis_fontsize = 22
axinset_ticksize = 11

sub_y0 = [1.17, 1.4, 1.3, 1.4]

fig, ax = plt.subplots(1, 4, figsize = (26, 7))

##########################################################

Tf = 100
h = 0.05
ups = 1

y0_sub = [1.4, 1.9, 2.2, 2.6] 
y0_long = [4, 3.3, 3, 3] 
y0_long2 = [0.7, 0.5, 0.5, 0.5] 
yloc_sub = [0.07, 0.2, 0.4, 0.8]
yloc_long = [90, 80, 80, 80]
yloc_long2 = [2.5e3, 2e3, 2e3, 2e3]

for t, at in enumerate(alphaT):
    ht = HT[t]

    inset_ax = ax[t].inset_axes([0.1, 0.52, 0.45, 0.45])  

    for r, ar in enumerate(alphaR):
        hr = HR[r]

        renv = rModulus(alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, Tf=Tf, h=h)

        renv.compute_msd_an()
        plot.plot_moment(ax[t], renv, 'msd', 'an', pic_in_grid=True, legend=True, legend_id='alphaR')

        handles, legend = ax[t].get_legend_handles_labels()
        ax[t].get_legend().remove()
    
        # Simulation data
        plot_sim_data(inset_ax, at=at, ht=ht, ar=ar, hr=hr)

        # Trens
        if r==0:
            plot.add_trend(ax[t], x0 = 0, xf = 0.3, y0=y0_sub[t], func = plot.talpha, text = fr"$~t^{{{at}}}$", xloc = 0.1, yloc = yloc_sub[t], alpha = at, fontsize=axis_fontsize)
            plot.add_trend(ax[t], x0 = 15, xf = 100, y0=y0_long[t], func = plot.t, text = fr"$~t$", xloc = 35, yloc = yloc_long[t], fontsize=axis_fontsize)
            plot.add_trend(ax[t], x0 = 15, xf = 100, y0=y0_long2[t], func = plot.t2, text = fr"$~t^2$", xloc = 35, yloc = yloc_long2[t], fontsize=axis_fontsize)



    ax[t].set_title(fr'$\alpha_T$={at}', fontsize = title_fontsize)
    ax[t].set_xscale("log")
    ax[t].set_yscale("log")
    ax[t].set_xlim(xmin = h)
    ax[t].set_xlabel('t', fontsize = axis_fontsize)
    ax[0].set_ylabel(par.ylabel_map['msd_r'], fontsize = axis_fontsize)

    inset_ax.tick_params(axis='both', labelsize=axinset_ticksize)
    inset_ax.grid(ls=':')



fig.legend(handles, legend, bbox_to_anchor = (0.99,0.7), ncol = 1, fontsize = legend_fontsize)
# fig.tight_layout()
fig.savefig(f"plots/paper/rmsd_long_analy_fdt.png", dpi=100)
