import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,10,100)
t_ref = 5
t_min = np.array([min(t_ref,ti) for ti in t])

alpha = 0.7
H = 0.5
pw = alpha - 2*H

var = -(np.abs(t-t_ref)**pw)*(t_min**alpha)

plt.plot(t, var)
plt.savefig("plots/tests/test_var.png")
