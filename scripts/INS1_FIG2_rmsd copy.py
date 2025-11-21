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
sets = 3

alphaRs = [1., 0.7, 0.5, 0.3, 0.2]
HRs = [(2 - a) / 2 for a in alphaRs]  
hs = [0.005, 0.005, 0.005, 0.0001, 0.0005]   
setsv = [3, 3, 3, 1, 1]  

# Plotting
fig, ax = plt.subplots(figsize=(7, 5))

for i, alphaR in enumerate(alphaRs):

    alphaT=alphaR

    HR = HRs[i]
    HT = HRs[i]

    h = hs[i]
    sets =setsv[i]

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
fig.savefig(f"plots/paper/inset_ups{ups}_fdt.png", dpi=100)

