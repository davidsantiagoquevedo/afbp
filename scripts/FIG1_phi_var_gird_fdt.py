import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities
import plotting_param as par
from matplotlib.offsetbox import AnchoredText


def plot_deltaphicos(ax, t_ref, env, color_cos):
    t_ref_index = int(t_ref/h)

    # Delta phi
    matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()
    var_ref = np.var(matrix_ref, axis=0)
    time = np.arange(0, len(var_ref))*h
    analytics = env.compute_msd_an(time=np.abs(time-t_ref))

    # Cos Delta phi

    mean_cos_deltaphi =  np.mean(np.cos(matrix_ref), axis=0)
    analytics = np.exp(-analytics/2)

    ax.plot(time, mean_cos_deltaphi, c = color_cos, lw=2)
    style = par.msd_style['an']
    style['c'] = par.color_analytic
    ax.plot(time, analytics, **style) 

    ax.tick_params(axis='both', labelsize=par.size_ticks)

##########################################################

legend_fontsize = 15

mode = 'phi'
Tf = 10.
start_set=1
L_type = 'L1'
DATA_PATH = 'data_tests/data_numba'
eta=1
tref = 5
realizations = 1000

fig, ax = plt.subplots(1, 2, figsize = (14, 6))

##########################################################

# alphaR = [1., 0.7, 0.5, 0.3, 0.1]
alphaR = [1., 0.7, 0.5, 0.3, 0.2]
HRs = (2-np.array(alphaR))/2
hs = [0.005, 0.005, 0.005, 0.001, 5e-5]
setsvec = [3, 3, 3, 3, 1]

for a, alphaR in enumerate(alphaR):
    HR = HRs[a]
    h = hs[a]
    sets = setsvec[a]

    # MSD
    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    env.compute_msd()
    color = plotting.plot_moment(ax[0], env, variable='sim', mom_type='msd', legend_id='alpha', pic_in_grid=True)
    # color = par.lighten_color(color, 0.5)
    env.compute_msd_an(tl=0)
    plotting.plot_moment(ax[0], env, variable='an', mom_type='msd', pic_in_grid=True, legend_label=False, color=par.color_analytic)

    # COS
    plot_deltaphicos(ax[1], tref, env, color_cos = color)

ax[0].set_ylabel(fr'$\langle (r(t)-r_0)^2 \rangle_{{\eta=0}}$', fontsize = par.axis_fontsize)
ax[1].set_ylabel(fr'$\langle \cos\left(\Delta q(t)\right) \rangle$', fontsize = par.axis_fontsize)
ax[0].set_xlabel('t', fontsize = par.axis_fontsize)
ax[1].set_xlabel('t', fontsize = par.axis_fontsize)

handles, legend = ax[0].get_legend_handles_labels()
ax[0].get_legend().remove()
fig.legend(handles, legend, bbox_to_anchor = (0.75,0.99), ncol = 4, fontsize = legend_fontsize)

at = AnchoredText('(a)', prop=dict(size=par.size_labels_figures), frameon=False, loc='upper left')
ax[0].add_artist(at)
at = AnchoredText('(b)', prop=dict(size=par.size_labels_figures), frameon=False, loc='upper left')
ax[1].add_artist(at)

# fig.tight_layout()
fig.savefig(f"plots/paper/phi_msd_cos_numb.png", bbox_inches='tight', dpi=100)
