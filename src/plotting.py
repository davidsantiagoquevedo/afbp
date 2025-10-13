# -- FUNCTIONS --
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import numpy as np
from scipy.special import gamma
import plotting_param as par
import data_analysis
from world import Angular, rModulus
import seaborn as sns
import colormaps as cmaps
cmap = cmaps.greenorange_6
palette = sns.color_palette([cmap(i) for i in range(cmap.N)])
sns.set_palette(palette)

# Analytic functions for fitting

def phi_propagator(phi, time, H, alpha, phi0=0):
    
    factor = np.sqrt(H/np.pi)*( gamma(H+1/2) / (gamma(2-alpha)*(time**(H+alpha-1))) )
    
    argument = -(H*gamma(H+1/2)**2 / gamma(2-alpha)**2) * ((phi - phi0)**2 / time**(2*H+2*alpha-2))
    
    return factor*np.exp(argument)

def phi_propagator_ansatz(phi, time, alpha, phi0=0):
    
    factor = np.sqrt( gamma(alpha+1) / (4*np.pi*(time**alpha)) )
    
    argument = - gamma(1+alpha)*(((phi - phi0)**2) / (4*time**(alpha)))
    
    return factor*np.exp(argument)

def phi_fBm_propagator_ansatz(phi, time, H, phi0=0):
    
    factor = np.sqrt( 1 / (2*np.pi*(time**(2*H))) )
    
    argument = - ((phi - phi0)**2) / (2*time**(2*H))
    
    return factor*np.exp(argument)

def phi_fBm_propagator_calvo(phi, time, H, phi0=0):
    
    
    return (np.sqrt(H/np.pi)) * (gamma(H+1/2)/(time**H)) * np.exp(-H*((gamma(H+1/2)*(phi-phi0)/(time**(H)))**2))

def phi_fBm_msd(time, H):
    # return (1/(2*H*(gamma(H+1/2)**2)))*(time**(2*H))
    return (time**(2*H))

def plot_trajectory(ax, x, y):

    ax.plot(x, y)

def plot_moment(ax, env, mom_type, variable, log = False, legend_label = True, pic_in_grid = False, color=None, label=''):

    """
    Plots a moment vector (msd or variance).
    
    Parameters:
    ----------
    ax : 

    env: class

    variable : str
        Can be 'sim' or 'sol': The moment was computed using L1 discretization of eom or of the convolution with the memory kernel, respectively

    moment_type : str
        Can be 'msd' or 'var' defining the type of moment, it will change y label.

    """

    style = par.msd_style[variable].copy()
    env.make_B_H()

    #color an curve from sim 
    if color is not None:
        style['c'] = par.lighten_color(color, 0.3) if log else par.lighten_color(color, 0.7)

    # legend label
    if legend_label:
        if log:
            style['label'] = 'analytic log' 
            style['label'] = rf"$H=${env.H}"
        if variable == 'sim' or variable == 'an':
            # style['label'] = rf"{style['label']} $\alpha_Q=${env.alpha} $H_Q=${env.H}"
            style['label'] = rf"$H_Q=${env.H}"
        
    if variable == 'sim':
        moment = env.msd if mom_type=='msd' else env.var#/env.var.max()
        time = env.t

    elif variable == 'sol':
        moment = env.msd_sol if mom_type=='msd' else env.var_sol
        time = env.t

    elif variable == 'an':
        moment = env.msd_an if mom_type=='msd' else env.var_an
        time = env.t[1:] if log else env.t

    line, = ax.plot(time, moment, **style)

    color = line.get_color()

    at = AnchoredText(label, prop=dict(size=par.size_labels_figures), frameon=False, loc='upper left')
    ax.add_artist(at)
    
    ax.tick_params(axis='both', labelsize=par.size_ticks)
    if pic_in_grid:
        ax.legend(fontsize = par.legend_size)
    else:
        ax.grid(':', zorder=0)    
        ax.legend(fontsize = par.legend_size,bbox_to_anchor=(1, 1))
        if mom_type == 'msd':
            mom_type = 'msd_phi' if isinstance(env, Angular) else 'msd_r'
        ax.set_ylabel(par.ylabel_map[mom_type], fontsize = par.axis_fontsize)
    ax.set_xlabel('t', fontsize = par.axis_fontsize)

    return color

def plot_pdf(ax, env, mode, time):
    
    trajectories_points = env.trajectories[:, time]

    # Analytitcal

    label = None
    variable = '\phi' if mode=='phi' else mode
    
    if time == int(env.Tf/(4*env.h)):
        label = r'$\frac{1}{\sqrt{{2\pi(\sigma)^2}}}$'+rf'$e^{{-\frac{{({variable}-\langle {variable} \rangle)^2}}{{2\sigma^2}}}}$'

    x, P = env.propagator(time)
    ax.plot(x, P, lw=2, ls=":", color = 'black', zorder=2, label = label)

    # Histogram and Fit
    num_bins=40
    hist, bin_edges = np.histogram(trajectories_points, density=True, bins=num_bins)
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2    
    
    # Get the fitted curve
    coeff = data_analysis.gauss_fit(trajectories_points, num_bins)
    coeff = coeff[0]
    hist_fit = data_analysis.gauss(bin_centres, *coeff) 

    ax.bar(bin_centres, hist, width=bin_edges[1] - bin_edges[0], alpha=0.5, zorder=0)
    ax.plot(bin_centres, hist_fit, lw=2, label=f'{(round(time*env.h, 2))}', zorder=1)
    
    ax.set_title(rf'$variable: \alpha = {env.alpha}, H = {env.H}, A_H = {round(env.A_H, 2)}$', fontsize=par.axis_fontsize)
    ax.set_xlabel(rf'${variable}$', fontsize=par.axis_fontsize)
    ax.set_ylabel(rf'$P({variable},t)$', fontsize=par.axis_fontsize)
    ax.tick_params(axis='both', labelsize=par.size_ticks)
    ax.legend(fontsize = par.legend_size)

def add_trend(ax, x0, xf, func, y0=1, text = "", xtext = False, dx = 0, dy = 0, fontsize = 15, **kwargs):
    t = np.arange(x0,xf,0.01)
    if xtext:
        xloc = xtext
    else:
        xloc = xf
    if kwargs:
        y = func(t, alpha = kwargs["alpha"])*y0
        ax.plot(t, y, color = "black", alpha = 1, ls = ":")
        ax.text(xloc + dx, func(xloc, alpha = kwargs["alpha"]) + dy, text, fontsize=fontsize)
    else:
        y = func(t)*y0
        ax.plot(t, y, color = "black", alpha = 1, ls = ":")
        ax.text(xloc + dx, func(xloc) + dy, text, fontsize = fontsize)

def t(t):
    return t

def t2(t):
    return t**2

def t3(t):
    return t**3

def talpha(t, **kwargs):
    alpha = kwargs["alpha"]
    return t**alpha