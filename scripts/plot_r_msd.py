import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

DATA_PATH = 'data_tests'
mode = 'r'
L_type = 'L1'
ups=1
AHT=1.
realizations = 1000
Tf = 10
h = 0.05
start_set = 1
sets = 1
hR = h
rule = 'N'

alphaTs = [1.]  
HTs = [0.5]   
# alphaRs = [1., 0.8, 0.3]
# HRs = [0.5, 0.6, 0.85]
alphaRs = alphaTs
HRs = HTs

# Plotting
fig, ax = plt.subplots(figsize=(12, 9))

for i, alphaR in enumerate(alphaRs):

    alphaT = alphaTs[i]
    HT = HTs[i]
    HR = HRs[i]

    env = utilities.read_env(mode=mode,
                            L_type = L_type, 
                            alpha=alphaT, H=HT,
                            alphaR=alphaR, HR=HR,
                            hR=hR,
                            ups=ups,
                            AHT=AHT,
                            rule=rule,
                            realizations=realizations,
                            Tf=Tf,
                            h=h,
                            start_set=start_set,
                            sets=sets,
                            path = DATA_PATH)

    # Plot MSD
    env.compute_msd()
    color = plotting.plot_moment(ax, env, 'msd', 'sim')
    env.compute_msd_an(total=True)
    plotting.plot_moment(ax, env, 'msd', 'an', color=color, legend_label=False)


fig.tight_layout()
fig.savefig(f"plots/tests/{L_type}_{mode}msd_alphaT{alphaTs}_HT{HTs}_r{realizations*sets}_Tf{Tf}_h{h}_hR{hR}_AHT{AHT}_ups{ups}_rule{rule}.png", dpi=100)

