from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
from os import sys
sys.path.append("src/")
import plt_parameters as par
from scipy.special import gamma

alpha = 0.3       
T_total = 100     # total time span
N = int(1e5)         # number of samples

dt = T_total / N
t = (np.arange(N) - N//2) * dt
print(t)

t = t + 1e-8
f_raw = (np.abs(t))**(-alpha) / gamma(1 - alpha)

F = np.fft.fftshift(np.fft.fft(np.fft.fftshift(f_raw)) )
omega = np.fft.fftshift(np.fft.fftfreq(N, d=dt))
print(omega)

C = 2 * np.sin(np.pi*alpha/2)
F_theory= C * (np.abs(omega) + 1e-30)**(alpha-1)

fig, ax = plt.subplots()
ax.plot(t, f_raw, label = 'sim')
ax.set_xlabel(r'$t$', fontsize = par.axis_fontsize)
ax.tick_params(axis='both', labelsize = par.size_ticks)
ax.set_ylabel(r'$f(t)$', fontsize = par.axis_fontsize)
# ax.legend(fontsize = par.legend_size)
ax.grid(':')
fig.tight_layout()
fig.savefig(f"plots/tests/fourier_trans_time.png", dpi=100)

fig, ax = plt.subplots()
# ax.plot(t, f_raw, label = 'sim')
plt.plot(omega, np.abs(F), label="sim")
# plt.plot(omega, F_theory, label=r"analy")
ax.set_xlabel(r'$\omega$', fontsize = par.axis_fontsize)
ax.tick_params(axis='both', labelsize = par.size_ticks)
ax.set_ylabel(r'$f(\omega)$', fontsize = par.axis_fontsize)
ax.legend(fontsize = par.legend_size)
ax.grid(':')
fig.tight_layout()
fig.savefig(f"plots/tests/fourier_trans_freq.png", dpi=100)
