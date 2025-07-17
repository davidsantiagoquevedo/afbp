# -- PARAMETERS --

legend_size = 15
axis_fontsize = 19
size_ticks = 20
marker_size = 10

msd_style = {
    'phi': dict(c = 'dodgerblue', lw=2, label = 'sim'),  
    'phi_sol': dict(c = 'magenta', lw=2, label = 'sol')  
}

# -- FUNCTIONS --
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gamma
import scipy.stats as stats
import pandas as pd

# Analytic functions for fitting

def phi_propagator(phi, time, H, alpha, phi0=0):
    
    factor = np.sqrt(H/np.pi)*( gamma(H+1/2) / (gamma(2-alpha)*(time**(H+alpha-1))) )
    
    argument = -(H*gamma(H+1/2)**2 / gamma(2-alpha)**2) * ((phi - phi0)**2 / time**(2*H+2*alpha-2))
    
    return factor*np.exp(argument)

# Plotting
def plot_msd(ax, msd, delta_t, alpha, H, variable):

    time = np.arange(0,len(msd))*delta_t

    ax.plot(time, msd, **msd_style[f'{variable}'])
    # ax.loglog(time, msd, lw=2, zorder=1, label=fr'$\alpha$={alpha}')
    # print((gamma(2*H)**2/(2*H*(gamma(H+1/2)**2))))
    ax.plot(time, ((gamma(2*H)**2)/(H*(gamma(H+1/2)**2)))*time**(alpha), c='red', zorder=1)

    ax.set_xlabel('t', fontsize = axis_fontsize)
    ax.tick_params(axis='both', labelsize=size_ticks)
    ax.set_ylabel(r'MSD$\langle (\phi(t)-\phi_0)^2 \rangle$', fontsize = axis_fontsize)
    ax.grid(':')
    ax.legend(fontsize = legend_size)

def plot_pdf(ax, phi_matrix, time, h, H, alpha, phi0=0):
    
    trajectories_points = phi_matrix[:, time]
    trajectories_points = pd.Series(trajectories_points)
    trajectories_points.hist(ax=ax, bins=20, alpha=0.6, label=rf't={time}', density=True, zorder=0)
    
    phi_range = np.arange(np.min(trajectories_points), np.max(trajectories_points), 1e-3)
    # phi_range = np.arange(-1, 1, 1e-2)
    propagator = phi_propagator(phi_range, time*h, H, alpha)
    
    ax.plot(phi_range, propagator, lw=2, zorder=1, label=rf't={time}')
    
    
    ax.legend(fontsize = legend_size)

