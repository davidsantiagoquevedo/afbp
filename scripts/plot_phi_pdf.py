import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

mode = 'phi'
L_type = 'L1'
realizations = 1000
Tf = 10
h = 0.05
start_set = 1
sets = 5

alphaRs = [1., 1., 1.] 
HRs = [0.8, 0.5, 0.2]  

for i, alphaR in enumerate(alphaRs):

    HR = HRs[i]

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets)

    # Plot PDF
    fig_pdf, ax_pdf = plt.subplots(figsize=(8, 7))
    for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
        plotting.plot_pdf(ax_pdf, env, mode, time=t)
    fig_pdf.tight_layout()
    fig_pdf.savefig(f"plots/pdf/{L_type}_{mode}pdf_alphaR{alphaR}_H{HR}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)

