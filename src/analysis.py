
from world import *
import matplotlib.pyplot as plt
import plotting

def phi_correlation(env):

    """
    Computes < [phi(t) - phi0]^2 > averaged over all agents.
    Returns:
        corr: array of shape (n,)
    """
    corr = []

    for time in range(env.n):

        corr_value = 0
        for agent in env.agents:

            agent.update_phi(time)
            corr_value += (agent.phi_vec[time]-agent.phi0)**2

        corr.append(corr_value/env.numb_agents)

    return corr

env = Env(numb_agents=1, alpha = 0.1, Tf = 0.03, h=1e-3)

correlation = phi_correlation(env)

fig, ax = plt.subplots()
plotting.plot_msd(ax, correlation, env.h, 'phi')
fig.tight_layout()
plt.savefig(f"phi_corr.pdf")


