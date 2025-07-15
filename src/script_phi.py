
from world import *
import matplotlib.pyplot as plt
import plotting
import time


start_time = time.time()

# alphas = [0.1, 0.3, 0.5, 0.7, 0.9, 1]
alphas = [0.5]
# H = 0.1
realizations = 100
Tf = 1
h = 1e-3    
run = True
envs=[]

for alpha in alphas:    
    
    H = (2-alpha)/2 
    
    env = afbm(realizations=realizations, alpha=alpha, H=H, Tf=Tf, h=h)
    
    if run:
        print("----Running for alpha", env.alpha)
        env.run()
        env.compute_phi_correlation()
        
        env.save(folder="data")
        
    else:
        filepath = (
            f"data/r_{env.realizations}_"
            f"alpha_{env.alpha}_"
            f"H_{env.H}_"
            f"Tf_{env.Tf}_"
            f"h_{env.h}.pkl"
        )
        env = afbm.load(filepath)
    
    envs.append(env)

fig, ax = plt.subplots()
for alpha_index in range(len(alphas)):
    env = envs[alpha_index]
    plotting.plot_msd(ax, env.phi_corr, env.h, env.alpha, env.H, 'phi')
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
# plotting.plot_pdf(ax, env.phi_matrix, time = 100, h = h, H = H, alpha = alpha)
# plotting.plot_pdf(ax, env.phi_matrix, time = 500, h = h, H = H, alpha = alpha)
# plotting.plot_pdf(ax, env.phi_matrix, time = 1000, h = h, H = H, alpha = alpha)
# fig.tight_layout()
# plt.savefig(f"plots/phipdf_numbag_{numb_agents}_Tf_{Tf}_h_{h}_alpha_{alpha}.png", dpi=100)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
