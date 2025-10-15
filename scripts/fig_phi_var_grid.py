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
realizations = 1000
sets = 5
L_type = 'L1'
DATA_PATH = 'data'
m=1e-9
eta=1

def tl(alpha, H, eta=1, m=0.00000001):
    return ((m*H*gamma(2*H))/(eta*(alpha+H-1)*gamma(alpha)*gamma(alpha+2*H-1)))**(1/(4-2*alpha-2*H))


fig, ax = plt.subplots(1, 4, figsize = (20, 5.5))

##########################################################

alphaR = 1.
hs = [0.05, 0.05, 0.05]

for i, HR in enumerate([0.8, 0.5, 0.2]):
    h = hs[i]

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    env.compute_var()
    color = plotting.plot_moment(ax[0], env, variable='sim', mom_type='var', pic_in_grid=True, label = '(a)')
    color = par.lighten_color(color, 0.5)
    tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
    env.compute_var_an(tl=tl_value)
    plotting.plot_moment(ax[0], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)


ax[0].set_title(fr'$\alpha_Q$=1', fontsize = par.title_fontsize)
ax[0].set_ylabel(fr'$\langle (q(t)-q_0)^2 \rangle$', fontsize = par.axis_fontsize)
ax[0].legend(fontsize = par.legend_size, loc = 'upper center')

##########################################################

alphaR = 0.7
hs = [0.05, 0.05, 0.01]

for i, HR in enumerate([0.8, 0.65, 0.5]):
    h = hs[i]

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    env.compute_var()
    color = plotting.plot_moment(ax[1], env, variable='sim', mom_type='var', pic_in_grid=True, label = '(b)')
    color = par.lighten_color(color, 0.5)
    tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
    env.compute_var_an(tl=tl_value)
    plotting.plot_moment(ax[1], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

ax[1].set_title(fr'$\alpha_Q$={alphaR}', fontsize = par.title_fontsize)
ax[1].legend(fontsize = par.legend_size, loc = 'upper center')

##########################################################

# alpha 0.5 --> Hfluc-diss = 0.75
alphaR = 0.5
ax[2].set_title(fr'$\alpha_Q$={alphaR}', fontsize = par.title_fontsize)
hs = [0.05, 0.05, 0.001]

for i, HR in enumerate([0.85, 0.75, 0.65]):
    h = hs[i]

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    env.compute_var()
    color = plotting.plot_moment(ax[2], env, variable='sim', mom_type='var', pic_in_grid=True, label = '(c)')
    color = par.lighten_color(color, 0.5)
    tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
    env.compute_var_an(tl=tl_value)
    plotting.plot_moment(ax[2], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

ax[2].legend(fontsize = par.legend_size, loc = 'upper center')

##########################################################

alphaR = 0.3
ax[3].set_title(fr'$\alpha_Q$={alphaR}', fontsize = par.title_fontsize)
realizations = 1000
sets = 5
h = 0.01

# --------------------------------------------------------- 

HR = 0.95
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[3], env, variable='sim', mom_type='var', pic_in_grid=True, label='(d)')
color = par.lighten_color(color, 0.5)
tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
env.compute_var_an(tl=tl_value)
plotting.plot_moment(ax[3], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

# --------------------------------------------------------- 

HR = 0.85
h = 0.001
sets = 2
realizations = 1500
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[3], env, variable='sim', mom_type='var', pic_in_grid=True)
color = par.lighten_color(color, 0.5)
tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
env.compute_var_an(tl=tl_value)
plotting.plot_moment(ax[3], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

# --------------------------------------------------------- 

HR = 0.75
h=0.0005
sets = 10
L_type = 'L2'

realizations = 160
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)

# add 10 sets of 150 realizations
# realizations = 150
# for set_index in range(sets):
#     envi = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
#     env.realizations += realizations
#     env.trajectories = np.vstack((env.trajectories, envi.trajectories))

# print(env.realizations)

env.compute_var()
color = plotting.plot_moment(ax[3], env, variable='sim', mom_type='var', pic_in_grid=True)
color = par.lighten_color(color, 0.5)
# env.compute_var_an(log=True)
tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
env.compute_var_an(tl=tl_value)
plotting.plot_moment(ax[3], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

ax[3].legend(fontsize = par.legend_size, loc = 'lower right')

##########################################################

fig.tight_layout()
fig.savefig(f"plots/paper/phi_var_grid.png", dpi=100)
