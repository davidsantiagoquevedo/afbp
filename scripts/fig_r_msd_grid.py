import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import utilities
import plotting_param as par


alpha = [1., 0.7, 0.5, 0.3]
mode = 'r'
L_type = 'L1'
nu = 1
AHT = 1

fig, ax = plt.subplots(1, 4, figsize = (20, 5.5))

##########################################################

ai = alpha[0]
H = [0.8, 0.5, 0.2]    
Tf = 10
realizations = 100
start_set = 1
sets = 5
h = 0.005

for hi in H:

    env = utilities.read_env(L_type=L_type, mode=mode, alpha=ai, H=hi, alphaR=ai, HR=hi, nu=nu, realizations=realizations,Tf=Tf,h=h,start_set=start_set,sets=sets, AHT=AHT)
    env.compute_msd()
    color = plot.plot_moment(ax[0], env, variable='sim', mom_type='msd', pic_in_grid=True, label = '(a)')
    color = par.lighten_color(color, 0.5)
    env.compute_msd_an()
    plot.plot_moment(ax[0], env, variable='an', mom_type='msd', pic_in_grid=True, color = color)

fig.tight_layout()
fig.savefig(f"plots/paper/rmsd_alphaTR{alpha}_Tf{Tf}_h{h}_nu{nu}.png", dpi=100)
