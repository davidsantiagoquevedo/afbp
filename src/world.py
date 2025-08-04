import numpy as np
from scipy.special import gamma
import pandas as pd
import mittag_leffler as ml
from fbm import FBM
import os
import pickle
from tqdm import tqdm
from integration import *

class angular_fbm():

    def __init__(self, 
                 realizations,
                 set_index,
                 alpha,
                 H,
                 Tf = 1, 
                 h = 1e-3,
                 T0 = 0, 
                 phi0=0, 
                 thetaR=1):
        
        # Parameters in
        self.realizations = realizations
        self.set_index = set_index
        self.alpha = alpha
        self.H = H
        self.Tf = Tf
        self.h = h
        self.T0 = T0
        self.phi0 = phi0
        self.thetaR = thetaR
        
        # Number of time steps
        self.n = int(self.Tf/self.h)
        
        # Noise amplitude
        if self.alpha == 1:
            self.A_H = np.sqrt(2)
        else:
            self.A_H = 1/np.sqrt(H*(2*H-1)*gamma(2*H-1))
        
        # Initialize matrices
        self.phi_matrix = np.full(self.n, self.phi0)
        self.phi_matrix_solution = np.full(self.n, self.phi0)
        self.phi_corr = None
        self.phi_corr_sol = None
        self.mean = None
        self.mean_sol = None
        self.variance = None
        self.variance_sol = None

    def make_B_H(self, method = 'daviesharte'):
        np.random.seed()
          
        f = FBM(n = self.n, hurst = self.H, length = self.Tf, method = method)

        self.B_H = f.fbm()
        self.dB_H = self.n/self.Tf*np.diff(self.B_H)
        self.d2B_H = self.n/self.Tf*np.diff(self.dB_H)

        self.t_BH = f.times()
        self.t = self.t_BH[:self.n]
        self.t_d2BH = self.t_BH[:(self.n-1)]

        self.B = self.A_H*self.B_H
        self.dB = self.A_H*self.dB_H
        self.d2B = self.A_H*self.d2B_H
        
    def cnj(self, k):
        return (k+1)**(1-self.alpha) - k**(1-self.alpha)
        
    def trajectory(self):       
        # Loop over timesteps
        r_trajectory = np.zeros(self.n)
        for time in range(1, self.n):
            
            # Sum term
            sum_term = 0
            for i in range(1, time-1):
                
                sum_term += self.cnj(time-i) * (r_trajectory[i]-r_trajectory[i-1])
            
            # Update rule
            coeff_noise = ((self.h)**(self.alpha)) * (gamma(2-self.alpha))
            r_trajectory[time] = r_trajectory[time-1] + coeff_noise*self.dB[time] - sum_term
            
        return r_trajectory

    def run(self):
            for r in tqdm(range(self.realizations)):
                np.random.seed()
                self.make_B_H()
                r_trajectory = self.trajectory()

                self.phi_matrix = np.vstack((self.phi_matrix, r_trajectory))
                
    def relaxation(self, t):
        coeff = 1/gamma(self.alpha)
        result = coeff * (t**(self.alpha-1))
        return result #np.where(np.isinf(result), 0, result)

    def relaxation_primitive(self, t):
        coeff = 1/(self.alpha*gamma(self.alpha))
        result = coeff * (t**(self.alpha))
        return result 

    def trajectory_solution(self):
        # self.make_B_H()
        # print(self.B_H)
        # return convolution(self.relaxation, self.dB, self.t)
        # return convolution_by_parts(self.relaxation_primitive, self.d2B, self.dB, self.t_d2BH)
        return convolution_weights(self.dB, self.t, self.alpha)
                
    def run_solution(self):
        
        for _ in tqdm(range(self.realizations)):
            self.make_B_H()
            r_trajectory = self.trajectory_solution()

            self.phi_matrix_solution = np.vstack((self.phi_matrix_solution, r_trajectory))
           
    def compute_mean(self):
        
        self.mean = np.mean(self.phi_matrix, axis=0)
        self.mean_sol = np.mean(self.phi_matrix_solution, axis=0)
     
    def compute_variance(self):
        
        self.variance = np.var(self.phi_matrix, axis=0)
        self.variance_sol = np.var(self.phi_matrix_solution, axis=0)
            
    def compute_phi_correlation(self):
        
        """
        Computes < [phi(t) - phi0]^2 > averaged over all agents.
        
        Parameters:
        
        ...
        
        Returns:
            self.phi_corr: array of shape (n)
        """
        
        # if self.phi_matrix is None:
        #     print(self.phi_matrix)
        #     self.run()
            
        # print(self.phi_matrix.shape)
        self.phi_corr = np.mean((self.phi_matrix - self.phi0)**2, axis=0)
        # print(self.phi_corr.shape)
        self.phi_corr_sol = np.mean((self.phi_matrix_solution - self.phi0)**2, axis=0)

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
            f"h_{self.h}_"
            f"set_{self.set_index}.pkl"
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
