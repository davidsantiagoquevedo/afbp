
from matplotlib.offsetbox import AnchoredText
import matplotlib as mpl
import numpy as np
import plotting_param as par
from world import Angular
import math
from scipy.special import gamma
import statsmodels.api as sm


def add_caption_letter(ax, cap, xloc=.07, yloc=.98):
    ax.text(xloc, yloc, cap, ha='left', va='top', transform=ax.transAxes)

def get_sampling_indices(upper_limit, samplesize, type, loglin_rat):
    n = upper_limit
    # linear spacing
    sampling_step = n / (samplesize - 1)
    indices_lin = (np.arange(samplesize) * sampling_step).astype(int)
    indices_lin = np.clip(indices_lin, 0, n - 1)
    
    # logarithmic spacing
    O = math.log10(n - 1)
    indices_log = np.logspace(0, O, samplesize)
    indices_log = np.round(indices_log).astype(int)
    indices_log = np.unique(indices_log)
    indices_log = indices_log[indices_log < n]
    if indices_log[0] != 0: #zero index
        indices_log = np.insert(indices_log, 0, 0)
    if indices_log[-1] != n - 1: #last index
        indices_log = np.append(indices_log, n - 1)
    
    if type is None:
        return indices_lin

    elif type == 'log':
        return indices_log
    
    if type == 'loglin':
        cut = int(n*loglin_rat)
        first = indices_log[indices_log < cut]
        step = int(first[-1]-first[-2])
        second = np.arange(cut, n, step)
        indices_loglin = np.append(first ,second)
        if indices_log[-1] != n - 1: #last index
            indices_loglin = np.append(indices_loglin, n - 1)
        return indices_loglin


def plot_trajectory(ax, x, y, mod, k, fig=False):
    # mod slice trajectory points
    # k interpolation points

    x=x[::mod]
    y=y[::mod]

    n=len(x)
    x = np.interp(np.arange(n * k), np.arange(n) * k, x)
    y = np.interp(np.arange(n * k), np.arange(n) * k, y)
    t = np.linspace(0, 100, len(x))

    sc = ax.scatter(x, y, s=3, c=t,  cmap=par.cmap_black)
    if fig:
        with mpl.rc_context(fname="src/plotting_style_colorbar.mplstyle"):  
            fig.colorbar(sc, ax=ax, label=r'$t/\tau_{R}$')

def plot_moment(ax, env, mom_type, variable, legend = False, legend_id = 'H', color=None, ci = False, ci_bars = False, sample = False, max_value = 1, sampling_type = None, sample_size = None, loglin_rat = 0.3, rescale = 1, total_msd = True):

    """
    Plots a moment vector (msd or variance).
    
    Parameters:
    ----------
    ax : 

    env: class

    variable : str
        Can be 'sim' or 'sol': The moment was computed using L1 discretization of eom or of the convolution with the memory kernel, respectively

    moment_type : str
        Can be 'msd' or 'orcorr' defining the type of moment, it will change y label.

    """

    style = par.msd_style[variable].copy()
    time = np.arange(0, env.n)*env.h

    # specify color  
    if color is not None:
        style['c'] = color

    # set legend id if legend
    if legend:
        if legend_id == 'alpha':
            style['label'] = rf"$\alpha=${env.alpha}"
        elif legend_id == 'alphaQ':
            style['label'] = rf"$\alpha_Q=${env.alpha}"
        elif legend_id == 'alphaR':
            if isinstance(env, Angular):
                style['label'] = rf"$\alpha_R=${env.alpha}"
            else:
                style['label'] = rf"$\alpha_R=${env.alphaR}"
        elif legend_id == 'alphaT':
            style['label'] = rf"$\alpha_T=${env.alpha}"
        else:
            style['label'] = legend_id
    else:
        style['label'] = None

    if variable == 'sim':
        if mom_type=='msd':
            env.compute_msd()
            moment = env.msd
            upper = env.msd_upper_ci
            lower = env.msd_lower_ci
        elif mom_type=='orcorr':
            env.compute_orientation_corr()
            moment = env.orientation_corr
            upper = env.orientation_corr_upper_ci
            lower = env.orientation_corr_lower_ci
        
        if sample:
            n = int(moment.shape[0]*max_value)
            idx = get_sampling_indices(upper_limit = n, samplesize = sample_size, type = sampling_type, loglin_rat = loglin_rat)
            style.update({'ls':'', 'marker':'^', 'markersize':8})
        else:
            n = int(time.shape[0]*max_value)
            idx = get_sampling_indices(upper_limit = n, samplesize = n + 1, type = None, loglin_rat = None)

        moment = moment[idx]
        time_s = time[idx]
        
    elif variable == 'an' or variable == 'an_a' or variable == 'an_tot' or variable == 'an_tot_oversim':
        if mom_type=='msd':
            if isinstance(env, Angular):
                env.compute_msd_an()
            else:
                env.compute_msd_an(total=total_msd)
            moment = env.msd_an
        if mom_type=='orcorr':
            env.compute_orientation_corr_an()
            moment = env.orientation_corr_an
        time_s = time
        n = int(time_s.shape[0]*max_value)
        idx = get_sampling_indices(upper_limit = n, samplesize = n + 1, type = None, loglin_rat = None)
        moment = moment[idx]
        time_s = time_s[idx]

    if ci:
        n = int(time.shape[0]*max_value)
        time = time[idx]
        upper = upper[idx]
        lower = lower[idx]
        if color is not None:
            if ci_bars:
                ax.errorbar(time, moment/rescale, yerr=[moment/rescale-lower/rescale, upper/rescale-moment/rescale], fmt='none', capsize = 4, capthick=2, ecolor=color, alpha=0.5, zorder=2)
            else:
                idx = get_sampling_indices(upper_limit = n, samplesize = n + 1, type = None, loglin_rat = None)
                ax.fill_between(time, lower/rescale, upper/rescale, alpha=0.5, zorder=0, color=color)
        else:
            if ci_bars:
                ax.errorbar(time, moment/rescale, yerr=[moment/rescale-lower/rescale, upper/rescale-moment/rescale], fmt='none', alpha=0.5, zorder=1)
            else:
                idx = get_sampling_indices(upper_limit = n, samplesize = n + 1, type = None, loglin_rat = None)
                ax.fill_between(time, lower/rescale, upper/rescale, alpha=0.5, zorder=0)
    
    line, = ax.plot(time_s, moment/rescale, alpha = 1, **style)
    color = line.get_color()
    
    if legend:
        ax.legend()

    return color

def plot_pdf(ax, env, mode, time, tl=0, tref=0, xy_label=True, legend=True, legend_an=False, color=None, alpha_color=0.5):
    
           
    trajectories_points = env.trajectories[:, time]

    # Analytitcal

    label = None
    lg = None
    variable = '\Delta\phi' if mode=='phi' else mode
    
    #if time == int(env.Tf/(4*env.h)):
    if legend:
        lg = rf"$t/\tau_R = {str(time*env.h)}$"
    if legend_an:
        label = "Theoretical Gaussian"
    
    # Gaussian propagator
    x, P = env.propagator(time, tref = tref, tl = tl)
    ax.plot(x, P, lw=2, ls="-", alpha=alpha_color, color = par.color_analytic, zorder=2, label = label)

    # Histogram
    num_bins=20
    hist, bin_edges = np.histogram(trajectories_points, density=True, bins=num_bins)
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2    
        
    ax.bar(bin_centres, hist, width=bin_edges[1] - bin_edges[0], alpha=alpha_color, zorder=0, color = color, label = lg)
    # edge color
    ax.set_title(rf'$variable: \alpha = {env.alpha}, H = {env.H}, A_H = {round(env.A_H, 2)}$')
    if xy_label:
        ax.set_xlabel(rf'${variable}$')
        ax.set_ylabel(rf'$P({variable},t)$')
    ax.tick_params(axis='both')
    

def add_trend(ax, x0, xf, func, y0=1, h=0.05, text = "", xloc = 0, yloc = 0, fontsize = 15, **kwargs):
    t = np.arange(x0,xf,h)

    if kwargs:
        y = func(t, alpha = kwargs["alpha"])*y0
        ax.plot(t, y, color = 'black', alpha = 1, ls = "-", lw=2, zorder=4)
        ax.text(xloc, yloc, text, fontsize=fontsize, color = 'black')
    else:
        y = func(t)*y0
        ax.plot(t, y, color = 'black', alpha = 1, ls = "-", lw=2, zorder=4)
        ax.text(xloc, yloc, text, fontsize = fontsize, color = 'black')

def qq_plot(data, ax, time, color, alpha_color):
    data = data[:, time]
    z = (data - np.mean(data))/np.std(data)
    sm.qqplot(z,ax=ax, line='45',
              markerfacecolor=color,   # data points color
              markeredgecolor=color,
              alpha = alpha_color)
    lines = ax.get_lines()
    if len(lines) > 1:
        lines[-1].set_color(par.color_analytic)
        lines[-1].set_linewidth(2)
    ax.set_xlabel("")
    ax.set_ylabel("")

def add_pers_time(ax, pers_time, ymax, color):
    ax.axvline(x = pers_time, ymax = ymax, c=color, lw = 4.4, ls=':')
 
def add_cross_time(ax, cross_time, color, ymax=1):
    ax.axvline(x = cross_time, c=color, ymax=ymax,  lw = 2.5, ls='-')
 
def t(t):
    return t

def t2(t):
    return t**2

def t3(t):
    return t**3

def talpha(t, **kwargs):
    alpha = kwargs["alpha"]
    return t**alpha