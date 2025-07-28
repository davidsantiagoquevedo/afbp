import numpy as np
from scipy.special import gamma
import sys
sys.path.append("src/")
import integration as it
import world as wd
from importlib import reload
reload(wd)
import matplotlib.pyplot as plt

alpha = 0.2
H = (2-alpha)/2

phi = wd.angular_fbm(realizations = 1, 
                  alpha = alpha,
                  H = H,
                  Tf = 1,
                  h = 0.01,
                  phi0 = 0
                  )

phi.make_B_H()
num = phi.trajectory()
anl = phi.trajectory_solution()

fig, ax = plt.subplots()
ax.plot(phi.t, num, label = "good, but not that good")
ax.plot(phi.t, anl, ls=":", label = "analytical")
fig.legend()
fig.savefig("convolution.png", dpi=500)

