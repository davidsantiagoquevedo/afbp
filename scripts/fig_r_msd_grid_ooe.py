################# OUT-OF-EQUILIBRIUM ##########################
import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import utilities
import plotting_param as par

DATA_PATH = 'data_tests'
mode = 'r'
L_type = 'L1'
ups = 1
AHT = 1.
total = True
if AHT<1:
    total = False
Tf = 10
realizations = 1000
start_set=1
sets=1
L_type = 'L1'
rule = 'mean'

fig, ax = plt.subplots(1, 4, figsize = (20, 5.5))

##########################################################
alpha = 1.
alphaR = alpha

hs = [0.01, 0.01, 0.005]

for i, H in enumerate([0.8, 0.5, 0.3]):
    h = hs[i]

    env = utilities.read_env(L_type=L_type, mode=mode, alpha=alpha, H=H, alphaR=alpha, HR=H, ups=ups, realizations=realizations,Tf=Tf,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT,  rule=rule, path=DATA_PATH)

    env.compute_msd()
    color = plot.plot_moment(ax[0], env, variable='sim', mom_type='msd', pic_in_grid=True, label = '(a)')
    color = par.lighten_color(color, 0.5)
    env.compute_msd_an(total=total)
    plot.plot_moment(ax[0], env, variable='an', mom_type='msd', pic_in_grid=True, color = color)

ax[0].set_title(fr'$\alpha_Q$=1', fontsize = par.title_fontsize)
if AHT<1:
    ax[0].set_ylabel(fr'$\langle (r(t)-r_0)^2 \rangle_a$', fontsize = par.axis_fontsize)
else:
    ax[0].set_ylabel(fr'$\langle (r(t)-r_0)^2 \rangle$', fontsize = par.axis_fontsize)

##########################################################
alpha = 0.7
alphaR = alpha

hs = [0.001, 0.005, 0.001]

for i, H in enumerate([0.8, 0.65, 0.5]):
    h = hs[i]

    env = utilities.read_env(L_type=L_type, mode=mode, alpha=alpha, H=H, alphaR=alpha, HR=H, ups=ups, realizations=realizations,Tf=Tf,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT,  rule=rule, path=DATA_PATH)

    env.compute_msd()
    color = plot.plot_moment(ax[1], env, variable='sim', mom_type='msd', pic_in_grid=True, label = '(a)')
    color = par.lighten_color(color, 0.5)
    env.compute_msd_an(total=total)
    plot.plot_moment(ax[1], env, variable='an', mom_type='msd', pic_in_grid=True, color = color)

ax[1].set_title(fr'$\alpha_Q$=0.7', fontsize = par.title_fontsize)


##########################################################
alpha = 0.5
alphaR = alpha

hs = [0.001, 0.001, 0.001]

for i, H in enumerate([0.85, 0.75, 0.65]):
    h = hs[i]
    
    env = utilities.read_env(L_type=L_type, mode=mode, alpha=alpha, H=H, alphaR=alpha, HR=H, ups=ups, realizations=realizations,Tf=Tf,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT,  rule=rule, path=DATA_PATH)

    env.compute_msd()
    color = plot.plot_moment(ax[2], env, variable='sim', mom_type='msd', pic_in_grid=True, label = '(a)')
    color = par.lighten_color(color, 0.5)
    env.compute_msd_an(total=total)
    plot.plot_moment(ax[2], env, variable='an', mom_type='msd', pic_in_grid=True, color = color)

ax[2].set_title(fr'$\alpha_Q$=0.5', fontsize = par.title_fontsize)

##########################################################

alpha = 0.3
alphaR = alpha

hs = [0.001, 0.001, 0.001]

for i, H in enumerate([0.95, 0.85, 0.75]):
    h = hs[i]

    env = utilities.read_env(L_type=L_type, mode=mode, alpha=alpha, H=H, alphaR=alpha, HR=H, ups=ups, realizations=realizations,Tf=Tf,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT,  rule=rule, path=DATA_PATH)

    env.compute_msd()
    color = plot.plot_moment(ax[3], env, variable='sim', mom_type='msd', pic_in_grid=True, label = '(a)')
    color = par.lighten_color(color, 0.5)
    env.compute_msd_an(total=total)
    plot.plot_moment(ax[3], env, variable='an', mom_type='msd', pic_in_grid=True, color = color)

ax[3].set_title(fr'$\alpha_Q$=0.3', fontsize = par.title_fontsize)


fig.tight_layout()
if AHT<1:
    fig.savefig(f"plots/paper/rmsda_grid.png", dpi=100)
else:
    fig.savefig(f"plots/paper/rmsd_grid.png", dpi=100)

