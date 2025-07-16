import numpy as np
from scipy.special import gamma
import pandas as pd
import mittag_leffler as ml
from fbm import FBM
import os
import pickle

class afbm():

    def __init__(self, 
                 realizations,
                 alpha,
                 H,
                 Tf, 
                 h = 1e-4,
                 T0 = 0, 
                 phi0=0, 
                 thetaR=1):
        
        # Parameters
        self.realizations = realizations
        self.alpha = alpha
        self.H = H
        self.Tf = Tf
        self.h = h
        self.T0 = T0
        self.phi0 = phi0
        self.thetaR = thetaR
        
        # Number of time steps
        self.n = int(self.Tf/self.h)
        
        # Initialize matrices
        self.phi_matrix = np.full(self.n, self.phi0)
        self.phi_corr = None

    def trajectory(self):
        
        # Generate noise 
        f = FBM(n = self.n, hurst = self.H, length = self.Tf, method = 'daviesharte')
        # B_H = f.fbm()
        B_H = f.fbm()/np.sqrt(self.H*(2*self.H-1)*gamma(2*self.H-1))
        
        # Loop over timesteps
        r_trajectory = np.zeros(self.n)
        phi_prev = self.phi0
        for time in range(1, self.n):
            
            # Sum term
            sum_term = 0
            if time-2>=0:
                for i in range(time-1):
                    sum_term += (r_trajectory[i]+r_trajectory[i+1])*((self.n-i)**(1-self.alpha)-(self.n-i-1)**(1-self.alpha))
            
            # Update rule

            phi_current = - phi_prev + 2*(self.h)**(self.alpha-1)*(self.thetaR*gamma(2-self.alpha)*(B_H[time])) - sum_term

            # Save and update old 
            r_trajectory[time] = phi_current
            phi_prev = np.copy(phi_current)
            
        return r_trajectory

    def cnj(self, k):
        return (k+1)**(1-self.alpha) - k**(1-self.alpha)

    def trajectory_new_discr(self):
        
        # Generate noise 
        f = FBM(n = self.n, hurst = self.H, length = self.Tf, method = 'daviesharte')
        B_H = f.fbm()
        # B_H = f.fbm()/np.sqrt(self.H*(2*self.H-1)*gamma(2*self.H-1))
        
        dB_H = self.n/self.Tf*np.diff(B_H)
        
        # Loop over timesteps
        r_trajectory = np.zeros(self.n)
        phi_prev = self.phi0
        for time in range(1, self.n):
            
            # Sum term
            sum_term = 0
            for i in range(1, time-1):
                
                sum_term += self.cnj(time-i) * (r_trajectory[i]-r_trajectory[i+1])
            
            # Update rule
            phi_current = phi_prev + ((self.h)**(self.alpha))*(gamma(2-self.alpha)*dB_H[time]) + sum_term

            # Save and update old 
            r_trajectory[time] = phi_current
            phi_prev = np.copy(phi_current)
            
        return r_trajectory
    
    def bi(self, k):
        
        return (k+1)**(1-self.alpha) - k**(1-self.alpha)
    
    def trajectory_new_discr2(self):
        
        # Generate noise 
        f = FBM(n = self.n, hurst = self.H, length = self.Tf, method = 'daviesharte')
        B_H = f.fbm()
        # B_H = f.fbm()/np.sqrt(self.H*(2*self.H-1)*gamma(2*self.H-1))
        
        dB_H = self.n/self.Tf*np.diff(B_H)
        
        # Loop over timesteps
        r_trajectory = np.zeros(self.n)
        phi_prev = self.phi0
        for time in range(1, self.n):
            
            # Sum term
            sum_term = 0
            for i in range(1, time-1):
                
                sum_term += self.bi(time) * (r_trajectory[i])
            
            # Update rule
            phi_current = ((self.h)**(self.alpha))*(gamma(2-self.alpha)*dB_H[time]) + sum_term

            # Save and update old 
            r_trajectory[time] = phi_current
            phi_prev = np.copy(phi_current)
            
        return r_trajectory

    def run(self):
            for r in range(self.realizations):
                # print("----Running for alpha", self.alpha, 'realization', r)

                # r_trajectory = self.trajectory()
                r_trajectory = self.trajectory_new_discr()
                # r_trajectory = self.trajectory_new_discr2()

                self.phi_matrix = np.vstack((self.phi_matrix, r_trajectory))
                
    def compute_phi_correlation(self):
        
        """
        Computes < [phi(t) - phi0]^2 > averaged over all agents.
        
        Parameters:
        
        ...
        
        Returns:
            self.phi_corr: array of shape (n)
        """
        
        if self.phi_matrix is None:
            self.run()
            
        self.phi_corr = np.mean((self.phi_matrix - self.phi0)**2, axis=0)
        return self.phi_corr

    def compute_pdf(self, time, bins=150):

        if self.phi_matrix is None:
            raise ValueError("Run the simulation first to generate phi_matrix.")

        phi_time = self.phi_matrix[:, time]
        hist, bin_edges = np.histogram(phi_time, bins=bins, density=True)
        return hist, bin_edges

    def save(self, folder="data"):
        """
        Save the entire Env object to a .pkl file in the specified folder.
        The filename includes key parameters.
        """
        os.makedirs(folder, exist_ok=True)
        
        filename = (
            f"r_{self.realizations}_"
            f"alpha_{self.alpha}_"
            f"H_{self.H}_"
            f"Tf_{self.Tf}_"
            f"h_{self.h}.pkl"
        )
        
        filepath = os.path.join(folder, filename)
        
        with open(filepath, "wb") as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, filepath):
        """
        Load an Env object from a .pkl file.
        """
        with open(filepath, "rb") as f:
            env = pickle.load(f)
            
        return env
