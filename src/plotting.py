# -- FUNCTIONS --
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gamma
import plotting_param as par
import data_analysis
from world import Angular, rModulus
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

def phi_fBm_propagator_ansatz(phi, time, H, phi0=0):
    
    factor = np.sqrt( 1 / (2*np.pi*(time**(2*H))) )
    
    argument = - ((phi - phi0)**2) / (2*time**(2*H))
    
    return factor*np.exp(argument)

def phi_fBm_propagator_calvo(phi, time, H, phi0=0):
    
    
    return (np.sqrt(H/np.pi)) * (gamma(H+1/2)/(time**H)) * np.exp(-H*((gamma(H+1/2)*(phi-phi0)/(time**(H)))**2))

def phi_fBm_msd(time, H):
    # return (1/(2*H*(gamma(H+1/2)**2)))*(time**(2*H))
    return (time**(2*H))



# Plotting
def plot_msd(ax, env, variable, label_an = True):

    style = par.msd_style[variable].copy()
    if isinstance(env, Angular):
        ylabel = r'MSD$\langle (\phi(t)-\phi_0)^2 \rangle$'
    if isinstance(env, rModulus):
        ylabel = r'MSD$\langle (\boldsymbol{r}(t)-\boldsymbol{r}_0)^2 \rangle$'

    env.make_B_H()

    if variable == 'an':
        style['label'] = style['label'] if label_an else None
    else:
        if isinstance(env, Angular):
            style['label'] = rf"{style['label']} $\alpha_R=${env.alpha} $H_R=${env.H}"
        else:
            style['label'] = rf"{style['label']} $\alpha_T=${env.alpha} $H_T=${env.H}"+ "\n" + rf"$\alpha_R=${env.alphaR} $H_R=${env.HR}"

    if variable == 'sim':
        msd = env.msd
        time = env.t
        style['marker']='o'

    elif variable == 'sol':
        msd = env.msd_sol
        time = env.t
    elif variable == 'an':
        msd = env.msd_an
        time = env.t

    ax.plot(time, msd, **style)

    ax.set_xlabel('t', fontsize = par.axis_fontsize)
    ax.tick_params(axis='both', labelsize=par.size_ticks)
    ax.set_ylabel(f'{ylabel}', fontsize = par.axis_fontsize)
    ax.grid(':')
    ax.legend(fontsize = par.legend_size, bbox_to_anchor=(1, 1))

def plot_moment(ax, env, variable, mom_type, label_an = True, pic_in_grid = False):

    """
    Plots a moment vector (mean or variance).
    
    Parameters:
    ----------
    ax : 

    env: class

    variable : str
        Can be 'sim' or 'sol': The moment was computed using L1 discretization of eom or of the convolution with the memory kernel, respectively

    moment_type : str
        Can be 'mean' or 'var' defining the type of moment, it will change y label.

    """

    style = par.msd_style[variable].copy()
    env.make_B_H()

    if variable == 'an':
        style['label'] = style['label'] if label_an else None
    else:
        if pic_in_grid:
            style['label'] = rf"$H=${env.H}"
        else:
            style['label'] = rf"{style['label']} $\alpha=${env.alpha} $H=${env.H} $A_H$={round(env.A_H,2)}"

    if variable == 'sim':
        moment = env.mean if mom_type=='mean' else env.var#/env.var.max()
        time = env.t

    elif variable == 'sol':
        moment = env.mean_sol if mom_type=='mean' else env.var_sol
        time = env.t

    elif variable == 'an':
        moment = env.mean_an if mom_type=='mean' else env.var_an#/env.var_an.max()
        time = env.t
    
    elif variable == 'fit':
        fit_indices = np.arange(1, (env.n), 5) 
        time = np.array(fit_indices) * env.h

        mean_fit = []
        var_fit = []

        for i in fit_indices:
            samples = env.trajectories[:, i]
            coeff, _ = data_analysis.gauss_fit(samples, bins=40)
            A, mu, sigma = coeff

            mean_fit.append(mu)
            var_fit.append(sigma**2)

        moment = var_fit if mom_type == 'var' else mean_fit


    ax.plot(time, moment, **style)

    ylabel_map = {
        'var': r'$\sigma^2(t)$',
        'mean': r'$\langle \phi(t) \rangle$'
    }

    ax.tick_params(axis='both', labelsize=par.size_ticks)
    if pic_in_grid:
        ax.legend(fontsize = par.legend_size)
    else:
        ax.grid(':')    
        ax.set_xlabel('t', fontsize = par.axis_fontsize)
        ax.set_ylabel(ylabel_map[mom_type], fontsize = par.axis_fontsize)
        ax.legend(fontsize = par.legend_size,bbox_to_anchor=(1, 1))


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

