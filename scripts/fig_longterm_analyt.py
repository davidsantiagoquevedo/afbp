import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot

alpha = [1, 0.7, 0.5, 0.3, 0.2]
H = [(2 - a) / 2 for a in alpha]    #fluc-diss

##########################################################
fig, ax = plt.subplots(figsize=(9, 7))

Tf = 70
h = 0.05

for i, ai in enumerate(alpha):
    hi = H[i]

    phi = Angular(alpha=ai, H=hi, Tf=Tf, h=h)
    phi.compute_msd_an()
    plot.plot_moment(ax, phi, 'msd', 'an')
    if i == 0:
        plot.add_trend(ax, x0 = 0, xf = Tf, func = plot.t, text = r"$~t$", xtext = 3, dy = -0.7)

# ax.set_xscale("log")
# ax.set_yscale("log")
ax.set_xlim(xmin = h)
fig.tight_layout()
fig.savefig(f"plots/analytics/phi_alphaR{alpha}_HR{H}_Tf{Tf}_h{h}_log.png", dpi=100)

##########################################################
alphaR = alpha
HR = H
##########################################################

fig, ax = plt.subplots(figsize=(9, 7))

Tf = 70
h = 0.05
ups = 1

linear = 1
for i, ai in enumerate(alpha):
    hi=H[i]
    aRi=alphaR[i]
    hRi=HR[i]

    r = rModulus(alpha=ai, H=hi, alphaR=aRi, HR=hRi, ups=ups, Tf=Tf, h=h)

    r.compute_msd_an(total=False)
    plot.plot_moment(ax, r, 'msd', 'an')
ax.set_xlim(xmin = h)
fig.tight_layout()
fig.savefig(f"plots/analytics/ra_alphaT{alpha}_HT{H}_alphaR{alphaR}_HR{HR}_Tf{Tf}_h{h}_ups{ups}.png", dpi=100)

##########################################################

fig, ax = plt.subplots(figsize=(9, 7))

Tf = 70
h = 0.05
ups = 1

linear = 1
for i, ai in enumerate(alpha):
    hi=H[i]
    aRi=alphaR[i]
    hRi=HR[i]

    r = rModulus(alpha=ai, H=hi, alphaR=aRi, HR=hRi, ups=ups, Tf=Tf, h=h)

    r.compute_msd_an(total=False)
    plot.plot_moment(ax, r, 'msd', 'an')

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(xmin = h)
fig.tight_layout()
fig.savefig(f"plots/analytics/ra_alphaT{alpha}_HT{H}_alphaR{alphaR}_HR{HR}_Tf{Tf}_h{h}_ups{ups}_log.png", dpi=100)

##########################################################
fig, ax = plt.subplots(figsize=(9, 7))

Tf = 70
h = 0.05
ups = 10

linear = 1
for i, ai in enumerate(alpha):
    hi=H[i]
    aRi=alphaR[i]
    hRi=HR[i]

    r = rModulus(alpha=ai, H=hi, alphaR=aRi, HR=hRi, ups=ups, Tf=Tf, h=h)

    r.compute_msd_an()
    plot.plot_moment(ax, r, 'msd', 'an')

ax.set_xlim(xmin = h)
fig.tight_layout()
fig.savefig(f"plots/analytics/r_alphaT{alpha}_HT{H}_alphaR{alphaR}_HR{HR}_Tf{Tf}_h{h}_ups{ups}.png", dpi=100)


##########################################################
fig, ax = plt.subplots(figsize=(9, 7))

Tf = 70
h = 0.05
ups = 100

linear = 1
for i, ai in enumerate(alpha):
    hi=H[i]
    aRi=alphaR[i]
    hRi=HR[i]

    r = rModulus(alpha=ai, H=hi, alphaR=aRi, HR=hRi, ups=ups, Tf=Tf, h=h)

    r.compute_msd_an()
    plot.plot_moment(ax, r, 'msd', 'an')

    if i == 0:
        # plot.add_trend(ax, x0 = 0, xf = Tf, func = plot.t, text = r"$~t$", xtext = 3, dy = -0.7)
        plot.add_trend(ax, x0 = 12, xf = Tf, y0=0.6, func = plot.t2, text = r"$~t^2$", xtext = 24, dy = 100, fontsize=15)
        plot.add_trend(ax, x0 = 12, xf = Tf, y0=3, func = plot.t, text = r"$~t$", xtext = 24, dy = 22, fontsize=15)
        plot.add_trend(ax, x0 = 0, xf = 0.3, y0=1.3, func = plot.talpha, text = fr"$~t$", xtext = 3 , dx=-2.9, dy = -2.91, alpha=ai, fontsize=15)

    if i == (len(alpha)-1):
        
        plot.add_trend(ax, x0 = 0, xf = 0.2, y0=4.6, func = plot.talpha, text = fr"$~t^{{{ai}}}$", xtext = 3, dx = -2.9, dy = 2.9, alpha=ai, fontsize=15)


ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(xmin = h)
fig.tight_layout()
fig.savefig(f"plots/analytics/r_alphaT{alpha}_HT{H}_alphaR{alphaR}_HR{HR}_Tf{Tf}_h{h}_ups{ups}_log.png", dpi=100)


