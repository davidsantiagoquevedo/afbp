
from world import *
import matplotlib.pyplot as plt
import plotting
import time

start_time = time.time()

alphas = [0.5]
run = False
envs=[]

for alpha in alphas:
    
    H = (2 - alpha) / 2
    
    env = Env(numb_agents=1000, alpha=alpha, H=H, Tf=5, h=1e-3)
    
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
        # print(filepath)
        # env = Env.load(filepath='data/numbag_1000_alpha_0.50_H_0.75_Tf_5_h_0.001.pkl')
        env = Env.load(filepath)
    
    envs.append(env)

fig, ax = plt.subplots()
for alpha_index in range(len(alphas)):
    env = envs[alpha_index]
    plotting.plot_msd(ax, env.phi_corr, env.h, env.alpha, 'phi')
fig.tight_layout()
plt.savefig(f"phi_corr.pdf")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
