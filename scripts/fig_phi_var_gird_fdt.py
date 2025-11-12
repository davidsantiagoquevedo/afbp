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
    analytics = env.compute_var_an(time=np.abs(time-t_ref))


    # Cos Delta phi

    mean_cos_deltaphi =  np.mean(np.cos(matrix_ref), axis=0)
    analytics = np.exp(-analytics/2)

    ax.plot(time, mean_cos_deltaphi, c = color_cos, lw=2)
    ax.plot(time, analytics, c='black', lw=3, ls=":", label = r'$e^{-D_{H_Q}t^{\alpha_Q}}$') 

    ax.tick_params(axis='both', labelsize=par.size_ticks)

##########################################################

legend_fontsize = 15

mode = 'phi'
Tf = 20.
start_set=1
L_type = 'L1'
DATA_PATH = 'data'
eta=1
tref = 12

fig, ax = plt.subplots(1, 2, figsize = (14, 6))

##########################################################

alphaR = [1., 0.7, 0.5, 0.3, 0.1]
HRs = (2-np.array(alphaR))/2
hs = [0.005, 0.005, 0.005, 0.001, 0.0001]
realizationsvec = [1000, 1000, 1000, 1000, 1000]
setsvec = [3, 3, 3, 3, 1]
Tfv = [20., 20., 20., 20., 1.]
# start_setvec = [3, 2, 1, 3, 1]

for a, alphaR in enumerate(alphaR):
    HR = HRs[a]
    h = hs[a]
    realizations = realizationsvec[a]
    sets = setsvec[a]
    Tf = Tfv[a]
    # start_set = start_setvec[a] 

    # MSD
    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    env.compute_var()
    color = plotting.plot_moment(ax[0], env, variable='sim', mom_type='var', legend_id='alpha', pic_in_grid=True)
    # color = par.lighten_color(color, 0.5)
    env.compute_var_an(tl=0)
    plotting.plot_moment(ax[0], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = 'black')

    # COS
    # plot_deltaphicos(ax[1], tref, env, color_cos = color)

ax[0].set_ylabel(fr'$\langle (q(t)-q_0)^2 \rangle$', fontsize = par.axis_fontsize)
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
fig.savefig(f"plots/paper/phi_msd_cos.png", bbox_inches='tight', dpi=100)
