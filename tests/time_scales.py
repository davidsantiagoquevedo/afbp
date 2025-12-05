import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
from scipy.special import gamma
plt.style.use("src/plotting_style.mplstyle")

Tf = 10
h = 0.1

alpha = np.linspace(0,1,100)
tau_a1 = np.zeros(alpha.shape)
tau_a2 = np.zeros(alpha.shape)
tau_p = np.zeros(alpha.shape)
tau_2 = np.zeros(alpha.shape)
tau_1 = np.zeros(alpha.shape)

for k, a in enumerate(alpha):
    ups1 = 1
    r1 = rModulus(alpha=a, H=(2 - a) / 2, alphaR=a, HR=(2 - a) / 2, ups=ups1, Tf=Tf, h=h)
    ups2 = 3
    r2 = rModulus(alpha=a, H=(2 - a) / 2, alphaR=a, HR=(2 - a) / 2, ups=ups2, Tf=Tf, h=h)
    tau_a1[k] = r1.calc_crossover_time()
    tau_a2[k] = r2.calc_crossover_time()
    tau_2[k] = r1.calc_ballistic_time()
    tau_p[k] = r1.calc_persistance_time()
    tau_1[k] = r1.calc_relaxation_time()
    

fig, ax = plt.subplots()
ax.plot(alpha, tau_a1, label = rf"$\tau_{{\alpha_T}}(\upsilon={ups1})$", color = "red", ls="-")
ax.plot(alpha, tau_a2, label = rf"$\tau_{{\alpha_T}}(\upsilon={ups2})$", color = "grey", ls="-")
ax.plot(alpha, tau_2, label = r"$\tau_{2}$", color = "grey", ls="--")
ax.plot(alpha, tau_p, label = r"$\tau_{p}$", color = "grey", ls=":")
ax.plot(alpha, tau_1, label = r"$\tau_{1}$", color = "grey", ls="-.")
ax.set_xlabel(r"$\alpha$")
ax.set_ylabel(r"$\tau$")
ax.set_ylim((0.1,10000))
ax.set_yscale('log')
ax.legend(loc='best')
plt.savefig("plots/tests/time-scales.png")
