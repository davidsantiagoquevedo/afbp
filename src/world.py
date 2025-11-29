import numpy as np
from scipy.special import gamma, gammainc
from scipy import stats
from fbm import FBM
import os
import pickle
from tqdm import tqdm
from integration import *
import random
import numba_functions as nb


# ---------- Base Class ---------- #
class Base:

    def __init__(self, alpha, H, Tf, h, realizations=1000, L_type='L1'):
        # Common parameters
        self.realizations = realizations
        self.alpha = alpha
        self.H = H
        self.Tf = Tf
        self.h = h
        self.n = int(Tf / h)
        self.L_type = L_type

        # Preallocate storage (to be specialized in subclasses)
        self.trajectories = []

        # Noise Amplitude
        self.A_H = 1/(np.sqrt(self.H*gamma(2-self.alpha) ))

    # Generalized diffusion coefficient 
    def calc_general_diff_coeff(self, alpha, H):
        nominator = H*gamma(2*H)
        denominator = (alpha+H-1)*gamma(alpha)*gamma(alpha+2*H-1)
        noise_intensity = (1)/(H*gamma(2-alpha))
        return noise_intensity*nominator/denominator

    # --------- Noise Generator --------- #
    def make_B_H(self, method='daviesharte'):
        np.random.seed()
        f = FBM(n=self.n, hurst=self.H, length=self.Tf, method=method)

        self.B_H = f.fbm()
        self.dB_H = np.diff(self.B_H) * (self.n / self.Tf)

        # print(self.A_H)
        self.B = self.A_H*self.B_H
        self.dB = self.A_H*self.dB_H

        self.t_BH = f.times()
        self.t = self.t_BH[:self.n]

        return 

    # --------- Utilities --------- #
    def cnj(self, k):
        return (k+1)**(1-self.alpha) - k**(1-self.alpha)

    def nxt_func(self, phit):
        nt = np.zeros(len(phit))
        for j in range(len(phit)):
            if j==0:
                nt[j] = np.cos(phit[j])*self.h
            else:
                nt[j] = nt[j-1] + np.cos(phit[j])*self.h
        return nt
    
    def nyt_func(self, phit):
        nt = np.zeros(len(phit))
        for j in range(len(phit)):
            if j==0:
                nt[j] = np.sin(phit[j])*self.h
            else:
                nt[j] = nt[j-1] + np.sin(phit[j])*self.h
        return nt

    def run(self):
        """Run all realizations"""
        self.trajectories = []
        for r in tqdm(range(self.realizations)):
            self.make_B_H()
            if isinstance(self, Angular):
                # Two discretization types implemented for angular equations
                if self.L_type == 'L1':         
                    traj = self.run_one_L1()
                elif self.L_type == 'L2':
                    traj = self.run_one_L2()
            else:
                traj = self.run_one(r)
            self.trajectories.append(traj)
        self.trajectories = np.array(self.trajectories)

    def run_numba(self):
        """Run all realizations"""
        self.trajectories = []
        cnj_array = np.zeros(self.n)
        for time in range(1, self.n):
            cnj_array[time] = self.cnj(time)
        coeff_noise = (self.h ** self.alpha) * gamma(2 - self.alpha)


        for r in tqdm(range(self.realizations)):
            self.make_B_H()

            if isinstance(self, Angular):
                traj = nb.run_one_phi(self.n, self.phi0, cnj_array, coeff_noise, self.dB)
            else:
                if isinstance(self, xDirection):
                    nt_array = nb.nxt_func(self.phi_trajectories[r], self.h)
                if isinstance(self, yDirection):
                    nt_array = nb.nyt_func(self.phi_trajectories[r], self.h)
                traj = nb.run_one(self.n, self.ups, nt_array, cnj_array, coeff_noise, self.dB, traj0=0)
            self.trajectories.append(traj)
        self.trajectories = np.array(self.trajectories)
 
    # --------- Stats --------- #
    def confidence_intervals(self, data, p):
        N = data.shape[0]
        z_p = stats.t.ppf(1-(1-p)/2, df=N-1)
        std = data.std(axis=0, ddof=1)
        se = std / np.sqrt(N)
        return z_p*se

    def compute_msd(self, p=0.95):
        # print(np.shape(self.trajectories))
        sqdis = (self.trajectories - self.trajectories[:, [0]])**2 
        ci = self.confidence_intervals(data = sqdis, p = p)
        self.msd = np.mean(sqdis, axis=0)
        self.msd_upper_ci = self.msd + ci
        self.msd_lower_ci = self.msd - ci

    def compute_mean(self):
        self.mean = np.mean(self.trajectories, axis=0)

    def compute_var(self):
        self.var = np.var(self.trajectories, axis=0)
        
        
    # --------- Save/Load --------- #
    def save(self, set_label, folder="data_tests", mode="phi"):
        
        if isinstance(self, Angular):
            alphaH = f"alphaR{self.alpha}_HR{self.H}"
        elif isinstance(self, xDirection) or isinstance(self, yDirection):
            alphaH = f"alphaT{self.alpha}_HT{self.H}_alphaR{self.alphaR}_HR{self.HR}_ups{self.ups}"
            delattr(self, "phi_trajectories") #removed to avoid duplicating information
        else:
            alphaH = f"alphaT{self.alpha}_HT{self.H}_alphaR{self.alphaR}_HR{self.HR}_ups{self.ups}"
            delattr(self, "x_trajectories") #removed to avoid duplicating information
            delattr(self, "y_trajectories") #removed to avoid duplicating information
        os.makedirs(folder, exist_ok=True)
        filename = (f"{self.L_type}_"
                    f"{mode}_"
                    f"{alphaH}_"
                    f"r{self.realizations}_"
                    f"Tf{self.Tf}_"
                    f"h{self.h}_" 
                    f"set{set_label}_AHfdt.pkl")
        filepath = os.path.join(folder, filename)
        print(filepath)
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
    
    def __init__(self,phi0 = 0, **kwargs):
        
        super().__init__(**kwargs)
        # self.phi0 = 0
        self.phi0 = np.pi*random.random()
        
    def compute_orientation_corr(self, p=0.95):
        cos_dphi = np.cos(self.trajectories-self.trajectories[:, [0]])
        ci = self.confidence_intervals(data = cos_dphi, p = p)
        self.orientation_corr = cos_dphi.mean(axis=0)
        self.orientation_corr_upper_ci = self.orientation_corr + ci
        self.orientation_corr_lower_ci = self.orientation_corr - ci
        
    def compute_orientation_corr_an(self):
        H = self.H
        alpha = self.alpha
        D_H = self.calc_general_diff_coeff(alpha, H)
        self.make_B_H() #generate time
        self.orientation_corr_an = np.exp((-D_H/2)*np.abs(self.t)**alpha)

    def compute_msd_an(self, time = None, tl = 0):
        H = self.H
        alpha = self.alpha
        D_H = self.calc_general_diff_coeff(alpha, H)

        if time is None:
            self.make_B_H() #generate time
            self.msd_an = D_H*(self.t**(2*alpha+2*H-2)-tl**(2*alpha+2*H-2))
        else:
            return D_H*(time**(2*alpha+2*H-2)-tl**(2*alpha+2*H-2))
            # return (1/(2*H*gamma(2-alpha)))*(time**(alpha))

    def propagator(self, time_index, tref, tl=0):
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

        variance = self.compute_var_an(time = np.abs((time_index*self.h - tref)), tl = tl)
        factor = np.sqrt( 1 / (2*np.pi*variance) )
        argument = (-(x)**2) / (2*variance)

        P = factor*np.exp(argument)

        return x, P
    
    def run_one_L1(self):
        # Loop over timesteps
        # traj = np.zeros(self.n)
        traj = np.ones(self.n) * self.phi0
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
        return (1/(2-alpha)) * ((l+1)**(2-alpha) - (l)**(2-alpha)) - 0.5 * ((l+1)**(1-alpha) + (l)**(1-alpha))
    
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
        
    def run_one_L2(self):
        c = self.c
        # Loop over timesteps
        traj = np.zeros(self.n)
        
        for j in range(0, self.n-1):
            c_0 = c(j,j)    
            if j == 0:
                sum_term = 0                
            else:
                # Sum term
                sum_term = 0
                for s in range(0, j):
                    
                    sum_term += c(j,s) * (traj[s+1]-traj[s])

            # Update rule
            coeff_noise = ((self.h)**(self.alpha)) * (gamma(2-self.alpha))/c_0

            
            traj[j+1] = traj[j] + coeff_noise*self.dB[j] - sum_term/c_0
        
        return traj

class xDirection(Base):
        
    """
    This class extends the general `Base` class to solve x equation·

    Parameters
    ----------

    """
    def __init__(self, phi, x0=0, ups=1, AHT=1, **kwargs):
        
        super().__init__(**kwargs) #since init defined, it doesn't inherit init from parent
        
        # initial condition
        self.x0 = x0
        # self_propulsion modulus
        self.ups = ups
        
        self.phi_trajectories = phi.trajectories
        self.alphaR = phi.alpha
        self.HR = phi.H
        self.DHR = self.calc_general_diff_coeff(self.alphaR, self.HR)

        if self.realizations != phi.realizations:
            self.realizations = phi.realizations
            
    def run_one(self, realization_index):
        """
        Compute one trajectory of x for a single realization.
        """
        traj = np.zeros(self.n)

        phi_trajectory = self.phi_trajectories[realization_index]
        nt = self.nxt_func(phi_trajectory)
        
        for time in range(1, self.n):

            sum_x = 0
            for i in range(1, time): 
                sum_x += self.cnj(time - i) * (traj[i] - traj[i-1])
            
            sum_phi = 0
            for i in range(1, time):

                sum_phi += self.cnj(time - i) * (nt[i]-nt[i-1]) 
            
            coeff_noise = (self.h**self.alpha) * gamma(2 - self.alpha)
            traj[time] = traj[time-1] + coeff_noise * self.dB[time] - sum_x + self.ups*sum_phi + (nt[time]-nt[time-1])

        return traj

class yDirection(Base):
        
    """
    This class extends the general `Base` class to solve y equation·

    Parameters
    ----------

    """
    def __init__(self, phi=None, y0=0, ups=1, **kwargs):
        
        super().__init__(**kwargs) #since init defined, it doesn't inherit init from parent
           
         # initial condition
        self.y0 = y0
        # self_propulsion modulus
        self.ups = ups
        
        self.phi_trajectories = phi.trajectories
        self.alphaR = phi.alpha
        self.HR = phi.H
        self.DHR = self.calc_general_diff_coeff(self.alphaR, self.HR)

        if self.realizations != phi.realizations:
            self.realizations = phi.realizations

    def run_one(self, realization_index):
        """
        Compute one trajectory of y for a single realization.
        """                                                              
        traj = np.zeros(self.n)

        phi_trajectory = self.phi_trajectories[realization_index]
        nt = self.nyt_func(phi_trajectory)

        for time in range(1, self.n):

            sum_y = 0
            for i in range(1, time): 
                sum_y += self.cnj(time - i) * (traj[i] - traj[i-1])
            
            sum_phi = 0
            for i in range(1, time):
                sum_phi += self.cnj(time - i) * (nt[i]-nt[i-1])
                    
            coeff_noise = (self.h**self.alpha) * gamma(2 - self.alpha)
            traj[time] = traj[time-1] + coeff_noise * self.dB[time] - sum_y + self.ups*sum_phi + (nt[time]-nt[time-1])

        return traj

class rModulus(Base):
        
    """
    This class extends the general `Base` class to solve r equation·

    Parameters
    ----------

    """
    def __init__(self, x=None, y=None, ups=None, alphaR=None, HR=None, **kwargs):
        super().__init__(**kwargs) #since init defined, it doesn't inherit init from parent
        
        # inherit from x and y classes if passed
        if x is not None:
            self.x_trajectories = x.trajectories
            self.y_trajectories = y.trajectories
            # translational properties
            self.ups = x.ups
            self.alphaT = x.alpha
            self.HT = x.H
            self.AHT = 1/(np.sqrt( self.HT*(2*self.HT-1)*gamma(2*self.HT-1) ))

            # rotational properties
            self.alphaR = x.alphaR
            self.HR = x.HR
        # read as input if only interested in analytical expression
        else:
            # translational properties
            self.ups = ups
            self.alphaT = self.alpha
            self.HT = self.H
            # rotational properties
            self.alphaR =alphaR
            self.HR = HR

    def compute_r_modulus(self):
        
        self.trajectories = np.sqrt(self.x_trajectories**2+self.y_trajectories**2)
        
    def compute_msd_an(self, total = True):
        alphaT = self.alpha
        HT = self.H
        alphaR = self.alphaR
        HR = self.HR
        DHT = self.calc_general_diff_coeff(alphaT, HT)
        DHR = self.calc_general_diff_coeff(alphaR, HR)
        ups = self.ups
        self.make_B_H()
        t = self.t 
        
        aux_var = alphaR + HR - 1

        coeff = ( ups**2 / (aux_var*((DHR/2)**(1/aux_var))) )
        gamma1 = gamma(1/(2*aux_var))*gammainc(1/(2*aux_var), (DHR*t**(2*aux_var))/2)
        gamma2 = gamma(1/(aux_var))*gammainc(1/  (aux_var), (DHR*t**(2*aux_var))/2)
    
        if total:
            self.msd_an =  coeff*( gamma1*((DHR/2)**(1/(2*aux_var)))*t - gamma2  ) + 2*DHT*(t**(2*alphaT+2*HT-2))
        else:
            self.msd_an =  coeff*( gamma1*((DHR/2)**(1/(2*aux_var)))*t - gamma2  )


    def compute_msd_fbm(self, time, total = True):
        alphaT = self.alpha
        HT = self.H
        alphaR = self.alphaR
        HR = self.HR
        DHT = self.calc_general_diff_coeff(alphaT, HT)
        DHR = self.calc_general_diff_coeff(alphaR, HR)
        ups = self.ups
        

        DHR = DHR/(alphaR+HR-1)
        DHT = DHT/(alphaT+HT-1)

        coeff = ( 2*ups**2 / ((DHR/2)**(2))) 
        gamma1 = (DHR/2)*time
        gamma2 = np.exp(-(DHR/2)*time) 
    
        if total:
            return  coeff*( gamma1 + gamma2 - 1 ) + 2*DHT*(time**(2*alphaT+2*HT-2))
        else:
            # print(DHT)
            return   coeff*( gamma1 + gamma2 - 1 )

