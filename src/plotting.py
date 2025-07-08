# -- PARAMETERS --

legend_size = 15
axis_fontsize = 19
size_ticks = 20
marker_size = 10

msd = {
    'phi': dict(c = 'dodgerblue', lw=2, label = 'sim')  
}

# -- FUNCTIONS --
import matplotlib.pyplot as plt
import numpy as np

def plot_msd(ax, msd, delta_t, variable):

    time = np.arange(0,len(msd))*delta_t

    ax.plot(time, msd, **msd[f'{variable}'], zorder=1)
    # ax.plot(time, time**, **msd[f'{variable}'], zorder=1)

    ax.set_xlabel('t', fontsize = axis_fontsize)
    ax.tick_params(axis='both', labelsize=size_ticks)
    ax.set_ylabel(r'MSD$\langle (\phi(t)-\phi_0)^2 \rangle$', fontsize = axis_fontsize)
    ax.grid(':')
    ax.legend(fontsize = legend_size)
