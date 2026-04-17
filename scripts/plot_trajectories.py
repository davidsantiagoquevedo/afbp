import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting as plot
import plotting_param as par
import utilities
from matplotlib import colormaps
from mpl_toolkits.mplot3d import Axes3D

DATA_PATH = 'data_tests'
mode = 'r'
Tf = 100.
h=0.005
realizations = 10
start_set=1
sets=1
L_type = 'L1'
alphaT = 0.5
HT = 0.75
alphaR = alphaT
HR = HT
ups=20.

x = utilities.read_env(mode='x',
                        L_type = 'L1', 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        ups=ups,
                        realizations=realizations,
                        Tf=Tf,
                        h=h, 
                        start_set=start_set,
                        sets=sets,
                        path=DATA_PATH)
y = utilities.read_env(mode='y',
                        L_type = 'L1', 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        ups=ups,
                        realizations=realizations,
                        Tf=Tf,
                        h=h, 
                        start_set=start_set,
                        sets=sets,
                        path=DATA_PATH)


for j in range(10):
    
    x_val = x.trajectories[j,:]
    y_val = y.trajectories[j,:]

    fig, ax = plt.subplots()
    
    plot.plot_trajectory(ax,  x_val, y_val, 10, 10, fig=fig)

    # fig.tight_layout()
    fig.savefig(f"plots/trajectories/alphaT{alphaT}/h{h}/traj_alphaT{alphaT}_HT{HT}_r{j}_Tf{Tf}_h{h}_ups{ups}.png", dpi=100)


# 3D
# import plotly.graph_objects as go

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# fig = go.Figure(data=[go.Scatter3d(
#     x=x, y=y, z=t,
#     mode='lines+markers',
#     marker=dict(
#         size=3,
#         color=t,
#         colorscale='Greens',   # 'Greens' ≈ Matplotlib's 'summer'
#         colorbar=dict(title='Time progression')
#     ),
#     line=dict(color='gray', width=1)
# )])

# # Layout and axis labels
# fig.update_layout(
#     scene=dict(
#         xaxis_title='x',
#         yaxis_title='y',
#         zaxis_title='Time',
#         aspectmode='auto'
#     ),
#     title=f"3D Trajectory (j={j}) — Time as z-axis",
#     template='plotly_white'
# )

# fig.show()