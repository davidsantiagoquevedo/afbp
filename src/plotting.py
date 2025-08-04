# -- PARAMETERS --

legend_size = 15
axis_fontsize = 19
size_ticks = 20
marker_size = 10

msd_style = {
    'phi': dict(lw=2, label = 'sim'),  
    'phi_sol': dict(lw=2, ls=':', label = 'sol')  
}

# -- FUNCTIONS --
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gamma
import scipy.stats as stats
import pandas as pd
import data_analysis
# plt.style.use("plotting_style.mplstyle")

# Analytic functions for fitting

def phi_propagator(phi, time, H, alpha, phi0=0):
    
    factor = np.sqrt(H/np.pi)*( gamma(H+1/2) / (gamma(2-alpha)*(time**(H+alpha-1))) )
    
    argument = -(H*gamma(H+1/2)**2 / gamma(2-alpha)**2) * ((phi - phi0)**2 / time**(2*H+2*alpha-2))
    
    return factor*np.exp(argument)

def phi_propagator_ansatz(phi, time, alpha, phi0=0):
    
    factor = np.sqrt( gamma(alpha+1) / (4*np.pi*(time**alpha)) )
    
    argument = - gamma(1+alpha)*(((phi - phi0)**2) / (4*time**(alpha)))
    
    return factor*np.exp(argument)

# Plotting
def plot_msd(ax, msd, delta_t, alpha, H, variable):

    time = np.arange(0,len(msd))*delta_t

    ax.plot(time, msd, **msd_style[f'{variable}'])
    # print((gamma(2*H)**2/(2*H*(gamma(H+1/2)**2))))
    msd_anl = ((gamma(2*H)**2)/(H*(gamma(H+1/2)**2)))*time**(alpha)
    msd_anl = (2/gamma(alpha+1))*time**(alpha)
    ax.plot(time, msd_anl, c='red', zorder=1)

    ax.set_xlabel('t', fontsize = axis_fontsize)
    ax.tick_params(axis='both', labelsize=size_ticks)
    ax.set_ylabel(r'MSD$\langle (\phi(t)-\phi_0)^2 \rangle$', fontsize = axis_fontsize)
    ax.grid(':')
    ax.legend(fontsize = legend_size)

def plot_mean(ax, mean, delta_t, variable):

    time = np.arange(0,len(mean))*delta_t

    ax.plot(time, mean, **msd_style[f'{variable}'])


    ax.set_xlabel('t', fontsize = axis_fontsize)
    ax.tick_params(axis='both', labelsize=size_ticks)
    ax.set_ylabel(r'$\langle \phi(t) \rangle$', fontsize = axis_fontsize)
    ax.grid(':')
    
def plot_var(ax, variance, delta_t, variable):

    time = np.arange(0,len(variance))*delta_t

    ax.plot(time, variance, **msd_style[f'{variable}'])

    ax.set_xlabel('t', fontsize = axis_fontsize)
    ax.tick_params(axis='both', labelsize=size_ticks)
    ax.set_ylabel(r'var', fontsize = axis_fontsize)
    ax.grid(':')
    ax.legend(fontsize = legend_size)


def plot_pdf(ax, phi_matrix, time, h, H, alpha, phi0=0):
    
    trajectories_points = phi_matrix[:, time]

    phi_range = np.arange(np.min(trajectories_points), np.max(trajectories_points), 1e-3)
    propagator = phi_propagator_ansatz(phi_range, time*h, H, alpha)
    ax.plot(phi_range, propagator, lw=2, ls=":", color = 'black', zorder=1)
    
    num_bins=40
    hist, bin_edges = np.histogram(trajectories_points, density=True, bins=num_bins)
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2    
    
    # Get the fitted curve
        # Get the fitted curve
    coeff = data_analysis.gauss_fit(trajectories_points, num_bins)
    coeff = coeff[0]
    hist_fit = data_analysis.gauss(bin_centres, *coeff) 

    ax.bar(bin_centres, hist, width=bin_edges[1] - bin_edges[0], alpha=0.6)
    ax.plot(bin_centres, hist_fit, label='Fitted data')
    
    ax.legend(fontsize = legend_size)

