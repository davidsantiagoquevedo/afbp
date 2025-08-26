import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import parallelization

realizations = 1000
set_label = 5
alpha = 0.5
H = (2 - alpha) / 2
Tf = 10
h = 0.05

phi = AngularFBM(realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
# phi.run()
phi.trajectories = parallelization.run_trajectories_parallel(phi, batch_size=10)
phi.run_solution()
phi.compute_msd()
phi.compute_msd_an()
phi.compute_msd_sol()

fig, ax = plt.subplots()
ax.plot(range(len(phi.msd)), phi.msd, label = 'sim')
ax.plot(range(len(phi.msd)), phi.msd_an, label = 'an')
ax.plot(range(len(phi.msd)), phi.msd_sol, label = 'sol')
fig.savefig(f"plots/tests/phi_msd.png", dpi=100)

