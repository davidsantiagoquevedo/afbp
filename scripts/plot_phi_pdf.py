import sys
sys.path.append("src/")
from world import *
import matplotlib.pyplot as plt
import plotting
import utilities

data_path = 'data'
out_path = 'tests'#'var'
mode = 'phi'
L_type = 'L2'
realizations = 160
Tf = 10
h = 0.0005
start_set = 1
sets = 10
m=1e-9
eta=1

def tl(alpha, H, eta=1, m=0.00000001):
    return ((m*H*gamma(2*H))/(eta*(alpha+H-1)*gamma(alpha)*gamma(alpha+2*H-1)))**(1/(4-2*alpha-2*H))

alphaRs = [0.3]#, 0.5, 0.5]
HRs = [0.75]#, 0.75, 0.85]
#alphaRs = [0.7, 0.7, 0.7]
#HRs = [0.55, 0.65, 0.75]
for i, alphaR in enumerate(alphaRs):

    HR = HRs[i]

    env = utilities.read_env(L_type, mode, alphaR, HR, realizations, Tf, h, start_set= start_set, sets=sets, path=data_path)
    tl_value = tl(alpha=alphaR, H=HR, eta=eta, m=m)
    # Plot PDF
    fig_pdf, ax_pdf = plt.subplots(figsize=(8, 7))
    for t in [int(Tf/(4*h)), int(Tf/(2*h)), int((Tf/h)-1)]:
        plotting.plot_pdf(ax_pdf, env, mode, time=t, tl = tl_value)
    fig_pdf.tight_layout()
    fig_pdf.savefig(f"plots/{out_path}/{L_type}_{mode}pdf_alphaR{alphaR}_H{HR}_r{realizations*sets}_Tf{Tf}_h{h}.png", dpi=100)

