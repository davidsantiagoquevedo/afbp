import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import data_analysis

alpha = 0.5
realizations = 1200
Tf = 10
h = 0.05
sets = 10
fit_points = 10
num_bins = 40

# Mean and variance from trajectories
for set_index in range(sets):
    H = (2-alpha)/2
    set_label = str(set_index+1).zfill(3)
    set_index += 1
    
    env = angular_fbm(realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
    
    filepath = (
        f"data/r_{env.realizations}_"
        f"alpha_{env.alpha}_"
        f"H_{env.H}_"
        f"Tf_{env.Tf}_"
        f"h_{env.h}_"
        f"set_{set_label}.pkl"
    )
    env = angular_fbm.load(filepath)
    if set_index==1:
        env_multiset = env
    else:
        env_multiset.realizations += realizations
        env_multiset.phi_matrix = np.vstack((env_multiset.phi_matrix, env.phi_matrix))

env_multiset.compute_mean()
env_multiset.compute_variance()

mean = np.zeros(fit_points-1)
mean_fit = np.zeros(fit_points-1)
variance = np.zeros(fit_points-1)
variance_fit = np.zeros(fit_points-1)
time_period = int((Tf/h)/fit_points)
for fit_point in range(fit_points-1):
    
    time_index = fit_point*time_period + 1
    mean[fit_point] = env_multiset.mean[time_index]
    variance[fit_point] = env_multiset.variance[time_index]
    
    trajectories_points = env_multiset.phi_matrix[:, time_index]
    coeff = data_analysis.gauss_fit(trajectories_points, num_bins)
    coeff = coeff[0]
    mean_fit[fit_point] = coeff[1]
    variance_fit[fit_point] = coeff[2]
    
t = np.arange((fit_points-1))
fig, ax = plt.subplots()
ax.plot(t, mean, label = "sim")
ax.plot(t, mean_fit, ls=":", label = "fit")
fig.legend()
fig.savefig("plots/tests/pdf_fit_mean.png", dpi=500)

fig, ax = plt.subplots()
ax.plot(t, variance, marker='o', ls=":", label = "sim")
ax.plot(t, variance_fit,  marker='*', markersize=10, ls=":", label = "fit")
fig.legend()
fig.savefig("plots/tests/pdf_fit_variance.png", dpi=500)