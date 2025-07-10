
from world import *
import matplotlib.pyplot as plt
import plotting
import time


start_time = time.time()

alphas = [1, 0.5]
run = True
envs=[]

for alpha in alphas:
    
    H = (2 - alpha) / 2
    
    env = Env(numb_agents=1000, alpha=alpha, H=H, Tf=10, h=1e-3)
    
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
plt.savefig(f"phi_corr.pdf")


# alpha=1
# fig, ax = plt.subplots()
# plotting.plot_pdf(ax, env.phi_matrix, time = 100, alpha = alpha)
# plotting.plot_pdf(ax, env.phi_matrix, time = 500, alpha = alpha)
# plotting.plot_pdf(ax, env.phi_matrix, time = 1000, alpha = alpha)
# fig.tight_layout()
# plt.savefig(f"phi_histogram.pdf")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
