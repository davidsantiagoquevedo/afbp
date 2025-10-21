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
t_ref=1

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

fig, ax = plt.subplots(3, 4, figsize = (22, 14))
##########################################################

alphaR = 1.
hs = [0.01, 0.01, 0.005]

for i, HR in enumerate([0.8, 0.5, 0.3]):
    h = hs[i]
    t_ref_index = int(t_ref/h)

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()
    env.trajectories = matrix_ref
    for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
        plotting.plot_pdf(ax[i][0], env, mode, time=t, tref = t_ref, legend=False, xy_label=False)

    ax[i][0].set_title(fr'$\alpha_R=1, H_R$={HR}, h={h}', fontsize = par.title_fontsize)
    ax[i][0].set_ylabel(rf'$P(\Delta \phi,t)$', fontsize=par.axis_fontsize)

ax[2][0].set_xlabel(rf'$\Delta \phi$', fontsize=par.axis_fontsize)
ax[0][0].legend(fontsize = par.legend_size, loc = 'upper right')

##########################################################

alphaR = 0.7
hs = [0.001, 0.005, 0.001]

for i, HR in enumerate([0.8, 0.65, 0.5]):
    h = hs[i]
    t_ref_index = int(t_ref/h)

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()
    env.trajectories = matrix_ref
    for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
        plotting.plot_pdf(ax[i][1], env, mode, time=t, tref = t_ref, legend=False, xy_label=False)

    ax[i][1].set_title(fr'$\alpha_R={alphaR}, H_R$={HR}, h={h}', fontsize = par.title_fontsize)

ax[2][1].set_xlabel(rf'$\Delta \phi$', fontsize=par.axis_fontsize)

# ##########################################################

alphaR = 0.5
hs = [0.001, 0.001, 0.001]
for i, HR in enumerate([0.85, 0.75, 0.65]):
    h = hs[i]
    t_ref_index = int(t_ref/h)

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()
    env.trajectories = matrix_ref
    for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
        plotting.plot_pdf(ax[i][2], env, mode, time=t, tref = t_ref, legend=False, xy_label=False)

    ax[i][2].set_title(fr'$\alpha_R={alphaR}, H_R$={HR}, h={h}', fontsize = par.title_fontsize)

ax[2][2].set_xlabel(rf'$\Delta \phi$', fontsize=par.axis_fontsize)


# ##########################################################

alphaR = 0.3
hs = [0.001, 0.001, 0.001]

for i, HR in enumerate([0.95, 0.85, 0.75]):
    h = hs[i]
    t_ref_index = int(t_ref/h)

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()
    env.trajectories = matrix_ref
    for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
        plotting.plot_pdf(ax[i][3], env, mode, time=t, tref = t_ref, legend=False, xy_label=False)

    ax[i][3].set_title(fr'$\alpha_R={alphaR}, H_R$={HR}, h={h}', fontsize = par.title_fontsize)

ax[2][3].set_xlabel(rf'$\Delta \phi$', fontsize=par.axis_fontsize)

fig.tight_layout()
fig.savefig(f"plots/tests/deltaphi_pdfs_grid.png", dpi=300)
