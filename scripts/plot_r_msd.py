import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

# DATA_PATH = 'data_tests/data_parall_work'
# DATA_PATH = 'data_santiofi'
DATA_PATH = 'data_tests'
mode = 'r'
L_type = 'L1'
ups=1
realizations = 1000
Tf = 20.
h = 0.005
start_set = 1
sets = 1

alphaT = 0.3
HT = 0.85   
alphaRs = [0.3]
HRs = [0.85]
# alphaRs = [alphaT]
# HRs = [HT]

# Plotting
fig, ax = plt.subplots(figsize=(12, 9))

for i, alphaR in enumerate(alphaRs):

    alphaT=alphaR

    HR = HRs[i]
    HT = HRs[i]

    # HT=HR
    env = utilities.read_env(mode=mode,
                            L_type = L_type, 
                            alpha=alphaT, H=HT,
                            alphaR=alphaR, HR=HR,
                            ups=ups,
                            realizations=realizations,
                            Tf=Tf,
                            h=h,
                            start_set=start_set,
                            sets=sets,
                            path = DATA_PATH)

    # Plot MSD
    env.compute_msd()
    color = plotting.plot_moment(ax, env, 'msd', 'sim', legend_id='alphaR', std=True)
    env.compute_msd_an(total=True)
    
    plotting.plot_moment(ax, env, 'msd', 'an', color=color, legend_label=False)


fig.tight_layout()
fig.savefig(f"plots/tests/{mode}msd_alphaT{alphaT}_HT{HT}_alphaR{alphaRs}_HR{HRs}_r{realizations*sets}_Tf{Tf}_h{h}_hR_ups{ups}.png", dpi=100)

