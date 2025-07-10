# -- PARAMETERS --

legend_size = 15
axis_fontsize = 19
size_ticks = 20
marker_size = 10

msd_style = {
    'phi': dict(c = 'dodgerblue', lw=2, label = 'sim')  
}

# -- FUNCTIONS --
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gamma


def plot_msd(ax, msd, delta_t, alpha, H, variable):

    time = np.arange(0,len(msd))*delta_t

    ax.plot(time, msd, lw=2, zorder=1, label=fr'$\alpha$={alpha}')
    # ax.plot(time, (gamma(2*H)**2/(2*H*(gamma(H+1/2)**2)))*time**(alpha), c='red', zorder=1)

    ax.set_xlabel('t', fontsize = axis_fontsize)
    ax.tick_params(axis='both', labelsize=size_ticks)
    ax.set_ylabel(r'MSD$\langle (\phi(t)-\phi_0)^2 \rangle$', fontsize = axis_fontsize)
    ax.grid(':')
    ax.legend(fontsize = legend_size)

def plot_pdf(ax, phi_matrix, time, alpha):
    
    trajectories_points = phi_matrix[:, time]
    
    ax.hist(trajectories_points, bins=150, color='skyblue', edgecolor='black', alpha=0.6, label=rf't={time}', density=True)
    ax.legend(fontsize = legend_size)

