import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

mode = 'r'
L_type = 'L1'
alphaTs = [1.]
# alphaRs = [1]  
# HRs = [0.5] 
nu=1           
AHT=1
realizations = 1000
Tf = 100
h = 0.01
start_set = 1
sets = 1

HTs = (2 - np.array(alphaTs)) / 2

# Plotting
fig, ax = plt.subplots(figsize=(12, 9))

for alphaT in alphaTs:
    alphaR = alphaT
    HT = (2 - alphaT) / 2
    HR = HT #for now, only fluc diss

    env = utilities.read_env(mode=mode,
                            L_type = L_type, 
                            alpha=alphaT, H=HT,
                            alphaR=alphaR, HR=HR,
                            nu=nu,
                            AHT=AHT,
                            realizations=realizations,
                            Tf=Tf,
                            h=h,
                            start_set=start_set,
                            sets=sets)

    # Plot MSD
    env.compute_msd()
    color = plotting.plot_moment(ax, env, 'msd', 'sim')
    env.compute_msd_an()
    plotting.plot_moment(ax, env, 'msd', 'an')

    # Plot PDF
    # fig_pdf, ax_pdf = plt.subplots(figsize=(8, 7))
    # for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
    #     plotting.plot_pdf(ax_pdf, env, mode, time=t)
    # fig_pdf.tight_layout()
    # fig_pdf.savefig(f"plots/pdf/{mode}pdf_alphaT{alphaT}_HT{HT}_alphaR{alphaR}_HR{HR}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)

fig.tight_layout()
fig.savefig(f"plots/msd/{L_type}_{mode}msd_alphaT{alphaTs}_HT{HTs}_r{realizations*sets}_Tf{Tf}_h{h}_AHT{AHT}_nu{nu}.png", dpi=100)

