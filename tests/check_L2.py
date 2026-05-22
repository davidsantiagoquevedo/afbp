import sys
sys.path.append("src/")
from world import *
import plotting
import matplotlib.pyplot as plt
import utilities
plt.style.use("src/plotting_style.mplstyle") 


realizations = 1000
start_set = 0
sets = 8
start_set = 0
data_path = 'data_tests'
ups = 20.

hv = [0.005, 0.005, 0.001]

colors = ["#FEBA27", "#76B3D0", "#F4BAEA"]

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
for ai, a in enumerate([0.7, 0.5, 0.3]):

    h = hv[ai]

    Tf = 10
    phi_l1 = utilities.read_env(mode='phi', L_type = 'L1', alpha=a, H=(2 - a) / 2, alphaR=a, HR=(2 - a) / 2, realizations=1000, Tf=Tf, h=h, start_set=start_set, sets=sets, path = data_path)
    phi_l1.compute_msd()
    phi_l2 = utilities.read_env(mode='phi', L_type = 'L2', alpha=a, H=(2 - a) / 2, alphaR=a, HR=(2 - a) / 2, realizations=1000, Tf=Tf, h=h, start_set=start_set, sets=sets, path = data_path)
    phi_l2.compute_msd()
                

    plotting.plot_moment(ax[0], phi_l1, color = colors[ai], variable='sim', mom_type='msd', ci=True, ci_bars=True, sample = True, sample_size = 41,  sampling_type = 'loglin', max_value = 1, legend_id = 'alphaQ', legend=True, rescale=ups**2)
    plotting.plot_moment(ax[0], phi_l2, color = 'black', variable='sim', mom_type='msd', ci=True, ci_bars=True, sample = True, sample_size = 41,  sampling_type = 'loglin', max_value = 1, rescale=ups**2)
    # phi_l1.compute_msd_an()
    # plotting.plot_moment(ax, phi_l1, variable='an', mom_type='msd')

    Tf = 20.
    r_l1 = utilities.read_env(mode='r', L_type = 'L1', alpha=a, H=(2 - a) / 2, alphaR=a, HR=(2 - a) / 2, realizations=1000, Tf=Tf, h=h, ups=ups, start_set=1, sets=sets, path = data_path)
    r_l1.compute_msd()
    r_l2 = utilities.read_env(mode='r', L_type = 'L2', alpha=a, H=(2 - a) / 2, alphaR=a, HR=(2 - a) / 2, realizations=1000, Tf=Tf, h=h, ups=ups, start_set=1, sets=sets, path = data_path)
    r_l2.compute_msd()

    plotting.plot_moment(ax[1], r_l1, color = colors[ai], variable='sim', mom_type='msd', ci=True, ci_bars=True, sample = True, sample_size = 41,  sampling_type = 'loglin', max_value = 1, legend_id = 'alphaQ', legend=True, rescale=ups**2)
    L2legend = True if ai==2 else False
    plotting.plot_moment(ax[1], r_l2, color = 'black', variable='sim', mom_type='msd', ci=True, ci_bars=True, sample = True, sample_size = 41,  sampling_type = 'loglin', max_value = 1, legend_id = r'L$2$', legend=L2legend, rescale=ups**2)

handles, legend = ax[1].get_legend_handles_labels()
ax[0].get_legend().remove()
ax[1].get_legend().remove()
fig_leg = fig.legend(handles, legend, bbox_to_anchor = (0.93,1.07), ncol = 4)

ax[0].set_ylabel(fr'$\langle (\phi(t)-\phi_0)^2 \rangle$')
ax[1].set_ylabel(fr'$\langle (\boldsymbol{{r}}(t)-\boldsymbol{{r}}_0)^2 \rangle/\upsilon^2\tau_R^2$')
ax[0].set_xlabel(r'$t/\tau_{R}$')
ax[1].set_xlabel(r'$t/\tau_{R}$')
fig.savefig('plots/tests/test_L2.png', dpi=100)