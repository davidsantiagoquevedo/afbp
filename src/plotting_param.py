legend_size = 13
axis_fontsize = 19
size_ticks = 20
marker_size = 10
title_fontsize = 15
size_labels_figures =16

msd_style = {
    'sim': dict(lw=2, label = 'sim', zorder=1),  
    'sol': dict(lw=2, label = 'sol'),  
    'an': dict(lw=5, label = 'analytic', ls='--', zorder=0),  
    'fit': dict(lw=2, marker = 'o', label = 'fit')  
}

ylabel_map = {
    'var': r'$\sigma^2(t)$',
    'mean': r'$\langle \phi(t) \rangle$',
    'msd_r': r'MSD$\langle (\boldsymbol{r}(t)-\boldsymbol{r}_0)^2 \rangle$',
    'msd_phi': r'MSD$\langle (\phi(t)-\phi_0)^2 \rangle$'
}

import matplotlib.colors as mcolors
def lighten_color(color, amount=0.5):
    """
    Lightens the given color.
    amount=0 → no change, 
    amount=1 → white
    """
    try:
        c = mcolors.cnames[color]  # handle named colors
    except:
        c = color
    r, g, b = mcolors.to_rgb(c)
    return (1 - amount) + amount * r, (1 - amount) + amount * g, (1 - amount) + amount * b