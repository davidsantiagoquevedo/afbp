import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import time
import matplotlib.cm as cm
import matplotlib.colors as mcolors

start_time = time.time()

alphas = [0.5]
# H = 0.1
realizations = 1200
set_index = "001"
Tf = 10
h = 0.05
envs=[]


for alpha in alphas:    
    
    H = (2-alpha)/2
    
    env = angular_fbm(realizations=realizations, set_index=set_index, alpha=alpha, H=H, Tf=Tf, h=h)
    
    filepath = (
        f"data/r_{env.realizations}_"
        f"alpha_{env.alpha}_"
        f"H_{env.H}_"
        f"Tf_{env.Tf}_"
        f"h_{env.h}_"
        f"set_{set_index}.pkl"
    )
    env = angular_fbm.load(filepath)
    env.compute_phi_correlation()
    
    envs.append(env)
# print(env.phi_corr_sol)
fig, ax = plt.subplots()
for alpha_index in range(len(alphas)):
    env = envs[alpha_index]
    plotting.plot_msd(ax, env.phi_corr, env.h, env.alpha, env.H, 'phi')
    plotting.plot_msd(ax, env.phi_corr_sol, env.h, env.alpha, env.H, 'phi_sol')
fig.tight_layout()
plt.savefig(f"plots/phicorr_r_{realizations}_Tf_{Tf}_h_{h}.png", dpi=100)

# alpha=1
# env = envs[0]
# fig, ax = plt.subplots()
# plotting.plot_pdf(ax, env.phi_matrix, time = 100, h = h, H = H, alpha = alpha)
# plotting.plot_pdf(ax, env.phi_matrix, time = 500, h = h, H = H, alpha = alpha)
# plotting.plot_pdf(ax, env.phi_matrix, time = 1000, h = h, H = H, alpha = alpha)
# fig.tight_layout()
# plt.savefig(f"plots/phipdf_r_{realizations}_Tf_{Tf}_h_{h}_alpha_{alpha}.png", dpi=100)

# alpha=0.5
# env = envs[0]
# fig, ax = plt.subplots()
# plotting.plot_pdf(ax, env.phi_matrix, time = int(Tf/(4*h)), h = h, H = H, alpha = alpha)
# plotting.plot_pdf(ax, env.phi_matrix, time = int(Tf/(2*h)), h = h, H = H, alpha = alpha)
# plotting.plot_pdf(ax, env.phi_matrix, time = 900, h = h, H = H, alpha = alpha)
# fig.tight_layout()
# plt.savefig(f"plots/phipdf_r_{realizations}_Tf_{Tf}_h_{h}_alpha_{alpha}.png", dpi=100)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
