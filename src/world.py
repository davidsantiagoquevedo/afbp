import numpy as np
from scipy.special import gamma
import pandas as pd
import mittag_leffler as ml
from fbm import FBM

class Agent():
    def __init__(self, **kwargs):
    
        self.alpha = kwargs.get('alpha')
        self.H = kwargs.get('H')
        self.Tf = kwargs.get('Tf')
        self.h = kwargs.get('h')
        self.T0 = kwargs.get('T0', 0)
        self.phi0 = kwargs.get('phi0', 0)
        self.thetaR = kwargs.get('thetaR', 1)
        self.n = kwargs.get('n')

        # Initialize solution of fractional Langevin equation

        self.phi_vec = []
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

        phi_current = - self.phi_prev + 2*(self.h)**(self.alpha-1)*(self.phi0+self.thetaR*gamma(2-self.alpha)*self.B_H[time]) - sum_term

        self.phi_vec.append(phi_current)
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
        
        self.numb_agents = numb_agents
        self.alpha = alpha
        self.H = H
        self.Tf = Tf
        self.h = h
        self.T0 = T0
        self.phi0 = phi0
        self.thetaR = thetaR

        self.n = int(self.Tf/self.h)

        self.agents = [Agent(**self.__dict__) for _ in range(self.numb_agents)]

    def update_phis(self):
        for agent in self.agents:
            agent.update_phi()

    
