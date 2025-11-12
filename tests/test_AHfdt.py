import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities
import plotting_param as par
from matplotlib.offsetbox import AnchoredText


mode = 'phi'
Tf = 20.
start_set=1
L_type = 'L1'
DATA_PATH = 'data_tests'
eta=1
tref = 12

fig, ax = plt.subplots()

##########################################################

alphaR = 0.2
HR = (2-alphaR)/2
h = 0.005
realizations = 1000
sets = 1
Tf = 20.
L_type = 'L1'


env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path = DATA_PATH)
time = np.linspace(0, Tf, env.n)
env.compute_var()
var_an = env.compute_var_an(time=time)

var_an_comp = (2/gamma(alphaR+1))*time**(alphaR)
# var_an_comp = var_an_comp*(2*HR)*gamma(2-alphaR)
print(env.var[1])
print(var_an_comp[1])
ax.plot(time, env.var)
# ax.plot(time, var_an, label='old result')
ax.plot(time, var_an_comp, label='analytics')
# ax.plot(time, time**2, ls=':', lw=1, c='black')
ax.legend()
# var_an_log = env.compute_var_an(time=time, log=True, tl=1)
# print(time[1:])
# ax.plot(time, var_an_log)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(h)
fig.savefig(f"plots/tests/alpha{alphaR}_h{h}_Tf{Tf}_AHfdt_scal.png", dpi=100)
# fig.savefig(f"plots/tests/alpha{alphaR}_h{h}_crazy.png", dpi=100)
