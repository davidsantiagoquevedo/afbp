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
    ax.plot(time, var_ref, lw=2, label = r'$\sigma_{\Delta_{\phi}}^2$')

    var_t = env.compute_var_an(time=time)
    var_tref = env.compute_var_an(time=t_ref)
    analytics = np.abs(var_t-var_tref)
    ax.plot(time, analytics, lw=5, ls='--', label=r'$\sigma_{\phi}$')

    # Cos Delta phi
    
    mean_cos_deltaphi =  np.mean(np.cos(matrix_ref), axis=0)
    analytics = np.exp(-analytics/2)

    ax.plot(time, mean_cos_deltaphi, lw=2, label = r'$\langle \cos\Delta \phi \rangle$')
    ax.plot(time, analytics, lw=3, ls="--", label = r'$e^{-\sigma^2_{\phi}/2}$') 

    ax.tick_params(axis='both', labelsize=par.size_ticks)

fig, ax = plt.subplots()
##########################################################

alphaR = 0.7
HR = 0.8
h = 0.001

env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()

plot_deltaphistat(ax, tref, env, color = palette[0], color_cos=palette[3])
ax.set_title(fr'$H_R$={HR}, h={h}', fontsize = par.title_fontsize)
ax.legend(fontsize = par.legend_size, loc = 'upper center')


ax.set_title(fr'$\alpha_R$=0.7', fontsize = par.title_fontsize)
ax.legend(fontsize = par.legend_size, loc = 'upper center')

fig.tight_layout()
fig.savefig(f"plots/tests/deltaphi_var_cos_alpha{alphaR}_H{HR}.png", dpi=300)
