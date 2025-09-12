import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

mode = 'phi'
alphaRs = [0.3]  
HRs = [0.95, 0.85, 0.75]           
realizations = 1000
Tf = 10
h = 0.05
start_set = 1
sets = 5
# Plotting
fig1, ax1 = plt.subplots(figsize=(12, 9))
fig2, ax2 = plt.subplots()
A_H = []
for alphaR in alphaRs:
    for HR in HRs:

        env = utilities.read_env(mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)
        A_H.append(round(env.A_H, 2))

        # Plot moments
        env.compute_var()
        plotting.plot_moment(ax2, env, variable='sim', mom_type='var')
        env.compute_var_an()
        plotting.plot_moment(ax2, env, variable='an', mom_type='var')

        # Plot PDF
        fig_pdf, ax_pdf = plt.subplots(figsize=(8, 7))
        for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
            plotting.plot_pdf(ax_pdf, env, mode, time=t)
        fig_pdf.tight_layout()
        fig_pdf.savefig(f"plots/pdf/{mode}pdf_alphaR{alphaR}_H{HR}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)


fig1.tight_layout()
fig1.savefig(f"plots/var/{mode}var_alphaR{alphaRs}_HR{HRs}_r{realizations*sets}_Tf{Tf}_h{h}_AH{A_H}.png", dpi=100)
fig2.tight_layout()
fig2.savefig(f"plots/mean/{mode}mean_alphaR{alphaRs}_HR{HRs}_r{realizations*sets}_Tf{Tf}_h{h}_AH{A_H}.png", dpi=100)
