import sys
sys.path.append("src/")
from world import *
import plotting
import matplotlib.pyplot as plt


realizations = 1000
alphaR = 0.3
HR = 0.8
Tf = 10
h = 0.05

phi = Angular(realizations=realizations, alpha=alphaR, H=HR, Tf=Tf, h=h)
phi.run()
phi.compute_var()

fig, ax = plt.subplots(figsize=(12, 9))
color = plotting.plot_moment(ax, phi, variable='sim', mom_type='var')
phi.compute_var_an()
plotting.plot_moment(ax, phi, variable='an', mom_type='var', color=color)
phi.compute_var_an(log=True)
plotting.plot_moment(ax, phi, variable='an', mom_type='var', color=color, log=True)
fig.savefig('plots/tests/L2.png', dpi=100)

def a(l):
    assert l >= 0
    alpha=1
    return (l+1)**(1-alpha) - (l)**(1-alpha)

def b(l):
    assert l >= 0
    alpha=1
    # return (1/(2-alpha)) * ((l+1)**(2-alpha) - (l)**(2-alpha)) - 0.5 * ((l+1)**(1-alpha) + (l)**(1-alpha))
    return (1/(2-alpha)) * ((l+1)**(2-alpha) - (l)**(2-alpha))

print(a(0), a(0) + b(0))