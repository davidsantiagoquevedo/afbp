# -- PARAMETERS --

legend_size = 15
axis_fontsize = 19
size_ticks = 20
marker_size = 10

msd_style = {
    'phi': dict(lw=2, label = 'sim'),  
    'phi_sol': dict(lw=2, ls=':', label = 'sol'),  
    'an': dict(lw=2, label = 'analytic'),  
    'fit': dict(lw=2, marker = 'o', label = 'fit')  
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

def phi_msd(time, alpha):
    # msd_anl = ((gamma(2*H)**2)/(H*(gamma(H+1/2)**2)))*time**(alpha)
    return (2/gamma(alpha+1))*time**(alpha)

def phi_mean(time):
    return np.zeros(len(time))
def phi_var(time, alpha):
    return (2*(time**alpha))/gamma(alpha+1)

# def phi_var(time):

# Plotting
def plot_msd(ax, env, variable):

    style = msd_style[variable].copy()
    style['label'] = rf"{style['label']} $\alpha=${env.alpha}"

    if variable == 'phi':
        msd = env.phi_corr
        time = np.arange(0,len(msd))*env.h
    elif variable == 'phi_sol':
        msd = env.phi_corr_sol
        time = np.arange(0,len(msd))*env.h
    else:
        time = np.arange(0, env.n)*env.h
        msd = phi_msd(time, env.alpha)
    
    ax.plot(time, msd, **style)

    ax.set_xlabel('t', fontsize = axis_fontsize)
    ax.tick_params(axis='both', labelsize=size_ticks)
    ax.set_ylabel(r'MSD$\langle (\phi(t)-\phi_0)^2 \rangle$', fontsize = axis_fontsize)
    ax.grid(':')
    ax.legend(fontsize = legend_size)

def plot_moment(ax, env, variable, mom_type):

    """
    Plots a moment vector (mean or variance).
    
    Parameters:
    ----------
    ax : 

    env: class

    variable : str
        Can be 'phi' or 'phi_sol'. The moment was computed using L1 discretization of eom or of the convolution with the memory kernel, respectively

    moment_type : str
        Can be 'mean' or 'var' defining the type of moment, it will change y label.

    ...
    
    Returns:

    """

    style = msd_style[variable].copy()
    style['label'] = rf"{style['label']} $\alpha={env.alpha}$"

    if variable in ['phi', 'phi_sol']:
        attr = f"{mom_type}" if variable == 'phi' else f"{mom_type}_sol"
        y = getattr(env, attr)
        time = np.arange(0, len(y)) * env.h

    elif variable == 'an':
        time = np.arange(0, env.n) * env.h
        y = phi_var(time, env.alpha) if mom_type == 'var' else phi_mean(time)

    elif variable == 'fit':
        fit_indices = np.arange(1, env.n,50) 
        time = np.array(fit_indices) * env.h

        mean_fit = []
        var_fit = []

        for i in fit_indices:
            samples = env.phi_matrix[:, i]
            coeff, _ = data_analysis.gauss_fit(samples, bins=40)
            A, mu, sigma = coeff

            mean_fit.append(mu)
            var_fit.append(sigma**2)

        y = var_fit if mom_type == 'var' else mean_fit

    else:
        raise ValueError(f"Unknown variable: {variable}")

    ax.plot(time, y, **style)

    ylabel_map = {
        'var': r'$\sigma^2(t)$',
        'mean': r'$\langle \phi(t) \rangle$'
    }
    ax.set_xlabel('t', fontsize=axis_fontsize)
    ax.set_ylabel(ylabel_map[mom_type], fontsize=axis_fontsize)
    ax.tick_params(axis='both', labelsize=size_ticks)
    ax.grid(':')
    ax.legend(fontsize=legend_size)

def plot_pdf(ax, env, time):
    
    trajectories_points = env.phi_matrix[:, time]

    # Ansatz
    phi_range = np.arange(np.min(trajectories_points), np.max(trajectories_points), 1e-3)
    propagator = phi_propagator_ansatz(phi_range, time*env.h, env.alpha)
    label = None
    if time == int(env.Tf/(4*env.h)):
        label = 'ansatz'
    ax.plot(phi_range, propagator, lw=2, ls=":", color = 'black', zorder=2, label = label)
    
    # Histogram and Fit
    num_bins=40
    hist, bin_edges = np.histogram(trajectories_points, density=True, bins=num_bins)
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2    
    
    # Get the fitted curve
    coeff = data_analysis.gauss_fit(trajectories_points, num_bins)
    coeff = coeff[0]
    hist_fit = data_analysis.gauss(bin_centres, *coeff) 

    ax.bar(bin_centres, hist, width=bin_edges[1] - bin_edges[0], alpha=0.5, zorder=0)
    ax.plot(bin_centres, hist_fit, lw=2, label=f'{time}', zorder=1)
    
    ax.set_title(rf'$\alpha=${env.alpha}')
    ax.legend(fontsize = legend_size)

