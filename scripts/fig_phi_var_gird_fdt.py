import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities
import plotting_param as par

mode = 'phi'
Tf = 10
start_set=1
L_type = 'L1'
DATA_PATH = 'data'
eta=1

fig, ax = plt.subplots(figsize=(6.5, 5))

##########################################################

alphaR = [1., 0.7, 0.5, 0.3]
HRs = (2-np.array(alphaR))/2
hs = [0.05, 0.05, 0.05, 0.001]
realizationsvec = [1000, 1000, 1000, 1500]
setsvec = [5, 5, 5, 2]

for a, alphaR in enumerate(alphaR):
    HR = HRs[a]
    h = hs[a]
    realizations = realizationsvec[a]
    sets = setsvec[a]

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    env.compute_var()
    color = plotting.plot_moment(ax, env, variable='sim', mom_type='var', legend_id='alpha', pic_in_grid=True)
    color = par.lighten_color(color, 0.5)
    env.compute_var_an(tl=0)
    plotting.plot_moment(ax, env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

ax.set_ylabel(fr'$\langle (q(t)-q_0)^2 \rangle$', fontsize = par.axis_fontsize)
ax.legend(fontsize = par.legend_size, loc = 'upper left')

fig.tight_layout()
fig.savefig(f"plots/paper/phi_var_grid_fdt.png", dpi=100)
