import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import parallelization

realizations = 1000
set_label = 1
alpha = 0.3
H = (2 - alpha) / 2
Tf = 10
h = 0.1

phi = AngularFBM(realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
phi.run()
# parallelization.run_trajectories_parallel(phi, batch_size=10)
phi_trajectories = phi.trajectories

env = xFBM(phi_trajectories = phi_trajectories, realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
# parallelization.run_trajectories_parallel(env, batch_size=10)
env.run()
# env.run_solution()
env.compute_msd()
# env.compute_msd_an()
# env.compute_msd_sol()
fig, ax = plt.subplots()
ax.plot(env.t, env.msd, label = 'sim')
# ax.plot(env.t, env.msd_an, label = 'an')
# ax.plot(env.t, env.msd_sol, label = 'sol')
fig.savefig(f"plots/tests/env_msd.png", dpi=100)

