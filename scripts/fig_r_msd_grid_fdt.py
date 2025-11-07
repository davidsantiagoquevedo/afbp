################# OUT-OF-EQUILIBRIUM ##########################
import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import utilities
import plotting_param as par

DATA_PATH = 'data'
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
L_type = 'L1'
std = False
rule = 'N'

alphaT = [1., 0.7, 0.5, 0.3]
HT = [(2 - a) / 2 for a in alphaT]    
alphaR = [1., 0.7, 0.5, 0.3]
HR = [(2 - a) / 2 for a in alphaR]    
setsv = [20, 20, 20, 5]
hv = [0.005, 0.005, 0.005, 0.001]

fig, ax = plt.subplots(1, 4, figsize = (27, 7))
##########################################################

for t, at in enumerate(alphaT):
    ht = HT[t]

    for r, ar in enumerate(alphaR):

        hr = HR[r]
        sets = setsv[r]
        h = hv[r]
        
        if ar==0.3:
            start_set=1

        env = utilities.read_env(L_type=L_type, mode=mode, alpha=at, H=ht, alphaR=ar, HR=hr, ups=ups, realizations=realizations,Tf=Tf,h=h, hR = h, start_set=start_set,sets=sets, AHT=AHT,  rule=rule, path=DATA_PATH)

        env.compute_msd()
        color = plot.plot_moment(ax[t], env, variable='sim', mom_type='msd', pic_in_grid=True, label = '', legend_id='alphaR', std=std)
        env.compute_msd_an(total=total)
        plot.plot_moment(ax[t], env, variable='an', mom_type='msd', pic_in_grid=True, color = color, legend_label=False)

    ax[t].set_title(fr'$\alpha_T$={at}', fontsize = par.title_fontsize)

fig.tight_layout()
fig.savefig(f"plots/tests/rmsd_sim_grid_fdt_h{h}_rule{rule}.png", dpi=100)
# fig.savefig(f"plots/tests/rmsd_sim_grid_fdt_mix_rule{rule}_stddivn.png", dpi=100)

