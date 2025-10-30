################# OUT-OF-EQUILIBRIUM ##########################
import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import utilities
import plotting_param as par

DATA_PATH = 'data_tests'
# DATA_PATH = 'data_cluster2'
mode = 'r'
L_type = 'L1'
ups = 1
AHT = 1.
total = True
if AHT<1:
    total = False
Tf = 20.
realizations = 1000
start_set=1
sets=10
L_type = 'L1'
std = False
rule = 'N'
h = 0.005

alphaT = [1., 0.7, 0.5, 0.3]
HT = [(2 - a) / 2 for a in alphaT]    
alphaR = [1, 0.7, 0.5, 0.3]
HR = [(2 - a) / 2 for a in alphaR]    

fig, ax = plt.subplots(1, 4, figsize = (27, 7))
##########################################################

at = 1.
ht = 0.5
alphaR = [1., 0.7, 0.5, 0.3]
HR = [(2 - a) / 2 for a in alphaR]   

setsv = [10, 10, 10, 5]
hv = [0.005, 0.005, 0.005, 0.001]

# setsv = [5, 5, 5, 5]

for r, ar in enumerate(alphaR):
    hr = HR[r]

    sets = setsv[r]
    h = hv[r]

    env = utilities.read_env(L_type=L_type, mode=mode, alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, realizations=realizations,Tf=Tf,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT,  rule=rule, path=DATA_PATH)

    env.compute_msd()
    color = plot.plot_moment(ax[0], env, variable='sim', mom_type='msd', pic_in_grid=True, label = '', legend_id='alphaR', std=std)
    # color = par.lighten_color(color, 0.5)
    env.compute_msd_an(total=total)
    plot.plot_moment(ax[0], env, variable='an', mom_type='msd', pic_in_grid=True, color = color, legend_label=False)

ax[0].set_title(fr'$\alpha_T$={at}', fontsize = par.title_fontsize)

##########################################################
sets = 20
at = alphaT[1]
ht = HT[1]

setsv = [sets, sets, sets, 5]
hv = [0.005, 0.005, 0.005, 0.001]

# setsv = [5, 5, 5, 5]

for r, ar in enumerate(alphaR):
    hr = HR[r]

    sets = setsv[r]
    h = hv[r]

    env = utilities.read_env(L_type=L_type, mode=mode, alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, realizations=realizations,Tf=Tf,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT,  rule=rule, path=DATA_PATH)

    env.compute_msd()
    color = plot.plot_moment(ax[1], env, variable='sim', mom_type='msd', pic_in_grid=True, label = '', legend_id='alphaR', std=std)
    color = par.lighten_color(color, 0.5)
    env.compute_msd_an(total=total)
    plot.plot_moment(ax[1], env, variable='an', mom_type='msd', pic_in_grid=True, color = color, legend_label=False)

ax[1].set_title(fr'$\alpha_T$={at}', fontsize = par.title_fontsize)

##########################################################
sets=20
at = alphaT[2]
ht = HT[2]

setsv = [sets, sets, sets, 5]
hv = [0.005, 0.005, 0.005, 0.001]

# setsv = [5, 5, 4, 5]


for r, ar in enumerate(alphaR):
    hr = HR[r]

    sets = setsv[r]
    h = hv[r]

    env = utilities.read_env(L_type=L_type, mode=mode, alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, realizations=realizations,Tf=Tf,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT,  rule=rule, path=DATA_PATH)

    env.compute_msd()
    color = plot.plot_moment(ax[2], env, variable='sim', mom_type='msd', pic_in_grid=True, label = '', legend_id='alphaR', std=std)
    color = par.lighten_color(color, 0.5)
    env.compute_msd_an(total=total)
    plot.plot_moment(ax[2], env, variable='an', mom_type='msd', pic_in_grid=True, color = color, legend_label=False)

ax[2].set_title(fr'$\alpha_T$={at}', fontsize = par.title_fontsize)

##########################################################

sets=10
at = alphaT[3]
ht = HT[3]

setsv = [sets, sets, sets, 4]
hv = [0.005, 0.005, 0.005, 0.001]

# setsv = [5, 5, 4, 4]

for r, ar in enumerate(alphaR):
    hr = HR[r]

    sets = setsv[r]
    h = hv[r]

    env = utilities.read_env(L_type=L_type, mode=mode, alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, realizations=realizations,Tf=Tf,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT,  rule=rule, path=DATA_PATH)

    env.compute_msd()
    color = plot.plot_moment(ax[3], env, variable='sim', mom_type='msd', pic_in_grid=True, label = '', legend_id='alphaR', std=std)
    color = par.lighten_color(color, 0.5)
    env.compute_msd_an(total=total)
    plot.plot_moment(ax[3], env, variable='an', mom_type='msd', pic_in_grid=True, color = color, legend_label=False)

ax[3].set_title(fr'$\alpha_T$={at}', fontsize = par.title_fontsize)

##########################################################

fig.tight_layout()
# fig.savefig(f"plots/tests/rmsd_sim_grid_fdt_h{h}_rule{rule}_sets10.png", dpi=100)
fig.savefig(f"plots/tests/rmsd_sim_grid_fdt_mix_rule{rule}.png", dpi=100)

