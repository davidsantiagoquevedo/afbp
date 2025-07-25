import numpy as np
from scipy.special import gamma
import sys
sys.path.append("src/")
import integration as it
import world as wd
from importlib import reload
reload(wd)
import matplotlib.pyplot as plt

alpha = 0.5
H = (2-alpha)/2


phi = wd.angular_fbm(realizations = 1, 
                  alpha = alpha,
                  H = H,
                  Tf = 1,
                  h = 0.001,
                  phi0 = 0
                  )

phi.make_B_H()
num_bad = phi.trajectory_bad()
num = phi.trajectory()
anl = phi.trajectory_solution()

fig, ax = plt.subplots(2,1)
ax[0].plot(phi.t, num, label = "good, but not that good")
ax[0].plot(phi.t, anl, ls=":", label = "analytical")
fig.legend()
plt.show()


1/0.01**(1-0.01)