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

colors_main_black = [
    "black",
    '#897bc1',
    "#b27236",
    "#AEA435",  
    "#FEBA27",  
    "#76B3D0",  
    "#F4BAEA",  
    "#FE6C23"   
]
cmap_black = ListedColormap(colors_main_black)

msd_style = {
    'sim': dict(lw=2, label = 'sim', zorder=2),  
    'sol': dict(lw=2, label = 'sol'),  
    'an': dict(lw=3.5, label = '', ls='-', zorder=3),  
    'an_a': dict(lw=2, label = '', ls='-', zorder=3, color = 'midnightblue'),  
    'an_tot': dict(lw=5, label = '', ls='-', zorder=2.5, color = colors_main_black[7]),  
    'an_tot_oversim': dict(lw=3, label = '', ls='-', zorder=2.5, color = colors_main_black[7]),  
    'fit': dict(lw=2, marker = 'o', label = 'fit')  
}

ylabel_map = {
    # 'var': r'$\sigma^2(t)$',
    'var': r'MSD$\langle (\phi(t)-\phi_0)^2 \rangle$',
    'mean': r'$\langle \phi(t) \rangle$',
    'msd_r': r'MSD$\langle (\mathbf{r}(t)-\mathbf{r}_0)^2 \rangle/L^2_{\alpha}$',
    'msd_phi': r'MSD$\langle (\phi(t)-\phi_0)^2 \rangle$'
}
