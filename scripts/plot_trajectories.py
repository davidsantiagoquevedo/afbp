import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par
import utilities

mode = 'r'
Tf = 10
h=0.01
realizations = 1000
start_set=1
sets=1
L_type = 'L1'
AHT=1.
alphaT = 1.
HT = 0.5
alphaR = alphaT
HR = HT
nu=1

x = utilities.read_env(mode='x',
                        L_type = L_type, 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        nu=nu,
                        AHT=AHT,
                        realizations=realizations,
                        Tf=Tf,
                        h=h,
                        start_set=start_set,
                        sets=sets)
y = utilities.read_env(mode='y',
                        L_type = L_type, 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        nu=nu,
                        AHT=AHT,
                        realizations=realizations,
                        Tf=Tf,
                        h=h,
                        start_set=start_set,
                        sets=sets)


fig, ax = plt.subplots()
j = 1
x = x.trajectories[j,:]
y = y.trajectories[j,:]

plot.plot_trajectory(ax,x,y)

fig.tight_layout()
fig.savefig(f"plots/trajectories/traj_alphaT{alphaT}_HT{HT}_r{j}_Tf{Tf}_h{h}_nu{nu}.png", dpi=100)

