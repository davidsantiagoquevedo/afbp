import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

mode = 'phi'
alphas = [1.]   # include both cases
Hs = [0.7, 0.5, 0.3]            # only used if alpha==1
realizations = 1000
Tf = 10
h = 0.05
sets = 5

# Plotting
fig1, ax1 = plt.subplots(figsize=(12, 9))
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

for alpha in alphas:
    for H in Hs:

        env = utilities.read_env(mode, alpha, H, realizations, Tf, h, sets)

        # Plot MSD
        env.compute_msd()
        plotting.plot_msd(ax1, env, 'sim')
        # env.compute_msd_sol()
        # plotting.plot_msd(ax1, env, 'sol')
        # env.compute_msd_an()
        # plotting.plot_msd(ax1, env, 'an', label_an=(env.alpha == 0.3))

        # Plot moments
        env.compute_var()
        plotting.plot_moment(ax2, env, variable='sim', mom_type='var')
        env.compute_var_an()
        plotting.plot_moment(ax2, env, variable='an', mom_type='var')
        plotting.plot_moment(ax2, env, variable='fit', mom_type='var')

        env.compute_mean()
        plotting.plot_moment(ax3, env, 'sim', 'mean')
        plotting.plot_moment(ax3, env, 'fit', 'mean')

        # Plot PDF
        fig_pdf, ax_pdf = plt.subplots(figsize=(8, 7))
        for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
            plotting.plot_pdf(ax_pdf, env, mode, time=t)
        fig_pdf.tight_layout()
        fig_pdf.savefig(f"plots/pdf/{mode}pdf_alpha{alpha}_H{H}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)

fig1.tight_layout()
fig1.savefig(f"plots/msd/{mode}msd_alpha{alphas}_H{Hs}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)
fig2.tight_layout()
fig2.savefig(f"plots/var/{mode}var_alpha{alphas}_H{Hs}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)
fig3.tight_layout()
fig3.savefig(f"plots/mean/{mode}mean_alpha{alphas}_H{Hs}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)
