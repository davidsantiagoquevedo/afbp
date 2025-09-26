import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

data_path = 'data_tests'
out_path = 'tests'#'var'
mode = 'phi'
L_type = 'L1'
realizations = 1500
Tf = 10
h = 0.001
start_set = 1
sets = 3

alphaRs = [0.5]#, 0.5, 0.5]
HRs = [0.65]#, 0.75, 0.85]
#alphaRs = [0.7, 0.7, 0.7]
#HRs = [0.55, 0.65, 0.75]
for i, alphaR in enumerate(alphaRs):

    HR = HRs[i]

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path=data_path)

    # Plot PDF
    fig_pdf, ax_pdf = plt.subplots(figsize=(8, 7))
    for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
        plotting.plot_pdf(ax_pdf, env, mode, time=t)
    fig_pdf.tight_layout()
    fig_pdf.savefig(f"plots/{out_path}/{L_type}_{mode}pdf_alphaR{alphaR}_H{HR}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)

