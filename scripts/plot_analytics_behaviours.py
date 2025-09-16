import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

nu=1           
Tf = 10
h = 0.01

# PHI VAR
alphaR = np.array([1, 0.7, 0.5, 0.3, 0.2])
HR = (2 - alphaR) / 2

fig, ax = plt.subplots(figsize=(9, 7))
for idx, alpha in enumerate(alphaR):
    H = HR[idx]
    phi = Angular(alpha=alpha, H=H, Tf=Tf, h=h)
    phi.compute_msd_an()
    plotting.plot_moment(ax, phi, 'msd', 'an')

fig.tight_layout()
fig.savefig(f"plots/analytics/phi_alphaR{alphaR}_HR{HR}_Tf{Tf}_h{h}_nu{nu}.png", dpi=100)

# R MSD ROTATIONAL
alphaT = np.array([1, 0.7, 0.5, 0.3, 0.2])
HT = (2 - alphaR) / 2
alphaR = alphaT
HR = HT

fig, ax = plt.subplots(figsize=(9, 7))
for idx, alpha in enumerate(alphaT):
    H = HT[idx]
    alphaRi = alphaR[idx]
    HRi = HR[idx]

    r = rModulus(alpha=alpha, H=H, alphaR=alphaRi, HR=HRi, nu=nu, Tf=Tf, h=h)

    r.compute_msd_an(total=False)
    plotting.plot_moment(ax, r, 'msd', 'an')

fig.tight_layout()
fig.savefig(f"plots/analytics/ra_alphaT{alphaT}_HT{HT}_alphaR{alphaR}_HR{HR}_Tf{Tf}_h{h}_nu{nu}.png", dpi=100)

# R MSD TOTAL
alphaT = np.array([1, 0.7, 0.5, 0.3, 0.2])
HT = (2 - alphaR) / 2
alphaR = alphaT
HR = HT

fig, ax = plt.subplots(figsize=(9, 7))
for idx, alpha in enumerate(alphaT):
    H = HT[idx]
    alphaRi = alphaR[idx]
    HRi = HR[idx]

    r = rModulus(alpha=alpha, H=H, alphaR=alphaRi, HR=HRi, nu=nu, Tf=Tf, h=h)

    r.compute_msd_an()
    plotting.plot_moment(ax, r, 'msd', 'an')

fig.tight_layout()
fig.savefig(f"plots/analytics/r_alphaT{alphaT}_HT{HT}_alphaR{alphaR}_HR{HR}_Tf{Tf}_h{h}_nu{nu}.png", dpi=100)
