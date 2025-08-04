import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import time
import matplotlib.cm as cm
import matplotlib.colors as mcolors

alphas = [0.9]
realizations = 1200
Tf = 10
h = 0.05
sets = 10
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
        print(env.phi_matrix.shape)
        if set_index==1:
            env_multiset = env
        else:
            env_multiset.realizations += realizations
            env_multiset.phi_matrix = np.vstack((env_multiset.phi_matrix, env.phi_matrix))
        
    env_multiset.compute_phi_correlation()
    env_multiset.compute_mean()
    env_multiset.compute_variance()
    print(len(env_multiset.mean))
        
    envs.append(env_multiset)
        
for alpha_index in range(len(alphas)):
    fig, ax = plt.subplots()
    env = envs[alpha_index]
    plotting.plot_msd(ax, env.phi_corr, env.h, env.alpha, env.H, 'phi')
    plotting.plot_msd(ax, env.phi_corr_sol, env.h, env.alpha, env.H, 'phi_sol')
    fig.tight_layout()
    plt.savefig(f"plots/phicorr_r_{env.realizations}_Tf_{Tf}_h_{h}.png", dpi=100)

    fig, ax = plt.subplots()
    plotting.plot_var(ax, env.variance, env.h, 'phi')
    plotting.plot_var(ax, env.variance_sol, env.h, 'phi_sol')
    fig.tight_layout()
    plt.savefig(f"plots/phivar_r_{env.realizations}_Tf_{Tf}_h_{h}.png", dpi=100)

    fig, ax = plt.subplots()
    plotting.plot_mean(ax, env.mean, env.h, 'phi')
    plotting.plot_mean(ax, env.mean_sol, env.h, 'phi_sol')
    fig.tight_layout()
    plt.savefig(f"plots/phimean_r_{env.realizations}_Tf_{Tf}_h_{h}.png", dpi=100)


    fig, ax = plt.subplots()
    plotting.plot_pdf(ax, env.phi_matrix, time = int(Tf/(4*h)), h = h, H = H, alpha = alpha)
    plotting.plot_pdf(ax, env.phi_matrix, time = int(Tf/(2*h)), h = h, H = H, alpha = alpha)
    plotting.plot_pdf(ax, env.phi_matrix, time = 199, h = h, H = H, alpha = alpha)
    fig.tight_layout()
    plt.savefig(f"plots/phipdf_r_{env.realizations}_Tf_{Tf}_h_{h}_alpha_{alpha}.png", dpi=100)
