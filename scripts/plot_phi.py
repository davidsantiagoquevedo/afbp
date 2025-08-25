import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

alphas = [0.5]   # include both cases
Hs = None#[0.5]            # only used if alpha==1
realizations = 1200
Tf = 10
h = 0.05
sets = 1

# Plotting
fig1, ax1 = plt.subplots(figsize=(12, 9))
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

for alpha in alphas:
    if alpha == 1:
        H_values = Hs
    else:
        H_values = [(2 - alpha) / 2]

    for H in H_values:

        env = utilities.read_envs(alpha, H, sets, Tf, h, realizations)

        # Plot MSD
        plotting.plot_msd(ax1, env, 'phi')
        plotting.plot_msd(ax1, env, 'phi_sol')
        plotting.plot_msd(ax1, env, 'an', label_an=(env.alpha == 0.3))

        # Example if you want variance/mean 
        # plotting.plot_moment(ax2, env, 'phi', 'var')
        # plotting.plot_moment(ax3, env, 'phi', 'mean')

        # Example PDF plotting
        # fig_pdf, ax_pdf = plt.subplots()
        # for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
        #     plotting.plot_pdf(ax_pdf, env, time=t)
        # fig_pdf.savefig(f"plots/pdf/pdf_alpha{alpha}_H{H}.png", dpi=100)

fig1.tight_layout()
fig1.savefig(f"plots/msd/phicorr_r{realizations}_Tf{Tf}_h{h}.png", dpi=100)
fig2.tight_layout()
fig2.savefig(f"plots/var/phivar_r{realizations}_Tf{Tf}_h{h}.png", dpi=100)
fig3.tight_layout()
fig3.savefig(f"plots/mean/phimean_r{realizations}_Tf{Tf}_h{h}.png", dpi=100)
