import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import parallelization

realizations = 1000
set_label = 1
Tf = 1
L_type = 'L1'
alphaR = 1
HR = 0.8

hR = 0.01
phi = Angular(realizations=realizations, alpha=alphaR, H=HR, Tf=Tf, h=hR, L_type=L_type)
parallelization.run_trajectories_parallel(phi, batch_size=10)
phi_trajectories = phi.trajectories

alphaT=1
ups=1
AHT=1
HT=0.8
h = 0.01

x = xDirection(phi=phi, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h, ups=ups, AHT=AHT, L_type=L_type)
# parallelization.run_trajectories_parallel(x, batch_size=10)
x.run()

y = yDirection(phi=phi, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h, ups=ups, AHT=AHT, L_type=L_type)
# y = parallelization.run_trajectories_parallel(y, batch_size=10)
y.run()

r = rModulus(x=x, y=y, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h, L_type=L_type)
r.compute_r_modulus()

fig, ax = plt.subplots(figsize=(12, 9))
r.make_B_H()
time = r.t
r.compute_msd()
ax.plot(time, r.msd, label=f'sim')

r.compute_msd_an(total=True)
ax.plot(time, r.msd_an, ls='--', label='an')
ax.legend()
fig.savefig(f"plots/tests/testmsdtot_{L_type}_rvar_alphaT{alphaT}_HT{HT}_alphaR{alphaR}_HR{HR}_AHT{AHT}_r{realizations}_h{h}.png", dpi=100)
