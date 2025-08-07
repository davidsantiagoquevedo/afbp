import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import time
import matplotlib.cm as cm
import matplotlib.colors as mcolors

alphas = [0.3, 0.5, 0.7, 0.9]
realizations = 3000
Tf = 10
h = 0.0005
sets = 2
envs = []

for alpha_index, alpha in enumerate(alphas):    
    
    H = (2-alpha)/2
    for set_index in range(sets):
        set_label = str(set_index+1).zfill(3)
        set_index += 1
        
        env = angular_fbm(realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
        
        filepath = (
            f"data/r_{env.realizations}_"
            f"alpha_{env.alpha}_"
            f"H_{env.H}_"
            f"Tf_{env.Tf}_"
            f"h_{env.h}_"
            f"set_{set_label}.pkl"
        )
        env = angular_fbm.load(filepath)
        
        if set_index==1:
            env_multiset = env
        else:
            env_multiset.realizations += realizations
            env_multiset.phi_matrix = np.vstack((env_multiset.phi_matrix, env.phi_matrix))
        
    env_multiset.compute_phi_correlation()
    env_multiset.compute_mean()
    env_multiset.compute_variance()
        
    envs.append(env_multiset)


"""
PLOTTING
msd, mean and variance are plotted in the same figure for different value of alpha while a figure is created for each alpha containing its pdf at three different times.
"""
fig1, ax1 = plt.subplots(figsize=(12,9))
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
for alpha_index in range(len(alphas)):
    env = envs[alpha_index]
    label_an = env.alpha == 0.3
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

    # fig4, ax4 = plt.subplots()
    # plotting.plot_pdf(ax4, env, time = int(Tf/(4*h)))
    # plotting.plot_pdf(ax4, env, time = int(Tf/(2*h)))
    # plotting.plot_pdf(ax4, env, time = int((Tf/h)-1))
    # fig4.tight_layout()
    # fig4.savefig(f"plots/pdf/phipdf_r_{env.realizations}_Tf_{Tf}_h_{h}_alpha_{env.alpha}.png", dpi=100)

fig1.tight_layout()
fig1.savefig(f"plots/msd/phicorr_r_{env.realizations}_Tf_{Tf}_h_{h}.png", dpi=100)
fig2.tight_layout()
fig2.savefig(f"plots/var/phivar_r_{env.realizations}_Tf_{Tf}_h_{h}.png", dpi=100)
fig3.tight_layout()
fig3.savefig(f"plots/mean/phimean_r_{env.realizations}_Tf_{Tf}_h_{h}.png", dpi=100)