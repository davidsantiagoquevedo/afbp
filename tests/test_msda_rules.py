import sys
sys.path.append("src/")
import utilities
import plotting 
import matplotlib.pyplot as plt

DATA_PATH = 'data_tests'
mode = 'r'
L_type = 'L1'
ups=1
AHT=0.
realizations = 1000
Tf = 10
h = 0.01
start_set = 1
sets = 1


alphaT = 1.
HT = 0.5  
alphaR = 0.8#, 0.8, 0.3]
HR = 0.6#, 0.6, 0.85]

# Plotting
fig, ax = plt.subplots(figsize=(12, 9))
rule=1
env = utilities.read_env(mode=mode,
                        L_type = L_type, 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        ups=ups,
                        AHT=AHT,
                        realizations=realizations,
                        Tf=Tf,
                        h=h,
                        start_set=start_set,
                        sets=sets,
                        path = DATA_PATH,
                        rule=rule)

# Plot MSD
env.make_B_H()
time = env.t
env.compute_msd()
ax.plot(time, env.msd, label='mean cos h=0.01')

rule = 2
env = utilities.read_env(mode=mode,
                        L_type = L_type, 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        ups=ups,
                        AHT=AHT,
                        realizations=realizations,
                        Tf=Tf,
                        h=h,
                        start_set=start_set,
                        sets=sets,
                        path = DATA_PATH,
                        rule = rule)
env.compute_msd()
ax.plot(time, env.msd, label='cos h=0.01')

rule = 3
env = utilities.read_env(mode=mode,
                        L_type = L_type, 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        ups=ups,
                        AHT=AHT,
                        realizations=realizations,
                        Tf=Tf,
                        h=h,
                        start_set=start_set,
                        sets=sets,
                        path = DATA_PATH,
                        rule = rule)
env.compute_msd()
ax.plot(time, env.msd, label='denser hR=0.005')

env.compute_msd_an(total=False)
ax.plot(time, env.msd_an, ls='--', label='an')
ax.legend()
fig.tight_layout()
fig.savefig(f"plots/tests/testcos_{L_type}_{mode}var_alphaT{alphaT}_HT{HT}_alphaR{alphaR}_HR{HR}_AHT{AHT}_r{realizations*sets}_h{h}.png", dpi=100)


