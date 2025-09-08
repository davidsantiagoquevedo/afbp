import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

mode = 'r'
alphaT = 1
alphaRs = [1.0]  
HRs = [0.7, 0.5, 0.3] 
nu=1           
realizations = 160
Tf = 10
h = 0.005
start_set = 1
sets = 8

HT = (2 - alphaT) / 2

# Plotting
fig1, ax1 = plt.subplots(figsize=(12, 9))
fig2, ax2 = plt.subplots(figsize=(12, 9))
fig3, ax3 = plt.subplots()
A_H = []
for alphaR in alphaRs:
    for HR in HRs:

        env = utilities.read_env(mode=mode, 
                                 alpha=alphaT, H=HT,
                                 alphaR=alphaR, HR=HR,
                                 nu=nu,
                                 realizations=realizations,
                                 Tf=Tf,
                                 h=h,
                                 start_set=start_set,
                                 sets=sets)
        A_H.append(round(env.A_H, 2))

        # Plot MSD
        env.compute_msd()
        plotting.plot_msd(ax1, env, 'sim')
        env.compute_msd_an()
        plotting.plot_msd(ax1, env, 'an')

        # Plot moments
        env.compute_var()
        plotting.plot_moment(ax2, env, variable='sim', mom_type='var')

        env.compute_mean()
        plotting.plot_moment(ax3, env, 'sim', 'mean')

        # Plot PDF
        # fig_pdf, ax_pdf = plt.subplots(figsize=(8, 7))
        # for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
        #     plotting.plot_pdf(ax_pdf, env, mode, time=t)
        # fig_pdf.tight_layout()
        # fig_pdf.savefig(f"plots/pdf/{mode}pdf_alphaT{alphaT}_HT{HT}_alphaR{alphaR}_HR{HR}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)

fig1.tight_layout()
fig1.savefig(f"plots/msd/{mode}msd_alphaT{alphaT}_HT{HT}_alphaR{alphaRs}_HR{HRs}_r{realizations*sets}_Tf{Tf}_h{h}_AH{A_H}_nu{nu}.png", dpi=100)
fig2.tight_layout()
fig2.savefig(f"plots/var/{mode}var_alphaT{alphaT}_HT{HT}_alphaR{alphaRs}_HR{HRs}_r{realizations*sets}_Tf{Tf}_h{h}_AH{A_H}_nu{nu}.png", dpi=100)
fig3.tight_layout()
fig3.savefig(f"plots/mean/{mode}mean_alphaT{alphaT}_HT{HT}_alphaR{alphaRs}_HR{HRs}_r{realizations*sets}_Tf{Tf}_h{h}_AH{A_H}_nu{nu}.png", dpi=100)
