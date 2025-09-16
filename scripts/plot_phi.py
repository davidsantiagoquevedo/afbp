import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

mode = 'phi'
L_type = 'L1'
alphaRs = [0.3]  
HRs = [0.75]   
fluc_diss = False        
realizations = 1000
Tf = 10
h = 0.05
start_set = 1
sets = 1

# Plotting
fig1, ax1 = plt.subplots(figsize=(12, 9))

A_H = []
HRs_vec = [] if fluc_diss else HRs
for alphaR in alphaRs:

    if fluc_diss:
        HRs = [(2 - alphaR) / 2]
        HRs_vec.append(HRs)

    for HR in HRs:

        env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
        A_H.append(round(env.A_H, 2))

        # Plot variance
        env.compute_var()
        color = plotting.plot_moment(ax1, env, variable='sim', mom_type='var')
        env.compute_var_an()
        plotting.plot_moment(ax1, env, variable='an', mom_type='var', color=color)

        # uncomment if you want to plot log
        # env.compute_var_an(log=True)
        # plotting.plot_moment(ax1, env, variable='an', log=True, mom_type='var', color=color)

        # Plot PDF
        fig_pdf, ax_pdf = plt.subplots(figsize=(8, 7))
        for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
            plotting.plot_pdf(ax_pdf, env, mode, time=t)
        fig_pdf.tight_layout()
        fig_pdf.savefig(f"plots/pdf/{L_type}_{mode}pdf_alphaR{alphaR}_H{HR}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)


fig1.tight_layout()
fig1.savefig(f"plots/var/{L_type}_{mode}var_alphaR{alphaRs}_HR{HRs_vec}_r{realizations*sets}_Tf{Tf}_h{h}_AH{A_H}.png", dpi=100)
