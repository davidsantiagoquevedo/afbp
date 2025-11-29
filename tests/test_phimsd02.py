import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities
import plotting_param as par
from matplotlib.offsetbox import AnchoredText


mode = 'phi'
Tf = 10.
L_type = 'L1'
DATA_PATH = 'data_tests'
eta=1
realizations = 1000
start_set=1
sets = 1
Tf = 20.

alphaR = 0.2
HR = (2-alphaR)/2
alphaT = alphaR
HT = HR

fig, ax = plt.subplots()

##########################################################
# h = 0.005
# env = utilities.read_env(mode=mode,
#                         L_type = L_type, 
#                         alpha=alphaT, H=HT,
#                         alphaR=alphaR, HR=HR,
#                         ups=1,
#                         realizations=realizations,
#                         Tf=Tf,
#                         h=h,
#                         start_set=start_set,
#                         sets=sets,
#                         path = DATA_PATH)


# env.compute_msd()
# time = np.linspace(0, Tf, len(env.msd))
# ax.plot(time, env.msd, label=f'h={h}')

# h = 0.001
# env = utilities.read_env(mode=mode,
#                         L_type = L_type, 
#                         alpha=alphaT, H=HT,
#                         alphaR=alphaR, HR=HR,
#                         ups=1,
#                         realizations=realizations,
#                         Tf=Tf,
#                         h=h,
#                         start_set=start_set,
#                         sets=sets,
#                         path = DATA_PATH)


# env.compute_msd()
# time = np.linspace(0, Tf, len(env.msd))
# ax.plot(time, env.msd, label=f'h={h}')

h = 0.0001
env = utilities.read_env(mode=mode,
                        L_type = L_type, 
                        alpha=alphaR, H=HR,
                        realizations=realizations,
                        Tf=Tf,
                        h=h,
                        start_set=start_set,
                        sets=sets,
                        path = DATA_PATH)


env.compute_msd()
time = np.linspace(0, Tf, len(env.msd))
ax.plot(time, env.msd, label=f'h={h}')


# h = 0.0001
# env = utilities.read_env(mode=mode,
#                         L_type = L_type, 
#                         alpha=alphaT, H=HT,
#                         alphaR=alphaR, HR=HR,
#                         ups=1,
#                         realizations=realizations,
#                         Tf=Tf,
#                         h=h,
#                         start_set=start_set,
#                         sets=sets,
#                         path = DATA_PATH)


# env.compute_msd()
# time = np.linspace(0, Tf, len(env.msd))
# ax.plot(time, env.msd, label=f'h={h}')

env.compute_msd_an()
time = np.linspace(0, Tf, len(env.msd_an))
ax.plot(time, env.msd_an, label='formula')

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(xmin = h)

ax.legend()
fig.savefig(f"plots/tests/alpha{alphaR}_Tf{Tf}_compareh.png", dpi=100)
