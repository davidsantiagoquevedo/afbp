import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities
import plotting_param as par
from matplotlib.offsetbox import AnchoredText

legend_fontsize = 15

mode = 'phi'
Tf = 10.
start_set=1
L_type = 'L1'
DATA_PATH = 'data'
eta=1
tref = 5
realizations = 1000

fig, ax = plt.subplots(1, 2, figsize = (14, 6))

##########################################################

alphaR_ = [1., 0.7, 0.5, 0.3, 0.2]
HRs = (2-np.array(alphaR_))/2
hs = [0.005, 0.005, 0.005, 0.001, 5e-5]
setsvec = [3, 3, 3, 3, 1]

for a, alphaR in enumerate(alphaR_):
    HR = HRs[a]
    h = hs[a]
    sets = setsvec[a]

    # MSD
    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    plotting.plot_moment(ax[0], env, variable='an', mom_type='msd', pic_in_grid=True, legend_label=False, color=par.color_analytic)
    plotting.plot_moment(ax[0], env, variable='sim', mom_type='msd', legend_id='alpha', pic_in_grid=True, ci=True,
                         sample = True, sample_size = 41,  sampling_type = 'loglin')
    # Orientation correlation
    plotting.plot_moment(ax[1], env, variable='an', mom_type='orcorr', pic_in_grid=True, legend_label=False, color=par.color_analytic, max_value = 0.5)
    plotting.plot_moment(ax[1], env, variable='sim', mom_type='orcorr', legend_id='alpha', pic_in_grid=True, ci=True,
                         sample = True, sample_size = 41,  sampling_type = 'loglin', max_value = 0.5)    




ax[0].set_ylabel(fr'$\langle (r(t)-r_0)^2 \rangle_{{\upsilon=0}}/L_{{\alpha}}^{2}$', fontsize = par.axis_fontsize)
ax[1].set_ylabel(r'$\langle \hat{n}(t) \cdot \hat{n}(0) \rangle$', fontsize = par.axis_fontsize)
ax[0].set_xlabel(r'$t/\tau_{\alpha}$', fontsize = par.axis_fontsize)
ax[1].set_xlabel(r'$t/\tau_{\alpha}$', fontsize = par.axis_fontsize)

handles, legend = ax[0].get_legend_handles_labels()
ax[0].get_legend().remove()
ax[1].get_legend().remove()
fig_leg = fig.legend(handles, legend, bbox_to_anchor = (0.85,1.1), ncol = 5, fontsize = legend_fontsize)
fig_leg.get_frame().set_facecolor('none')
fig_leg.get_frame().set_edgecolor('none')

at = AnchoredText('(a)', prop=dict(size=par.size_labels_figures), frameon=False, loc='upper left')
ax[0].add_artist(at)
at = AnchoredText('(b)', prop=dict(size=par.size_labels_figures), frameon=False, loc='upper left')
ax[1].add_artist(at)
fig.tight_layout()
fig.savefig(f"plots/paper/phi_msd_cos_numb_trasp.png", bbox_inches='tight', dpi=100, transparent=False)

