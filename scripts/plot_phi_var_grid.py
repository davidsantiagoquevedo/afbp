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

fig, ax = plt.subplots(1, 4, figsize = (20, 5.5))

# alpha 1 --> Hfluc-diss = 0.5
alphaR = 1.
ax[0].set_title(fr'$\alpha$=1', fontsize = par.title_fontsize)
sets = 5
h = 0.05

# --- H 0.8
HR = 0.8
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[0], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[0], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

# --- H 0.5
HR = 0.5
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[0], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[0], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

# --- H 
HR = 0.2
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[0], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[0], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

# alpha 0.7 --> Hfluc-diss = 0.65
alphaR = 0.7
ax[1].set_title(fr'$\alpha$={alphaR}', fontsize = par.title_fontsize)
sets = 5
h = 0.05

# --- H 0.8
HR = 0.8
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[1], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[1], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

# --- H 0.65
HR = 0.65
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[1], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[1], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

# --- H 
HR = 0.4
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[1], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[1], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

fig.text(0.5, 0.04, 't', ha='center', fontsize=par.title_fontsize)    
fig.text(0.04, 0.5, r'$\sigma^2_{\phi}$', va='center', rotation='vertical', fontsize=par.title_fontsize)  

# alpha 0.5 --> Hfluc-diss = 0.75
alphaR = 0.5
ax[2].set_title(fr'$\alpha$={alphaR}', fontsize = par.title_fontsize)
sets = 5
h = 0.05

# --- H 0.8
HR = 0.85
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[2], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[2], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

# --- H 0.65
HR = 0.75
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[2], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[2], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

# --- H 
HR = 0.55
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[2], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[2], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

# alpha 0.3 --> Hfluc-diss = 0.85
alphaR = 0.3
ax[3].set_title(fr'$\alpha$={alphaR}', fontsize = par.title_fontsize)
sets = 5
h = 0.05

# --- H 0.8
HR = 0.95
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[3], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[3], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

# --- H 0.65
HR = 0.85
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[3], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[3], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

# --- H 
HR = 0.75
env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
env.compute_var()
plotting.plot_moment(ax[3], env, variable='sim', mom_type='var', pic_in_grid=True)
env.compute_var_an()
plotting.plot_moment(ax[3], env, variable='an', mom_type='var', pic_in_grid=True, label_an=False)

fig.text(0.5, -1, 't', ha='center', fontsize=par.title_fontsize)    
fig.text(0.04, 0.5, r'$\sigma^2_{\phi}$', va='center', rotation='vertical', fontsize=par.title_fontsize)  

fig.tight_layout()
fig.savefig(f"plots/paper/phi_var_grid.png", dpi=100)
