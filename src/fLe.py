import sys
sys.path.append("src/")
import numpy as np
from scipy.special import gamma
import pandas as pd
import mittag_leffler as ml
from fbm import FBM
import fBm_stats as fbs


class fle():
    def __init__(self, alpha):
        self.alpha = alpha
        self.H = (2-alpha)/2
    
    def params(self, h, Tf, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1):
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
        
        self.h = h
        self.Tf = Tf
        self.t = np.linspace(T0,Tf,1000)
        self.n = int(self.Tf/self.h)
        self.x_n = np.zeros(self.n)

        H = self.H
        if self.alpha == 1:
            self.A_H = 1
        else:
            self.A_H = 1/np.sqrt(H*(2*H-1)*gamma(2*H-1))
           
            
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

    def make_B_H(self, method = 'daviesharte'):
        n = self.n
        H = self.H
        Tf = self.Tf
        A_H = self.A_H
        np.random.seed()
          
        f = FBM(n = n, hurst = H, length = Tf, method = method)
        self.B_H = f.fbm()
        self.dB_H = n/Tf*np.diff(self.B_H)
        self.t_BH = f.times()
        self.t = self.t_BH[:self.n]
        self.B = A_H*self.B_H
        self.dB =A_H*self.dB_H

    # Numerical solution
    def a_i(self, i):
        H = self.H
        n = self.n
        return (n-i)**(2*H-1) - (n-i-1)**(2*H-1)
    
    def x_k(self, k):
        alpha = self.alpha
        H = self.H
        B = self.B
        
        h = self.h
        x_n = self.x_n
         
        a_ii = 0
        if k-2 >= 0:    
            for i in range(0, k-1):
                a_ii += self.a_i(i)*(x_n[i+1]+x_n[i])
        gamma2h = 2*gamma(2-alpha)*(h**(alpha-1))
        return -x_n[k-1] +  gamma2h*B[k] - a_ii

    def solve(self):
        n = self.n
        x_n = self.x_n
        
        for k in range(1,n):
            x_n[k] = self.x_k(k)
        
        self.numerical = x_n

from tqdm import tqdm
def get_msd(eq,realizations):
    for r in tqdm(range(realizations)):
        eq.make_B_H()
        eq.solve()   
        if r == 0:
            df_msd = pd.DataFrame({"t": eq.t})
        df_msd["x_"+str(r)] = eq.numerical        
    df_msd.set_index("t", inplace = True)

    msd = fbs.msd(df_msd, False)
    return msd

realizations = 100


# alpha = 1
# eq1 = fle(alpha)
# eq1.params(h=0.01, Tf=10, T0 = 0)
# msd1 = get_msd(eq1,realizations)

alpha = 0.5
eq05 = fle(alpha)
eq05.params(h=0.001, Tf=1, T0 = 0)
msd05 = get_msd(eq05,realizations)


alpha = 0.3
eq03 = fle(alpha)
eq03.params(h=0.001, Tf=1, T0 = 0)
msd03 = get_msd(eq03,realizations)


import matplotlib.pyplot as plt
plt.plot(eq03.t,msd03, label = "0.3")
plt.plot(eq05.t,msd05, label = "0.5")
# plt.plot(eq1.t,msd1, label = "1")
#plt.plot(eq.t, msd_teo)
plt.legend()
plt.show()
