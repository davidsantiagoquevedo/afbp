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

# dynamics = 'fdt'
dynamics = 'ooe'

mode = 'phi'
start_set=1
realizations = 1000
L_type = 'L1'
DATA_PATH = 'data'
m=1e-9
eta=1
tref=5
h = 0.005

def tl(alpha, H, eta=1, m=0.00000001):
    return ((m*H*gamma(2*H))/(eta*(alpha+H-1)*gamma(alpha)*gamma(alpha+2*H-1)))**(1/(4-2*alpha-2*H))

def plot_deltaphivar(ax, t_ref, env, color):
    t_ref_index = int(t_ref/h)

    # Delta phi
    matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()
    var_ref = np.var(matrix_ref, axis=0)
    time = np.arange(0, len(var_ref))*h
    ax.plot(time, var_ref, c = color, lw=2, label = r'$\sigma_{\Delta_{\phi}}^2$')

    analytics = env.compute_var_an(time=np.abs(time-t_ref))
    ax.plot(time, analytics, c=par.lighten_color(color, 0.7), lw=5, ls="--")

    ax.tick_params(axis='both', labelsize=par.size_ticks)

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

    ax.plot(time, mean_cos_deltaphi, c = color_cos, lw=2, label = r'$\langle \cos\Delta \phi \rangle$')
    ax.plot(time, analytics, c=par.lighten_color(color_cos, 0.7), lw=3, ls="--", label = r'$e^{-\sigma^2_{\Delta\phi}/2}$') 

    ax.tick_params(axis='both', labelsize=par.size_ticks)

##########################################################

if dynamics=='fdt':
    sets = 20
    Tf = 20.
    fig, ax = plt.subplots(2, 4, figsize = (17, 8))
    # FDT
    alphaR = [1., 0.7, 0.5, 0.3]
    HR = [[(2 - a) / 2] for a in alphaR]    
else:
    sets = 1
    Tf = 10
    # OOE
    fig, ax = plt.subplots(4, 4, figsize = (20, 18))
    alphaR = [1., 0.7, 0.5, 0.3]
    HR = [[0.8, 0.5, 0.3], [0.8, 0.65, 0.5], [0.85, 0.75, 0.65], [0.95, 0.85, 0.75]]   
    hs = [[0.01, 0.01, 0.005], [0.001, 0.005, 0.001], [0.001, 0.001, 0.001], [0.001, 0.001, 0.001]] 

for i, ar in enumerate(alphaR):

    for j, hr in enumerate(HR[i]):

        if dynamics=='ooe':
            h = hs[i][j]

        env = utilities.read_env(L_type, mode, ar, hr, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
        env.compute_var()
        color = plotting.plot_moment(ax[0][i], env, variable='sim', mom_type='var', pic_in_grid=True)

        color_light = par.lighten_color(color, 0.5)
        tl_value = tl(alpha=ar, H=hr, eta=eta, m=m)
        env.compute_var_an(tl=tl_value)
        plotting.plot_moment(ax[0][i], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color_light)

        plot_deltaphivar(ax[j+1][i], tref, env, color = color)
        plot_deltaphicos(ax[j+1][i], tref, env, color_cos = palette[3])

        ax[j+1][i].legend(fontsize = par.legend_size, loc = 'upper center')

    ax[0][i].set_title(fr'$\alpha_R={ar}$, $H_R={hr}$, $h={h}$', fontsize = par.title_fontsize)
    ax[0][i].legend(fontsize = par.legend_size, loc = 'upper center')
ax[0][0].set_ylabel(r'$\sigma_{\phi}^2$', fontsize = par.axis_fontsize)
fig.tight_layout()
fig.savefig(f"plots/tests/phi_deltaphi_var_grid_fdt_tref{tref}_sets{sets}_h{h}_dyn{dynamics}.png", dpi=300)
