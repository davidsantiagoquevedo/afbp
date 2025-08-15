import sys
sys.path.append("src/")
import utilities
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

alphas = [0.5]
realizations = 3000
Tf = 10
h = 0.05
sets = 1
kBT = 1

t_ref = 5
t_ref_index = int(t_ref/h)

envs = utilities.read_envs(alphas, sets, Tf, h, realizations)

phi_matrix_ref = (envs[0].phi_matrix.transpose() - envs[0].phi_matrix[:, t_ref_index]).transpose()

var_ref = np.var(phi_matrix_ref, axis=0)
time = np.arange(0, len(var_ref))*h
# analytics = np.abs(time-t_ref_index)**(alphas[0])
# analytics = (kBT/np.pi)*(1/np.tan(alphas[0]*np.pi/2))*(gamma(1-alphas[0])/alphas[0])*np.abs(time-t_ref)**(alphas[0])/2
# analytics = (kBT)*(1/np.tan(alphas[0]*np.pi/2))*(gamma(1-alphas[0])/alphas[0])*np.abs(time-t_ref)**(alphas[0])
analytics = -(kBT/np.pi)*(1/np.tan(alphas[0]*np.pi/2))*(gamma(-alphas[0]))*np.abs(time-t_ref)**(alphas[0])

print(np.max(analytics)/np.max(var_ref))

fig, ax = plt.subplots()
ax.plot(time, var_ref, label = 'sim')
ax.plot(time, analytics, label='analy')
# ax.plot(time, var_ref/var_ref.max(), label = 'sim')
# ax.plot(time, analytics/analytics.max(), label='analy')
fig.savefig(f"plots/tests/delta_phi_var.png", dpi=100)
