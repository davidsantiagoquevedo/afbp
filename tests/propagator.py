import numpy as np
from scipy.special import gamma
import sys
sys.path.append("src/")
import integration as it


def F(H,T):
    """Normalization constant of the propagator

    Args:
        H (float): Hurst exponente
        t (ndarray): Time to evaluate

    Returns:
        ndarray: Normalization constant
    """
    return np.sqrt(H/np.pi)*(gamma(H+1/2))/(T**H)


def A_H(alpha,H):
    kBT = 1
    eta = 1
    theta = np.sqrt(kBT*eta/(H*(2*H-1)*gamma(1-alpha)))
    return eta/theta

def I_phi(alpha, t, phi_t):
    def f(t):
        return t**(-alpha)
    return it.convolution(f,phi_t, t)
    

def S(alpha, H, phi0, T):
    num = H*(gamma(H+1/2)**2)*A_H(alpha,H)
    den = (gamma(1-alpha)**2)*(T**(2*H))
    
    I = I_phi()
    
    