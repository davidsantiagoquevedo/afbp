# -- FUNCTIONS --
from matplotlib.offsetbox import AnchoredText
import numpy as np
import plotting_param as par
import data_analysis
from world import Angular

def plot_trajectory(ax, x, y):

    ax.plot(x, y)

def plot_moment(ax, env, mom_type, variable, legend_id = 'H',  log = False, legend_label = True, pic_in_grid = False, color=None, label='', std = False, legend = True):

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
        # style['c'] = par.lighten_color(color, 0.3) if log else par.lighten_color(color, 0.7)
        style['c'] = color

    # legend label
    if legend_label:
        if log:
            style['label'] = 'analytic log' 
            style['label'] = rf"$H=${env.H}"
        if variable == 'sim' or variable == 'an':
            # style['label'] = rf"{style['label']} $\alpha_Q=${env.alpha} $H_Q=${env.H}"
            if legend_id == 'H':
                style['label'] = rf"$H_Q=${env.H}"
            if legend_id == 'alpha':
                style['label'] = rf"$\alpha_Q=${env.alpha}"
            if legend_id == 'alphaR':
                style['label'] = rf"$\alpha_R=${env.alphaR}"
            if legend_id == 'alphaT':
                style['label'] = rf"$\alpha_T=${env.alphaT}"

        
    if variable == 'sim':
        moment = env.msd if mom_type=='msd' else env.var#/env.var.max()
        # time = env.t
        time = np.linspace(0, env.Tf, len(moment))

    elif variable == 'sol':
        moment = env.msd_sol if mom_type=='msd' else env.var_sol
        time = env.t

    elif variable == 'an':
        moment = env.msd_an if mom_type=='msd' else env.var_an
        time = env.t[1:] if log else env.t

    line, = ax.plot(time, moment, **style)

    color = line.get_color()

    if std:
        std_msd = np.std(env.trajectories, axis=0)
        upper = env.msd + 2.33*std_msd/np.sqrt(env.n)
        lower = env.msd - 2.33*std_msd/np.sqrt(env.n)
        color_std = par.lighten_color(color, 0.4)
        ax.fill_between(time, lower, upper, color=color_std, alpha=0.3, zorder=0)  

    at = AnchoredText(label, prop=dict(size=par.size_labels_figures), frameon=False, loc='upper left')
    ax.add_artist(at)
    
    ax.tick_params(axis='both', labelsize=par.size_ticks)
    if legend:
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

def plot_pdf(ax, env, mode, time, tl=0, tref=0, xy_label=True, legend=True):
    
    trajectories_points = env.trajectories[:, time]

    # Analytitcal

    label = None
    variable = '\phi' if mode=='phi' else mode
    
    if time == int(env.Tf/(4*env.h)):
        label = r'$\frac{1}{\sqrt{{2\pi(\sigma)^2}}}$'+rf'$e^{{-\frac{{({variable}-\langle {variable} \rangle)^2}}{{2\sigma^2}}}}$'

    x, P = env.propagator(time, tref = tref, tl = tl)
    ax.plot(x, P, lw=2, ls=":", color = 'black', zorder=2, label = label)

    # Histogram and Fit
    num_bins=40
    hist, bin_edges = np.histogram(trajectories_points, density=True, bins=num_bins)
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2    
    
    # Get the fitted curve
    coeff = data_analysis.gauss_fit(trajectories_points, num_bins)
    coeff = coeff[0]
    min = np.min(trajectories_points)
    max = np.max(trajectories_points)
    x_fit = np.linspace(min*1.2, max*1.2)
    hist_fit = data_analysis.gauss(x_fit, *coeff) 

    ax.bar(bin_centres, hist, width=bin_edges[1] - bin_edges[0], alpha=0.5, zorder=0)
    ax.plot(x_fit, hist_fit, lw=2, label=f'{(round(time*env.h, 2))}', zorder=1)

    ax.set_title(rf'$variable: \alpha = {env.alpha}, H = {env.H}, A_H = {round(env.A_H, 2)}$', fontsize=par.axis_fontsize)
    if xy_label:
        ax.set_xlabel(rf'${variable}$', fontsize=par.axis_fontsize)
        ax.set_ylabel(rf'$P({variable},t)$', fontsize=par.axis_fontsize)
    ax.tick_params(axis='both', labelsize=par.size_ticks)
    if legend:
        ax.legend(fontsize = par.legend_size)

def add_trend(ax, x0, xf, func, y0=1, text = "", xloc = 0, yloc = 0, fontsize = 15, **kwargs):
    t = np.arange(x0,xf,0.05)

    if kwargs:
        y = func(t, alpha = kwargs["alpha"])*y0
        ax.plot(t, y, color = "black", alpha = 1, ls = ":", lw=2)
        ax.text(xloc, yloc, text, fontsize=fontsize)
    else:
        y = func(t)*y0
        ax.plot(t, y, color = "black", alpha = 1, ls = ":", lw=2)
        ax.text(xloc, yloc, text, fontsize = fontsize)

def t(t):
    return t

def t2(t):
    return t**2

def t3(t):
    return t**3

def talpha(t, **kwargs):
    alpha = kwargs["alpha"]
    return t**alpha