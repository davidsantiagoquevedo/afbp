import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities
import plotting_param as par
from matplotlib.offsetbox import AnchoredText
plt.style.use("src/plotting_style.mplstyle")

mode = 'phi'
Tf = 10.
start_set=1
L_type = 'L1'
DATA_PATH = 'data'
eta=1
tref = 5
realizations = 1000

fig, ax = plt.subplots(2, 1, figsize = (6, 8.5), sharex = True)
axins = ax[0].inset_axes([0.15, 0.6, 0.3, 0.3])

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
    try:
        env.t
    except:
        env.t = np.arange(0, env.n)*env.h
    plotting.plot_moment(ax[0], env, variable='an', mom_type='msd', color=par.color_analytic)
    color = plotting.plot_moment(ax[0], env, variable='sim', mom_type='msd', legend = True, legend_id='alphaR',  ci=True,
                         sample = True, sample_size = 41,  sampling_type = 'loglin')
    if alphaR in [0.2, 0.7]:
    ## inset
        env_ther = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h = 0.005, start_set= start_set, sets=1, path = DATA_PATH)
        try:
            env_ther.t
        except:
            env_ther.t = np.arange(0, env_ther.n)*env_ther.h
        plotting.plot_moment(axins, env_ther, variable='an', mom_type='msd',  legend=False, color=par.color_analytic)
        plotting.plot_moment(axins, env_ther, variable='sim', mom_type='msd',  legend=False, color=color)
    # Orientation correlation
    plotting.plot_moment(ax[1], env, variable='an', mom_type='orcorr', color=par.color_analytic,
                         max_value = 1)
    plotting.plot_moment(ax[1], env, variable='sim', mom_type='orcorr', ci=True,
                         sample = True, sample_size = 41,  sampling_type = 'loglin', max_value = 1)    


axins.set_xscale('log')
axins.set_yscale('log')
axins.set_xlim(0.005)

ax[0].set_ylabel(fr'$\langle (\phi(t)-\phi_0)^2 \rangle$')
ax[1].set_ylabel(r'$\langle \boldsymbol{\hat{n}}(t) \cdot \boldsymbol{\hat{n}}(0) \rangle$')
ax[1].set_xlabel(r'$t/\tau_{R}$')

handles, legend = ax[0].get_legend_handles_labels()
ax[0].get_legend().remove()
fig_leg = fig.legend(handles, legend, bbox_to_anchor = (0.95,0.5), ncol = 2, fontsize=14)
#fig_leg.get_frame().set_facecolor('none')
#fig_leg.get_frame().set_edgecolor('none')

plotting.add_caption_letter(ax[0], "(a)", xloc=-0.15, yloc=1.05)
plotting.add_caption_letter(ax[1], "(b)", xloc=-0.15, yloc=1.1)
fig.tight_layout()
fig.savefig(f"plots/paper/fig1.png", bbox_inches='tight', dpi=200, transparent=False)

