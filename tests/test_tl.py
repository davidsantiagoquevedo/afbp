import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import utilities
from scipy.special import gamma

DATA_PATH = 'data'
out_path = "tests"
mode = 'phi'
L_type = 'L1'
realizations = 160
Tf = 10
h = 0.0005
start_set = 1
sets = 10

alphaR = 0.7
HR = 0.35
m=1e-9
eta=1

def tl(alpha, H, eta=1, m=0.00000001):
    return ((m*H*gamma(2*H))/(eta*(alpha+H-1)*gamma(alpha)*gamma(alpha+2*H-1)))**(1/(4-2*alpha-2*H))


env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path=DATA_PATH)

env.compute_var()
env.make_B_H()

fig, ax = plt.subplots()
ax.plot(env.t, env.var, label = "numerics")
tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)

env.compute_var_an(tl=tl_value)
ax.plot(env.t, env.var_an, ls = "-", label = r"$t_l=$"+str(tl_value))
env.compute_var_an(log=True,tl=tl_value)
ax.plot(env.t[1:], env.var_an, ls = ":", label = r"$log + t_l=$"+str(tl_value))
tl_value = 0
env.compute_var_an(tl=tl_value)
ax.plot(env.t, env.var_an, ls = "--", label = r"$t_l=$"+str(tl_value))
ax.legend(loc='best')
ax.set_title(f"H={HR}, alpha = {alphaR}, eta = {eta}, m={m}")
fig.savefig(f"plots/{out_path}/{L_type}_{mode}LT_var_alphaR{alphaR}_HR{HR}_r{realizations*sets}_Tf{Tf}_h{h}_m{m}.png", dpi=100)