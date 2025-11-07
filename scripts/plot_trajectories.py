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
h=0.01
realizations = 10
start_set=1
sets=1
L_type = 'L1'
AHT=1.
alphaT = 0.1
HT = 0.95
alphaR = alphaT
HR = HT
ups=1.
rule='N'

x = utilities.read_env(mode='x',
                        L_type = L_type, 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        ups=ups,
                        AHT=AHT,
                        realizations=realizations,
                        Tf=Tf,
                        h=h, hR=h,
                        start_set=start_set,
                        sets=sets,
                        rule=rule,
                        path=DATA_PATH)
y = utilities.read_env(mode='y',
                        L_type = L_type, 
                        alpha=alphaT, H=HT,
                        alphaR=alphaR, HR=HR,
                        ups=ups,
                        AHT=AHT,
                        realizations=realizations,
                        Tf=Tf,
                        h=h, hR=h,
                        start_set=start_set,
                        sets=sets,
                        rule=rule,
                        path=DATA_PATH)


for j in range(10):

    fig, ax = plt.subplots()
    x_val = x.trajectories[j,:]
    y_val = y.trajectories[j,:]

    # x=x[::30]
    # y=y[::30]

    k=10
    n=len(x_val)
    x_val = np.interp(np.arange(n * k), np.arange(n) * k, x_val)
    y_val = np.interp(np.arange(n * k), np.arange(n) * k, y_val)
    t = np.linspace(0, 100, len(x_val))

    sc = ax.scatter(x_val, y_val, s=3, c=t,  cmap=colormaps['summer'])

    fig.colorbar(sc, ax=ax, label='t')

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