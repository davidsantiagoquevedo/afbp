from fbm import FBM
import numpy as np
from scipy.special import gamma
import pandas as pd
import mittag_leffler as ml

class fle():
    def __init__(self, alpha):
        self.alpha = alpha
        self.H = (2-alpha)/2
    
    def params(self, Tf, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1):
        """
        Function to set the parameters of the system to solve
        
        Args:
        """
        self.kB = 1
        self.eta = eta
        self.T = T
        self.M = M
        
        self.v0 = v0
        self.v02 = self.kB*T
        
        self.Tf = Tf
        self.t = np.linspace(T0,Tf,1000)
        
               
            
            
    def relaxation_overdamped(self):
        alpha = self.alpha
        t = self.t
        self.G_o = t**alpha
    
    def relaxation_underdamped(self):
        alpha = self.alpha
        eta = self.eta
        M = self.M
        
        t = self.t
        
        def G(t):
            z = (-eta / M) * t**(2 - alpha)
            return t * ml.mittag_leffler(z, 2 - alpha, 2)
        
        self.G_u = G(t)
               
    def msd_underdamped(self):
        alpha = self.alpha
        
        eta = self.eta
        M = self.M
        T = self.T
        
        v02 = self.v02
        kBT = self.kB*T
        
        t = self.t
        
        self.relaxation_underdamped()
        G2 = self.G_u*self.G_u
        z = -(eta/M)*t**(2-alpha)
        self.msd_u = v02*G2 + 2*kBT/M*((t**2) * ml.mittag_leffler(z, 2-alpha, 3) - 1/2*G2)
        
    def msd_overdamped(self):
        alpha = self.alpha
        
        eta = self.eta
        M = self.M
        T = self.T
        
        kBT = self.kB*T
        
        t = self.t
        
        self.relaxation_overdamped()
        self.msd_o = 2*kBT*(t**alpha)/(eta*gamma(alpha+1))

import matplotlib.pyplot as plt

bby1 = fle(alpha = 0.05)
bby1.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby1.msd_underdamped()
bby1.msd_overdamped()

bby2 = fle(alpha = 0.1)
bby2.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby2.msd_underdamped()
bby2.msd_overdamped()

bby3 = fle(alpha = 0.3)
bby3.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby3.msd_underdamped()
bby3.msd_overdamped()

bby4 = fle(alpha = 0.5)
bby4.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby4.msd_underdamped()
bby4.msd_overdamped()

bby5 = fle(alpha = 0.7)
bby5.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby5.msd_underdamped()
bby5.msd_overdamped()

bby6 = fle(alpha = 0.9)
bby6.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby6.msd_underdamped()
bby6.msd_overdamped()

bby7 = fle(alpha = 1)
bby7.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby7.msd_underdamped()
bby7.msd_overdamped()

fig, ax = plt.subplots()

ax.plot(bby1.t, bby1.msd_o, label=r"$\alpha$=0.05")
ax.plot(bby2.t, bby2.msd_o, label=r"$\alpha$=0.1")
ax.plot(bby3.t, bby3.msd_o, label=r"$\alpha$=0.3")
ax.plot(bby4.t, bby4.msd_o, label=r"$\alpha$=0.5")
ax.plot(bby5.t, bby5.msd_o, label=r"$\alpha$=0.7")
ax.plot(bby6.t, bby6.msd_o, label=r"$\alpha$=0.9")
ax.plot(bby7.t, bby7.msd_o, label=r"$\alpha$=1")
fig.show()

fig, ax = plt.subplots()

ax.plot(bby1.t, bby1.msd_o, label=r"$\alpha$=0.05")
ax.plot(bby1.t, bby1.msd_u, color = "red")
ax.plot(bby2.t, bby2.msd_o, label=r"$\alpha$=0.1")
ax.plot(bby2.t, bby2.msd_u, color = "red")
ax.plot(bby3.t, bby3.msd_o, label=r"$\alpha$=0.3")
ax.plot(bby3.t, bby3.msd_u, color = "red")
ax.plot(bby4.t, bby4.msd_o, label=r"$\alpha$=0.5")
ax.plot(bby4.t, bby4.msd_u, color = "red")
fig.show()