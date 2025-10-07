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
AHT=1
realizations = 100
Tf = 10
h = 0.005
start_set = 1
sets = 5


alphaTs = [1., 1., 1.]  
HTs = [0.8, 0.5, 0.2]   
alphaRs = alphaTs
HRs = HTs

# Plotting
fig, ax = plt.subplots(figsize=(12, 9))

for i, alphaR in enumerate(alphaRs):

    alphaT = alphaTs[i]
    HT = HTs[i]
    HR = HRs[i]

    if alphaT==0.5:
        sets = 1
    if alphaT<0.4:
        h=0.001
        sets=1

    env = utilities.read_env(mode=mode,
                            L_type = L_type, 
                            alpha=alphaT, H=HT,
                            alphaR=alphaR, HR=HR,
                            ups=ups,
                            AHT=AHT,
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
fig.savefig(f"plots/msd/{L_type}_{mode}msd_alphaT{alphaTs}_HT{HTs}_r{realizations*sets}_Tf{Tf}_h{h}_AHT{AHT}_ups{ups}.png", dpi=100)

