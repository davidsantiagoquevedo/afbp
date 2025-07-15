
import matplotlib.pyplot as plt
import fLe as fle

bby1 = fle(alpha = 0.05)
bby1.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby1.msd_underdamped()
bby1.msd_overdamped()

bby2 = fle(alpha = 0.1)
bby2.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby2.msd_underdamped()
bby2.msd_overdamped()

bby3 = fle(alpha = 0.3)
bby3.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby3.msd_underdamped()
bby3.msd_overdamped()

bby4 = fle(alpha = 0.5)
bby4.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby4.msd_underdamped()
bby4.msd_overdamped()

bby5 = fle(alpha = 0.7)
bby5.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby5.msd_underdamped()
bby5.msd_overdamped()

bby6 = fle(alpha = 0.9)
bby6.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby6.msd_underdamped()
bby6.msd_overdamped()

bby7 = fle(alpha = 1)
bby7.params(Tf=30, T0 = 0, v0 = 1, M = 1, eta = 1, T = 1)
bby7.msd_underdamped()
bby7.msd_overdamped()

fig, ax = plt.subplots()

ax.plot(bby1.t, bby1.msd_o, label=r"$\alpha$=0.05")
ax.plot(bby2.t, bby2.msd_o, label=r"$\alpha$=0.1")
ax.plot(bby3.t, bby3.msd_o, label=r"$\alpha$=0.3")
ax.plot(bby4.t, bby4.msd_o, label=r"$\alpha$=0.5")
ax.plot(bby5.t, bby5.msd_o, label=r"$\alpha$=0.7")
ax.plot(bby6.t, bby6.msd_o, label=r"$\alpha$=0.9")
ax.plot(bby7.t, bby7.msd_o, label=r"$\alpha$=1")
fig.show()

fig, ax = plt.subplots()

ax.plot(bby1.t, bby1.msd_o, label=r"$\alpha$=0.05")
ax.plot(bby1.t, bby1.msd_u, color = "red")
ax.plot(bby2.t, bby2.msd_o, label=r"$\alpha$=0.1")
ax.plot(bby2.t, bby2.msd_u, color = "red")
ax.plot(bby3.t, bby3.msd_o, label=r"$\alpha$=0.3")
ax.plot(bby3.t, bby3.msd_u, color = "red")
ax.plot(bby4.t, bby4.msd_o, label=r"$\alpha$=0.5")
ax.plot(bby4.t, bby4.msd_u, color = "red")
fig.show()