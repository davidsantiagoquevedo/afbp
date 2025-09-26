import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import utilities
from scipy.special import gamma

DATA_PATH = 'data_tests'
out_path = "tests"
mode = 'phi'
L_type = 'L1'
realizations = 500
Tf = 10
h = 0.005
start_set = 1
sets = 10

alphaR = 0.5
HR = 0.85
m=0.00000001
m=0.0000001
eta=1

def tl(alpha, H, eta=1, m=0.00000001):
    return ((m*H*gamma(2*H))/(eta*(alpha+H-1)*gamma(alpha)*gamma(alpha+2*H-1)))**(1/(4-2*alpha-2*H))


env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path=DATA_PATH)

env.compute_var()
env.make_B_H()


plt.plot(env.t, env.var, label = "numerics")
tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)

env.compute_var_an(tl=tl_value)
plt.plot(env.t, env.var_an, ls = "-", label = r"$t_l=$"+str(tl_value))
tl_value = 0
env.compute_var_an(tl=tl_value)
plt.plot(env.t, env.var_an, ls = "--", label = r"$t_l=$"+str(tl_value))
plt.legend(loc='best')
plt.title(f"H={HR}, alpha = {alphaR}, eta = {eta}, m={m}")
plt.savefig(f"plots/{out_path}/{L_type}_{mode}LT_var_alphaR{alphaR}_HR{HR}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)
plt.show()