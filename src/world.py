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

    def __init__(self, realizations, set_index, alpha, H, Tf=10, h=1e-3, phi0=0, x0=0, y0=0, v0=1, eta=1):
        # Common parameters
        self.realizations = realizations
        self.set_index = set_index
        self.alpha = alpha
        self.H = H
        self.Tf = Tf
        self.h = h
        self.n = int(Tf / h)

        # Initial conditions
        self.phi0 = phi0
        self.v0 = v0
        self.x0 = x0
        self.y0 = y0

        # self_propulsion modulus
        self.eta = eta

        # Preallocate storage (to be specialized in subclasses)
        self.trajectories = []
        self.trajectory_sol = []

        # Noise Amplitude
        if self.alpha == (2-2*H):
            # print('running')
            self.A_H = 1#/np.sqrt(H*gamma(2*H))
            # self.A_H = 1#/np.sqrt(H*(2*H-1)*gamma(2*H-1))
            # print('scaling')
        else: 
            self.A_H = 1#/np.sqrt(2)
        # else:
        #     self.A_H = 1/(np.sqrt(2*H)*gamma(H+1/2))

        # Generalized diffusion coefficient 
        nominator = self.H*gamma(2*self.H)
        denominator = (self.alpha+self.H-1)*gamma(self.alpha)*gamma(self.alpha+2*self.H-1)
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

    # --------- Abstract Run --------- #
    def run_one(self, dB):
        """One trajectory (to be implemented in subclass)"""
        raise NotImplementedError

    def run(self):
        """Run all realizations"""
        self.trajectories = []
        for _ in tqdm(range(self.realizations)):
            self.make_B_H()
            traj = self.run_one()
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
        # print(self.trajectories[0])
        self.msd = np.mean((self.trajectories - self.trajectories[:, [0]])**2, axis=0)

    def compute_msd_sol(self):
        print(len(self.trajectory_sol))
        self.msd_sol = np.mean((self.trajectory_sol - self.trajectory_sol[:, [0]])**2, axis=0)

    def compute_mean(self):
        self.mean = np.mean(self.trajectories, axis=0)

    def compute_var(self):
        self.var = np.var(self.trajectories, axis=0)
    def compute_var_sol(self):
        self.var_sol = np.var(self.trajectory_sol, axis=0)

    # --------- Save/Load --------- #
    def save(self, folder="data", mode="phi"):
        os.makedirs(folder, exist_ok=True)
        filename = (f"{mode}_"
                    f"alpha{self.alpha}_"
                    f"H{self.H}_"
                    f"r{self.realizations}_"
                    f"Tf{self.Tf}_"
                    f"h{self.h}_" 
                    f"set{self.set_index}.pkl")
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

    def compute_var_an(self, time = 0):
        H = self.H
        alpha = self.alpha
        self.var_an = self.D_H*(self.t**(2*alpha+2*H-2))
        return self.D_H*(time**(2*alpha+2*H-2))
    
        # return (nominator/denominator)*((time*self.h)**(2*alpha+2*H-2))

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

    def run_one_solution(self):
        return convolution_weights(self.dB, self.t, self.alpha)

class xDirection(Base):
        
    """
    This class extends the general `Base` class to solve x equation·

    Parameters
    ----------

    """
    def __init__(self, phi_trajectories, **kwargs):
        super().__init__(**kwargs) #since init defined, it doesn't inherit init from parent
        self.phi_trajectories = phi_trajectories

    def run_one(self, realization_index):
        """
        Compute one trajectory of x for a single realization.
        """
        traj = np.zeros(self.n)
        
        for time in range(1, self.n):

            sum_noise = 0
            for i in range(1, time):
                sum_noise += self.cnj(time - i) * (traj[i] - traj[i-1])
            
            sum_phi = 0
            for i in range(1, time+1):
                sum_phi += self.cnj(time - i) * np.cos(self.phi_trajectories[realization_index, i]) * self.h
            
            coeff_noise = (self.h**self.alpha) * gamma(2 - self.alpha)
            traj[time] = traj[time-1] + coeff_noise * self.dB[time] - sum_noise + self.v0*sum_phi

        return traj

    def run(self):
        """Run all realizations - OVERWRITITNG!"""
        self.trajectories = []
        for r in tqdm(range(self.realizations)):
            self.make_B_H()
            traj = self.run_one(r)
            self.trajectories.append(traj)
        self.trajectories = np.array(self.trajectories)






