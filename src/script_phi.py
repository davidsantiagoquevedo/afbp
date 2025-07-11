
from world import *
import matplotlib.pyplot as plt
import plotting
import time


start_time = time.time()

alphas = [1, 0.5]
H = 0.7
numb_agents = 1000
Tf = 10
h = 1e-3
run = False
envs=[]

for alpha in alphas:
    
    H = (2 - alpha) / 2
    
    env = Env(numb_agents=numb_agents, alpha=alpha, H=H, Tf=Tf, h=h)
    
    if run:
        print("----Running for alpha", env.alpha)
        env.define_agents()
        env.run()
        env.compute_phi_correlation()
        
        env.save(folder="data")
        
    else:
        filepath = (
            f"data/numbag_{env.numb_agents}_"
            f"alpha_{env.alpha}_"
            f"H_{env.H}_"
            f"Tf_{env.Tf}_"
            f"h_{env.h}.pkl"
        )
        env = Env.load(filepath)
    
    envs.append(env)

fig, ax = plt.subplots()
for alpha_index in range(len(alphas)):
    env = envs[alpha_index]
    plotting.plot_msd(ax, env.phi_corr, env.h, env.alpha, env.H, 'phi')
fig.tight_layout()
plt.savefig(f"plots/phicorr_numbag_{numb_agents}_Tf_{Tf}_h_{h}.png", dpi=100)


alpha=1
H=0.7
env = envs[1]
fig, ax = plt.subplots()
plotting.plot_pdf(ax, env.phi_matrix, time = 100, h = h, H = H, alpha = alpha)
plotting.plot_pdf(ax, env.phi_matrix, time = 500, h = h, H = H, alpha = alpha)
plotting.plot_pdf(ax, env.phi_matrix, time = 1000, h = h, H = H, alpha = alpha)
fig.tight_layout()
plt.savefig(f"plots/phipdf_numbag_{numb_agents}_Tf_{Tf}_h_{h}_alpha_{alpha}.png", dpi=100)

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
