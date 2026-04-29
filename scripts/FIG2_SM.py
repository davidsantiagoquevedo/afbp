import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities
import plotting_param as par
plt.style.use("src/plotting_style.mplstyle")
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

mode = 'phi'
Tf = 10.0
start_set=1
realizations = 1000
sets = 3
L_type = 'L1'
DATA_PATH = 'data'
eta=1
t_ref=1

def plot_deltaphistat(ax, t_ref, env, color, color_cos):
    t_ref_index = int(t_ref/h)

    # Delta phi
    matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()
    var_ref = np.var(matrix_ref, axis=0)
    time = np.arange(0, len(var_ref))*h
    ax.plot(time, var_ref, c = color, lw=2, label = r'$\sigma_{\Delta_{\phi}}^2$')

    analytics = env.compute_var_an(time=np.abs(time-t_ref))
    ax.plot(time, analytics, c=par.lighten_color(color, 0.7), lw=5, ls="--")

    # Cos Delta phi
    # 
    mean_cos_deltaphi =  np.mean(np.cos(matrix_ref), axis=0)
    analytics = np.exp(-analytics/2)

    ax.plot(time, mean_cos_deltaphi, c = color_cos, lw=2, label = r'$\langle \cos\Delta \phi \rangle$')
    ax.plot(time, analytics, c=par.lighten_color(color_cos, 0.7), lw=3, ls="--", label = r'$e^{-\sigma^2_{\Delta\phi}/2}$') 

    ax.tick_params(axis='both', labelsize=par.size_ticks)

fig, ax = plt.subplots(2, 4, figsize = (20, 10))
##########################################################

hs = [0.005, 0.005, 0.005, 0.001]
color_order = [4,0,2,0]
alpha_color = [0.3,0.5,0.7]
times_plot = [2,3,9]
caption_letter = [("(a)","(e)"),("(b)","(f)"),("(c)","(g)"),("(d)","(h)")]

for i, alphaR in enumerate([1.0, 0.7, 0.5, 0.3]):
    HR = 1 - alphaR/2
    h = hs[i]
    t_ref_index = int(t_ref/h)
    times_plot_index = [int(t/h) for t in times_plot]
    legend = True

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
    matrix_ref = (env.trajectories.transpose() - env.trajectories[:, t_ref_index]).transpose()
    env.trajectories = matrix_ref
    for j, t in enumerate(times_plot_index):

        plotting.qq_plot(data=matrix_ref, ax=ax[1,i], time=t, color=colors[color_order[j]], alpha_color = alpha_color[j])
        
        if j == 2:
            legend_an = True 
        else:
            legend_an = False
        plotting.plot_pdf(ax[0,i], env, mode, time=t, tref = t_ref, legend=legend, legend_an=legend_an, xy_label=False, color = colors[color_order[j]], alpha_color = alpha_color[j])
        handles, labels = ax[0,i].get_legend_handles_labels()
        #ax[0,i].get_legend().remove()
    
    plotting.add_caption_letter(ax=ax[0,i], cap=caption_letter[i][0], xloc=-0.15, yloc=1.05)
    plotting.add_caption_letter(ax=ax[1,i], cap=caption_letter[i][1], xloc=-0.15, yloc=1.05)
    ax[0,i].set_title(fr'$\alpha_R={alphaR}, H_R$={HR}')
    ax[0,i].set_xlabel(rf'$\Delta \phi$')
    ax[1,i].set_xlabel("Theoretical Quantiles")
ax[0,0].set_ylabel(rf'$P(\Delta \phi,t)$')
ax[1,0].set_ylabel("Sample Quantiles")



fig.legend(handles, labels, bbox_to_anchor = (0.95, 1.05), ncol = 4)


fig.tight_layout()
fig.savefig(f"plots/paper/fig2_SM.png", dpi=300)
