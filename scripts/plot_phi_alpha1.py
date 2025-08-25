import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

alphas = [1.]
# H = None
Hs = [0.3, 0.5, 0.7]
realizations = 1000
Tf = 10.
h = 0.01
sets = 5
envs = []

envs = utilities.read_envs(alphas, sets, Tf, h, realizations, Hs)

"""
PLOTTING
msd, mean and variance are plotted in the same figure for different value of alpha while a figure is created for each alpha containing its pdf at three different times.
"""

fig1, ax1 = plt.subplots(figsize=(12,9))
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
for alpha_index, alpha in enumerate(alphas):
    
    if Hs is None:
        Hs = (2-alpha)/2
        
    for H_index, H in enumerate(Hs):
        env_index = alpha_index + H_index
        env = envs[env_index]
        label_an = alpha_index == 0 and H_index == 0
        plotting.plot_msd(ax1, env, 'phi')
        plotting.plot_msd(ax1, env, 'phi_sol')
        plotting.plot_msd(ax1, env, 'an', label_an=label_an)

        # plotting.plot_moment(ax2, env, 'phi', 'var')
        # plotting.plot_moment(ax2, env, 'phi_sol', 'var')
        # plotting.plot_moment(ax2, env, 'an', 'var')
        # plotting.plot_moment(ax2, env, 'fit', 'var')

        # plotting.plot_moment(ax3, env, 'phi', 'mean')
        # plotting.plot_moment(ax3, env, 'phi_sol', 'mean')
        # plotting.plot_moment(ax3, env, 'an', 'mean')

        fig4, ax4 = plt.subplots()
        plotting.plot_pdf(ax4, env, time = int(Tf/(4*h)))
        plotting.plot_pdf(ax4, env, time = int(Tf/(2*h)))
        #plotting.plot_pdf(ax4, env, time = int((Tf/h)-1))
        fig4.tight_layout()
        fig4.savefig(f"plots/pdf/phipdf_r_{env.realizations}_Tf_{Tf}_h_{h}_alpha_{env.alpha}_H_{env.H}.png", dpi=100)

fig1.tight_layout()
fig1.savefig(f"plots/msd/phicorr_r_{env.realizations}_Tf_{Tf}_h_{h}.png", dpi=100)
fig2.tight_layout()
fig2.savefig(f"plots/var/phivar_r_{env.realizations}_Tf_{Tf}_h_{h}.png", dpi=100)
fig3.tight_layout()
fig3.savefig(f"plots/mean/phimean_r_{env.realizations}_Tf_{Tf}_h_{h}.png", dpi=100)