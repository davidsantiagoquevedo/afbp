import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities
import plotting_param as par
import seaborn as sns
import colormaps as cmaps
cmap = cmaps.greenorange_6
palette = sns.color_palette([cmap(i) for i in range(cmap.N)])
sns.set_palette(palette)

mode = 'phi'
Tf = 10
start_set=1
realizations = 1000
sets = 1
L_type = 'L1'
DATA_PATH = 'data'
m=1e-9
eta=1
tref=5

def tl(alpha, H, eta=1, m=0.00000001):
    return ((m*H*gamma(2*H))/(eta*(alpha+H-1)*gamma(alpha)*gamma(alpha+2*H-1)))**(1/(4-2*alpha-2*H))

def plot_deltaphistat(ax, t_ref, env, color, color_cos):
    t_ref_index = int(t_ref/h)

    # Delta phi
    matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()
    var_ref = np.var(matrix_ref, axis=0)
    time = np.arange(0, len(var_ref))*h
    ax.plot(time, var_ref, c = color, lw=2, label = r'$\sigma_{\Delta_{\phi}}^2$')

    analytics = env.compute_var_an(time=np.abs(time-t_ref))
    ax.plot(time, analytics, c=par.lighten_color(color, 0.7), lw=5, ls="--")

    # Cos Delta phi
    # 
    mean_cos_deltaphi =  np.mean(np.cos(matrix_ref), axis=0)
    analytics = np.exp(-analytics/2)

    ax.plot(time, mean_cos_deltaphi, c = color_cos, lw=2, label = r'$\langle \cos\Delta \phi \rangle$')
    ax.plot(time, analytics, c=par.lighten_color(color_cos, 0.7), lw=3, ls="--", label = r'$e^{-\sigma^2_{\Delta\phi}/2}$') 

    ax.tick_params(axis='both', labelsize=par.size_ticks)

fig, ax = plt.subplots(4, 4, figsize = (20, 18))
##########################################################

alphaR = 1.
hs = [0.01, 0.01, 0.005]

for i, HR in enumerate([0.8, 0.5, 0.3]):
    h = hs[i]

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    env.compute_var()
    color = plotting.plot_moment(ax[0][0], env, variable='sim', mom_type='var', pic_in_grid=True)

    color_light = par.lighten_color(color, 0.5)
    tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
    env.compute_var_an(tl=tl_value)
    plotting.plot_moment(ax[0][0], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color_light)

    plot_deltaphistat(ax[i+1][0], tref, env, color = color, color_cos=palette[3+i])
    ax[i+1][0].set_title(fr'$H_R$={HR}, h={h}', fontsize = par.title_fontsize)
    ax[i+1][0].legend(fontsize = par.legend_size, loc = 'upper center')



ax[0][0].set_title(fr'$\alpha_R$=1', fontsize = par.title_fontsize)
ax[0][0].set_ylabel(r'$\sigma_{\phi}^2$', fontsize = par.axis_fontsize)
ax[0][0].legend(fontsize = par.legend_size, loc = 'upper center')

##########################################################

alphaR = 0.7
hs = [0.001, 0.005, 0.001]

for i, HR in enumerate([0.8, 0.65, 0.5]):
    h = hs[i]

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    env.compute_var()
    color = plotting.plot_moment(ax[0][1], env, variable='sim', mom_type='var', pic_in_grid=True)

    color_light = par.lighten_color(color, 0.5)
    tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
    env.compute_var_an(tl=tl_value)
    plotting.plot_moment(ax[0][1], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color_light)

    plot_deltaphistat(ax[i+1][1], tref, env, color = color, color_cos=palette[3+i])
    ax[i+1][1].set_title(fr'$H_R$={HR}, h={h}', fontsize = par.title_fontsize)
    ax[i+1][1].legend(fontsize = par.legend_size, loc = 'upper center')


ax[0][1].set_title(fr'$\alpha_Q$={alphaR}', fontsize = par.title_fontsize)
ax[0][1].legend(fontsize = par.legend_size, loc = 'upper center')

##########################################################

alphaR = 0.5
hs = [0.001, 0.001, 0.001]

for i, HR in enumerate([0.85, 0.75, 0.65]):
    h = hs[i]
    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    env.compute_var()
    color = plotting.plot_moment(ax[0][2], env, variable='sim', mom_type='var', pic_in_grid=True)

    color_light = par.lighten_color(color, 0.5)
    tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
    env.compute_var_an(tl=tl_value)
    plotting.plot_moment(ax[0][2], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color_light)

    plot_deltaphistat(ax[i+1][2], tref, env, color = color, color_cos=palette[3+i])
    ax[i+1][2].set_title(fr'$H_R$={HR}, h={h}', fontsize = par.title_fontsize)
    ax[i+1][2].legend(fontsize = par.legend_size, loc = 'upper center')


ax[0][2].set_title(fr'$\alpha_Q$={alphaR}', fontsize = par.title_fontsize)
ax[0][2].legend(fontsize = par.legend_size, loc = 'upper center')

##########################################################

alphaR = 0.3
hs = [0.001, 0.001, 0.001]

for i, HR in enumerate([0.95, 0.85, 0.75]):
    h = hs[i]

    # if i == 1:
    #     realizations=1500
    #     sets=2
    # if i == 2:
    #     sets = 10
    #     L_type = 'L2'
    #     realizations = 160

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    env.compute_var()
    color = plotting.plot_moment(ax[0][3], env, variable='sim', mom_type='var', pic_in_grid=True)

    color_light = par.lighten_color(color, 0.5)
    tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
    env.compute_var_an(tl=tl_value)
    plotting.plot_moment(ax[0][3], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color_light)

    plot_deltaphistat(ax[i+1][3], tref, env, color = color, color_cos=palette[3+i])
    ax[i+1][3].set_title(fr'$H_R$={HR}, h={h}', fontsize = par.title_fontsize)
    ax[i+1][3].legend(fontsize = par.legend_size, loc = 'upper center')


ax[0][3].set_title(fr'$\alpha_Q$={alphaR}', fontsize = par.title_fontsize)
ax[0][3].legend(fontsize = par.legend_size, loc = 'upper center')

fig.tight_layout()
fig.savefig(f"plots/tests/phi_deltaphi_var_grid.png", dpi=300)
