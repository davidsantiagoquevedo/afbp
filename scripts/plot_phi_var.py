import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

data_path = 'data_tests'
out_path = 'tests'#'var'
mode = 'phi'
L_type = 'L1'
realizations = 1500
Tf = 10
h = 0.001
start_set = 1
sets = 3

alphaRs = [0.5]#, 0.5, 0.5]
HRs = [0.65]#, 0.75, 0.85]
#alphaRs = [0.7, 0.7, 0.7]
#HRs = [0.55, 0.65, 0.75]

# Plotting
fig1, ax1 = plt.subplots(figsize=(12, 9))

for i, alphaR in enumerate(alphaRs):

    HR = HRs[i]
    if alphaR<0.4:
        h=0.001
        sets=1

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path=data_path)

    # Plot variance
    env.compute_var()
    color = plotting.plot_moment(ax1, env, variable='sim', mom_type='var')
    env.compute_var_an()
    plotting.plot_moment(ax1, env, variable='an', mom_type='var', color=color)

    # uncomment if you want to plot log
    # env.compute_var_an(log=True)
    # plotting.plot_moment(ax1, env, variable='an', log=True, mom_type='var', color=color)

fig1.tight_layout()
fig1.savefig(f"plots/{out_path}/{L_type}_{mode}var_alphaR{alphaRs}_HR{HRs}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)
