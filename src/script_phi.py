
from world import *
import matplotlib.pyplot as plt
import plotting
import time

start_time = time.time()

alpha = 0.5
H = (2 - alpha)/2
env = Env(numb_agents=10, alpha = alpha, H = H, Tf = 2, h=1e-3)

env.compute_phi_correlation()

fig, ax = plt.subplots()
plotting.plot_msd(ax, env.phi_corr, env.h, 'phi')
fig.tight_layout()
plt.savefig(f"phi_corr.pdf")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
