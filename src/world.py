import numpy as np
from scipy.special import gamma, gammainc
import pandas as pd
from fbm import FBM
import os
import pickle
from tqdm import tqdm
from integration import *

# ---------- Base Class ---------- #
class Base:

    def __init__(self, realizations, alpha, H, Tf, h):
        # Common parameters
        self.realizations = realizations
        self.alpha = alpha
        self.H = H
        self.Tf = Tf
        self.h = h
        self.n = int(Tf / h)

        # Preallocate storage (to be specialized in subclasses)
        self.trajectories = []
        self.trajectory_sol = []

        # Noise Amplitude
        self.A_H = 1
        # self.A_H = 1/(np.sqrt(2*H)*gamma(H+1/2))

    # Generalized diffusion coefficient 
    def calc_general_diff_coeff(self):
        nominator = self.H*gamma(2*self.H)
        denominator = gamma(self.alpha)*gamma(self.alpha+2*self.H-1)
        self.D_H = (self.A_H**2)*nominator/denominator

    # --------- Noise Generator --------- #
    def make_B_H(self, method='daviesharte'):
        np.random.seed()
        f = FBM(n=self.n, hurst=self.H, length=self.Tf, method=method)

        self.B_H = f.fbm()
        self.dB_H = np.diff(self.B_H) * (self.n / self.Tf)

        self.B = self.A_H*self.B_H
        self.dB = self.A_H*self.dB_H

        self.t_BH = f.times()
        self.t = self.t_BH[:self.n]

        return 

    # --------- Utilities --------- #
    def cnj(self, k):
        return (k+1)**(1-self.alpha) - k**(1-self.alpha)

    def run(self):
        """Run all realizations"""
        self.trajectories = []
        for r in tqdm(range(self.realizations)):
            self.make_B_H()
            if isinstance(self, Angular):
                traj = self.run_one()
            else:
                traj = self.run_one(r)
            self.trajectories.append(traj)
        self.trajectories = np.array(self.trajectories)

    def run_solution(self):
        
        for _ in tqdm(range(self.realizations)):
            self.make_B_H()
            traj = self.run_one_solution()
            self.trajectory_sol.append(traj)
        self.trajectory_sol = np.array(self.trajectory_sol)
           
    # --------- Stats --------- #
    def compute_msd(self):
        self.msd = np.mean((self.trajectories - self.trajectories[:, [0]])**2, axis=0)

    def compute_msd_sol(self):
        self.msd_sol = np.mean((self.trajectory_sol - self.trajectory_sol[:, [0]])**2, axis=0)

    def compute_mean(self):
        self.mean = np.mean(self.trajectories, axis=0)

    def compute_var(self):
        self.var = np.var(self.trajectories, axis=0)
        
    def compute_var_sol(self):
        self.var_sol = np.var(self.trajectory_sol, axis=0)

    # --------- Save/Load --------- #
    def save(self, set_label, folder="data", mode="phi"):
        
        if isinstance(self, Angular):
            alphaH = f"alphaR{self.alpha}_HR{self.H}"
        elif isinstance(self, xDirection) or isinstance(self, yDirection):
            alphaH = f"alphaT{self.alpha}_HT{self.H}_alphaR{self.alphaR}_HR{self.HR}_nu{self.nu}_AHT{self.A_H}"
            delattr(self, "phi_trajectories") #removed to avoid duplicating information
        else:
            alphaH = f"alphaT{self.alpha}_HT{self.H}_alphaR{self.alphaR}_HR{self.HR}_nu{self.nu}_AHT{self.A_H}"
            delattr(self, "x_trajectories") #removed to avoid duplicating information
            delattr(self, "y_trajectories") #removed to avoid duplicating information
        os.makedirs(folder, exist_ok=True)
        filename = (f"{mode}_"
                    f"{alphaH}_"
                    f"r{self.realizations}_"
                    f"Tf{self.Tf}_"
                    f"h{self.h}_" 
                    f"set{set_label}.pkl")
        filepath = os.path.join(folder, filename)
        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filepath):
        with open(filepath, "rb") as f:
            env = pickle.load(f)
        return env

# ---------- Angular (phi) ---------- #
class Angular(Base):
        
    """
    This class extends the general `Base` class to solve angular euation·

    Parameters
    ----------

    """
    
    def __init__(self, phi0 = 0, **kwargs):
        
        super().__init__(**kwargs)
        self.phi0 = phi0
        self.calc_general_diff_coeff()
    
    def compute_var_an(self, log=False, time = 0):
        H = self.H
        alpha = self.alpha
        self.calc_general_diff_coeff()
        if log:
            self.var_an = 2*self.D_H*(np.log(self.t/self.h))
            return self.D_H*(np.log(time))
        else:
            self.D_H = self.D_H/(alpha+H-1)
            self.var_an = self.D_H*(self.t**(2*alpha+2*H-2))
            return self.D_H*(time**(2*alpha+2*H-2))

    def compute_msd_an(self):
        if not hasattr(self, "var_an"): #compute variance if not already done
            self.compute_var_an()
        self.msd_an = self.var_an + (self.phi0**2)

    def propagator(self, time_index):
        """

        Given a time, it returns the analytical probability function over the interval spanned by the trajectory.

        Returns:

        x : np.array 
        Intreval of evaluation of probability function [min(trajectory), max(trajectory)]
        
        P(x,t) : np.array
        Analytical probability function

        """

        screenshot = self.trajectories[:, time_index]   # time screenshot of many realizations at time_index
        limit = np.min(np.abs(np.array(np.min(screenshot), np.max(screenshot))))
        limit += limit*0.3 
        x = np.arange(-limit, limit, 1e-3)

        variance = self.compute_var_an(time_index*self.h)
        factor = np.sqrt( 1 / (2*np.pi*variance) )
        argument = (-(x)**2) / (2*variance)

        P = factor*np.exp(argument)

        return x, P
    
    def run_one(self):
        # Loop over timesteps
        traj = np.zeros(self.n)
        for time in range(1, self.n):
            
            # Sum term
            sum_term = 0
            for i in range(1, time):
                
                sum_term += self.cnj(time-i) * (traj[i]-traj[i-1])

            # Update rule
            coeff_noise = ((self.h)**(self.alpha)) * (gamma(2-self.alpha))
            traj[time] = traj[time-1] + coeff_noise*self.dB[time] - sum_term
        
        return traj
    
    def a(self, l):
        assert l >= 0
        alpha=self.alpha
        return (l+1)**(1-alpha) - (l)**(1-alpha)
    
    def b(self, l):
        assert l >= 0
        alpha=self.alpha
        return (1/(2-alpha)) * ((l+1)**(2-alpha) - (l)**(2-alpha)) - 0.5 * ((l+1)**(1-alpha) - (l)**(1-alpha))
    
    def c(self, j, s):
        a = self.a
        b = self.b
        
        k = j - s
        
        if j <= 1:
            assert k < 2
            if k==0:
                c = a(0) + b(0) + b(1)
            elif k==1:
                c = a(1) - b(1) - b(0)
                
        if j == 2:
            assert k < 3
            if k==0:
                c = a(0) + b(0)
            elif k==1:
                c = a(1) + b(1) + b(2) - b(0)
            elif k==2:
                c = a(2) - b(2) - b(1)
                
        if j >= 3:
            assert k < (j+1)
            if k==0:
                c = a(0) + b(0)
            elif k>=1 and k<=(j-2):
                c = a(k) + b(k) - b(k-1)
            elif k==(j-1):
                c = a(j-1) + b(j-1) + b(j) - b(j-2)
            elif k==j:
                c = a(j) - b(j) - b(j-1)
                
        return c
        
    # def run_one(self):
    #     c = self.c
    #     # Loop over timesteps
    #     traj = np.zeros(self.n)
        
    #     for j in range(0, self.n-1):
    #         c_0 = c(j,j)    
    #         if j == 0:
    #             sum_term = 0                
    #         else:
    #             # Sum term
    #             sum_term = 0
    #             for s in range(0, j-1):
                    
    #                 sum_term += c(j,s) * (traj[s+1]-traj[s])

    #         # Update rule
    #         coeff_noise = ((self.h)**(self.alpha)) * (gamma(2-self.alpha))/c_0
            
    #         traj[j+1] = traj[j] + coeff_noise*self.dB[j+1] - sum_term/c_0
        
    #     return traj

    def run_one_solution(self):
        return convolution_weights(self.dB, self.t, self.alpha)

class xDirection(Base):
        
    """
    This class extends the general `Base` class to solve x equation·

    Parameters
    ----------

    """
    def __init__(self, phi, x0=0, nu=1, AHT=1, **kwargs):
        
        super().__init__(**kwargs) #since init defined, it doesn't inherit init from parent
        
        # initial condition
        self.x0 = x0
        # self_propulsion modulus
        self.nu = nu
        self.A_H = AHT
        self.calc_general_diff_coeff()  #calculating D_H translational
        
        self.phi_trajectories = phi.trajectories
        self.alphaR = phi.alpha
        self.HR = phi.H
        self.DHR = phi.D_H
        if self.realizations != phi.realizations:
            self.realizations = phi.realizations
            
    def run_one(self, realization_index):
        """
        Compute one trajectory of x for a single realization.
        """
        traj = np.zeros(self.n)
        
        for time in range(1, self.n):

            sum_x = 0
            for i in range(1, time): 
                sum_x += self.cnj(time - i) * (traj[i] - traj[i-1])
            
            sum_phi = 0
            for i in range(1, time):
                sum_phi += self.cnj(time - i) * (np.cos(self.phi_trajectories[realization_index, i-1])) * self.h
            
            coeff_noise = (self.h**self.alpha) * gamma(2 - self.alpha)
            traj[time] = traj[time-1] + coeff_noise * self.dB[time] - sum_x + self.nu*sum_phi + (np.cos(self.phi_trajectories[realization_index, time-1]))*self.h

        return traj

class yDirection(Base):
        
    """
    This class extends the general `Base` class to solve y equation·

    Parameters
    ----------

    """
    def __init__(self, phi=None, y0=0, nu=1, AHT=1, **kwargs):
        
        super().__init__(**kwargs) #since init defined, it doesn't inherit init from parent
           
        # initial condition
        self.y0 = y0
        # self_propulsion modulus
        self.nu = nu
        self.A_H = AHT
        self.calc_general_diff_coeff()  #calculating D_H translational

        
        if phi is not None:
            # We must overwrite some features
            self.phi_trajectories = phi.trajectories
            self.alphaR = phi.alpha
            self.HR = phi.H
            self.DHR = phi.D_H
            if self.realizations != phi.realizations:
                self.realizations = phi.realizations

    def run_one(self, realization_index):
        """
        Compute one trajectory of y for a single realization.
        """                                                              
        traj = np.zeros(self.n)
        
        for time in range(1, self.n):

            sum_y = 0
            for i in range(1, time): 
                sum_y += self.cnj(time - i) * (traj[i] - traj[i-1])
            
            sum_phi = 0
            for i in range(1, time):
              sum_phi += self.cnj(time - i) * (np.sin(self.phi_trajectories[realization_index, i-1])) * self.h
            
            coeff_noise = (self.h**self.alpha) * gamma(2 - self.alpha)
            traj[time] = traj[time-1] + coeff_noise * self.dB[time] - sum_y + self.nu*sum_phi + (np.sin(self.phi_trajectories[realization_index, time-1]))*self.h

        return traj

class rModulus(Base):
        
    """
    This class extends the general `Base` class to solve r equation·

    Parameters
    ----------

    """
    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs) #since init defined, it doesn't inherit init from parent
        self.x_trajectories = x.trajectories
        self.y_trajectories = y.trajectories
        
        # translational properties
        self.nu = x.nu
        self.A_H = x.A_H
        self.D_H = x.D_H

        # rotational properties
        self.alphaR = x.alphaR
        self.HR = x.HR
        self.DHR = x.DHR

        # self.r_trajectories = np.zeros(len(self.x_trajectories))
    
    def compute_r_modulus(self):
        
        self.trajectories = np.sqrt(self.x_trajectories**2+self.y_trajectories**2)
        
    def compute_msd_an(self):
        DHT = self.D_H
        DHR = self.DHR
        nu = self.nu
        t = self.t 
        alphaT = self.alpha
        HT = self.H # to add in complete expression without fluc-diss
        alphaR = self.alphaR
        HR = self.HR
        
        aux_var = alphaR + HR - 1

        coeff = ( nu**2 / (aux_var*((DHR/2)**(1/aux_var))) )
        gamma1 = gamma(1/(2*aux_var))*gammainc(1/(2*aux_var), (DHR*t**(2*aux_var))/2)
        gamma2 = gamma(1/(aux_var))*gammainc(1/  (aux_var), (DHR*t**(2*aux_var))/2)
    
        # self.msd_an =  coeff*( gamma1*((DHR/2)**(1/(2*aux_var)))*t - gamma2  ) + 2*DHT*t**alphaT
        self.msd_an =  coeff*( gamma1*((DHR/2)**(1/(2*aux_var)))*t - gamma2  ) 
        # self.msd_an = 2*DHT*t**alphaT
