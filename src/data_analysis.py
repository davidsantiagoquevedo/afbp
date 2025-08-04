import numpy as np
from scipy.optimize import curve_fit

def gauss(x, *p):
    A, sigma = p
    return A*np.exp(-(x)**2/(2.*sigma**2))

def gauss_fit(data, bins):
    
    hist, bin_edges = np.histogram(data, density=True, bins=bins)
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2    
    
    # Gaussian fit
    # p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
    p0 = [1., 1.]

    coeff = curve_fit(gauss, bin_centres, hist, p0=p0)
    
    return coeff