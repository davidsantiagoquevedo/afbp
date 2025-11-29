legend_size = 13
axis_fontsize = 19
size_ticks = 20
marker_size = 10
title_fontsize = 15
size_labels_figures =17

# Main palette
import seaborn as sns
from matplotlib.colors import ListedColormap
colors_main = [
    "#AEA435",  
    "#FEBA27",  
    "#76B3D0",  
    "#F4BAEA",  
    "#FE6C23"   
]
color_analytic = "#57281E"
cmap = ListedColormap(colors_main)
palette = sns.color_palette([cmap(i) for i in range(cmap.N)])
sns.set_palette(palette)

msd_style = {
    'sim': dict(lw=4, label = 'sim', zorder=2),  
    'sol': dict(lw=2, label = 'sol'),  
    # 'an': dict(lw=4.5, label = '', ls='--', zorder=1),  
    'an': dict(lw=4, label = '', ls=':', zorder=3),  
    'fit': dict(lw=2, marker = 'o', label = 'fit')  
}

ylabel_map = {
    # 'var': r'$\sigma^2(t)$',
    'var': r'MSD$\langle (\phi(t)-\phi_0)^2 \rangle$',
    'mean': r'$\langle \phi(t) \rangle$',
    'msd_r': r'MSD$\langle (\mathbf{r}(t)-\mathbf{r}_0)^2 \rangle/L^2_{\alpha}$',
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

# Trajectories palettes

colors = [
    "#471800",  
    "#A23701",  
    "#FE5501",  
    "#FE925D",
    "#FEB18A"   
]
cmap_alpha01 = ListedColormap(colors)

colors = [
    "#651057",  
    "#B51C9B",  
    "#DD22BE",  
    "#E972D5",  
    "#F4BAEA"   
]
cmap_alpha03 = ListedColormap(colors)

colors = [
    "#5A551C",  
    "#7D7626",  
    "#AEA435",  
    "#CEC55F",  
    "#E3DEA5"   
]
cmap_alpha1 = ListedColormap(colors)

traj_style = {
    '0.1': dict(s=3, cmap = cmap_alpha01),
    '0.3': dict(s=3, cmap = cmap_alpha03),
    '1.0': dict(s=3, cmap = cmap_alpha1),
    '0.7': dict(s=3, cmap = cmap_alpha1)
}

colors01 = [
    "#471800",  
    "#A23701",  
    "#FE5501",  
    "#FE925D",
    "#FEB18A"   
]

colors03 = [
    "#651057",  
    "#B51C9B",  
    "#DD22BE",  
    "#E972D5",  
    "#F4BAEA"    
]

colors1 = [
    "#5A551C",  
    "#7D7626",  
    "#AEA435",  
    "#CEC55F",  
    "#E3DEA5"   
]

traj_colors = {
    '0.1': colors01,
    '0.3': colors03,
    '1.0': colors1
}

traj_colors_unique = {
    '0.1': colors_main[4],
    '0.3': colors_main[2],
    '1.0': colors_main[0]
}

colors_main_black = [
    "black",
    "#AEA435",  
    "#FEBA27",  
    "#76B3D0",  
    "#F4BAEA",  
    "#FE6C23"   
]
cmap_black = ListedColormap(colors_main_black)