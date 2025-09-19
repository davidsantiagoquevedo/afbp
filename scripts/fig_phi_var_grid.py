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
L_type = 'L1'
DATA_PATH = 'data_tests'

fig, ax = plt.subplots(1, 4, figsize = (20, 5.5))
##########################################################

# alpha 1 --> Hfluc-diss = 0.5
alphaR = 1.
ax[0].set_title(fr'$\alpha$=1', fontsize = par.title_fontsize)
ax[0].set_ylabel(fr'$\langle (q(t)-q_0)^2 \rangle$', fontsize = par.axis_fontsize)
sets = 5
h = 0.05

# --------------------------------------------------------- 

HR = 0.8
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[0], env, variable='sim', mom_type='var', pic_in_grid=True, label = '(a)')
color = par.lighten_color(color, 0.5)
env.compute_var_an()
plotting.plot_moment(ax[0], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

# --------------------------------------------------------- 

HR = 0.5
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[0], env, variable='sim', mom_type='var', pic_in_grid=True)
color = par.lighten_color(color, 0.5)
env.compute_var_an()
plotting.plot_moment(ax[0], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

# --------------------------------------------------------- 
HR = 0.2
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[0], env, variable='sim', mom_type='var', pic_in_grid=True)
color = par.lighten_color(color, 0.5)
env.compute_var_an()
plotting.plot_moment(ax[0], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

ax[0].legend(fontsize = par.legend_size, loc = 'upper center')

##########################################################

# alpha 0.7 --> Hfluc-diss = 0.65
alphaR = 0.7
ax[1].set_title(fr'$\alpha$={alphaR}', fontsize = par.title_fontsize)
sets = 5
h = 0.05

# --------------------------------------------------------- 

HR = 0.8
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[1], env, variable='sim', mom_type='var', pic_in_grid=True, label = '(b)')
color = par.lighten_color(color, 0.5)
env.compute_var_an()
plotting.plot_moment(ax[1], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

# --------------------------------------------------------- 

HR = 0.65
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[1], env, variable='sim', mom_type='var', pic_in_grid=True)
color = par.lighten_color(color, 0.5)
env.compute_var_an()
plotting.plot_moment(ax[1], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

# --------------------------------------------------------- 

HR = 0.4
h=0.001
realizations=100
sets = 10

env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[1], env, variable='sim', mom_type='var', pic_in_grid=True)
color = par.lighten_color(color, 0.5)
env.compute_var_an()
plotting.plot_moment(ax[1], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

ax[1].legend(fontsize = par.legend_size, loc = 'upper center')

##########################################################

# alpha 0.5 --> Hfluc-diss = 0.75
alphaR = 0.5
ax[2].set_title(fr'$\alpha$={alphaR}', fontsize = par.title_fontsize)
realizations = 1000
sets = 5
h = 0.05

# --------------------------------------------------------- 

HR = 0.85
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[2], env, variable='sim', mom_type='var', pic_in_grid=True, label = '(c)')
color = par.lighten_color(color, 0.5)
env.compute_var_an()
plotting.plot_moment(ax[2], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

# --------------------------------------------------------- 

HR = 0.75
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[2], env, variable='sim', mom_type='var', pic_in_grid=True)
color = par.lighten_color(color, 0.5)
env.compute_var_an()
plotting.plot_moment(ax[2], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

# --------------------------------------------------------- 

HR = 0.55
h=0.005 
realizations=100
sets = 10

env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[2], env, variable='sim', mom_type='var', pic_in_grid=True)
color = par.lighten_color(color, 0.5)
# env.compute_var_an()
# plotting.plot_moment(ax[2], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)
env.compute_var_an(log=True)
plotting.plot_moment(ax[2], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color, log=True)

ax[2].legend(fontsize = par.legend_size, loc = 'upper center')

##########################################################

# alpha 0.3 --> Hfluc-diss = 0.85
alphaR = 0.3
ax[3].set_title(fr'$\alpha$={alphaR}', fontsize = par.title_fontsize)
realizations = 1000
sets = 5
h = 0.05

# --------------------------------------------------------- 

HR = 0.95
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[3], env, variable='sim', mom_type='var', pic_in_grid=True, label='(d)')
color = par.lighten_color(color, 0.5)
env.compute_var_an()
plotting.plot_moment(ax[3], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

# --------------------------------------------------------- 

HR = 0.85
h = 0.001
sets = 1
env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[3], env, variable='sim', mom_type='var', pic_in_grid=True)
color = par.lighten_color(color, 0.5)
env.compute_var_an()
plotting.plot_moment(ax[3], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color)

# --------------------------------------------------------- 

HR = 0.75
h=0.0005
realizations = 160
sets = 10
L_type = 'L2'

env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
env.compute_var()
color = plotting.plot_moment(ax[3], env, variable='sim', mom_type='var', pic_in_grid=True)
color = par.lighten_color(color, 0.5)
env.compute_var_an(log=True)
plotting.plot_moment(ax[3], env, variable='an', mom_type='var', pic_in_grid=True, legend_label=False, color = color, log=True)

ax[3].legend(fontsize = par.legend_size, loc = 'lower right')

##########################################################

fig.tight_layout()
fig.savefig(f"plots/paper/phi_var_grid.png", dpi=100)
