import numpy as np
from scipy.special import gamma
import pandas as pd
import mittag_leffler as ml
from fbm import FBM
import os
import pickle

class Agent():
    def __init__(self, **kwargs):
    
        self.alpha = kwargs.get('alpha')
        self.H = kwargs.get('H')
        self.Tf = kwargs.get('Tf')
        self.h = kwargs.get('h')
        self.T0 = kwargs.get('T0', 0)
        self.phi0 = kwargs.get('phi0', 0)
        self.thetaR = kwargs.get('thetaR', 100)
        self.n = kwargs.get('n')

        # Initialize solution of fractional Langevin equation
        self.phi_vec = np.zeros(self.n)
        self.phi_prev = self.phi0

        # Define fractional noise BH specific for this agent
        n = self.n
        # H = (2 - self.alpha)/2
        Tf = self.Tf
        
        f = FBM(n = n, hurst = self.H, length = Tf, method = 'daviesharte')
        self.B_H = f.fbm()
        self.t_BH = f.times()
        self.t = self.t_BH[:self.n]

    def update_phi(self, time):

        sum_term = 0
        if time-2>=0:
            for i in range(time-2):
                sum_term += (self.phi_vec[i]+self.phi_vec[i+1])*((time-i)**(1-self.alpha)-(time-i-1)**(1-self.alpha))
                # sum_term += (self.phi_vec[i]+self.phi_vec[i+1])*((time-i-1)**(1-self.alpha)-(time-i)**(1-self.alpha))

        phi_current = - self.phi_prev + 2*(self.h)**(self.alpha-1)*(self.phi0+self.thetaR*gamma(2-self.alpha)*self.B_H[time]) - sum_term
        # phi_current = - self.phi_prev - 2*(self.h)**(self.alpha-1)*(self.phi0+self.thetaR*gamma(2-self.alpha)*self.B_H[time]) + sum_term

        self.phi_vec[time] = phi_current
        self.phi_prev = np.copy(phi_current)

    def trajectory(self):
        for time in range(self.n):
            self.update_phi(time)

class Env():

    def __init__(self, 
                 numb_agents,
                 alpha,
                 H,
                 Tf, 
                 h = 1e-4,
                 T0 = 0, 
                 phi0=0, 
                 thetaR=0.01):
        
        # Parameters
        self.numb_agents = numb_agents
        self.alpha = alpha
        self.H = H
        self.Tf = Tf
        self.h = h
        self.T0 = T0
        self.phi0 = phi0
        self.thetaR = thetaR
        
        # Number of time steps
        self.n = int(self.Tf/self.h)

        
        # Initialize 
        self.phi_matrix = None
        self.phi_corr = None

    def define_agents(self):
        
        # Define agents part of the env with their fractional noise
        self.agents = [Agent(**self.__dict__) for _ in range(self.numb_agents)]

    def run(self):
            for agent_index, agent in enumerate(self.agents):
                print("----Running for alpha", self.alpha, 'agent', agent_index)

                agent.trajectory()

            # Store all trajectories in phi_matrix
            self.phi_matrix = np.array([agent.phi_vec for agent in self.agents])

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
            f"numbag_{self.numb_agents}_"
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
    
