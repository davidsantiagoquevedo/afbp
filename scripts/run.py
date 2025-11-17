import sys
sys.path.append("src/")
from world import *
import time
import parallelization
import argparse
import utilities
import warnings
warnings.filterwarnings("ignore") 

"""
Run example: nohup pyhton3 scripts/run.py --alphaT 1 0.5 0.3 --HT 0.5 0.75 0.85 --alphaR 1 0.5 0.3 --HR 0.5 0.75 0.85 --h 0.01
The parameters α and H are read element-wise: the first run with alphaT[0], HT[0], alphaR[0], HR[0]. Thus, they have to have the same number of elements!
The same list structure has to be used in the plotting modules.
"""

DATA_PATH = 'data_tests'

parser = argparse.ArgumentParser()
parser.add_argument("--L", type=str, default='L1', choices=["L1", "L2"], help="Which discretization type")
parser.add_argument("--folder", type=str, default='data_tests', help="Which output folder")
parser.add_argument("--modes", nargs='+', default=["phi"], choices=["phi", "x", "y", "r"], help="Which motion to simulate: phi, x, y, r"
)
parser.add_argument("--alphaR", nargs='+', type=float, default=[0.5], help="Rotational alpha value(s)")
parser.add_argument("--alphaT", nargs='+', type=float, default=[1], help="Translational alpha value")
parser.add_argument("--HR", nargs='+', type=float, default=[0.5], help="H value(s).")
parser.add_argument("--HT", nargs='+', type=float, default=[0.5], help="H value(s).")
parser.add_argument("--rule", type=str, default='N', help="Rule for evaluation of N(t)-N(t-1)")
parser.add_argument("--realizations", type=int, default=1000, help="Number of realizations")
parser.add_argument("--sets", type=int, default=1, help="Number of sets")
parser.add_argument("--Tf", type=float, default=10, help="Final time Tf")
parser.add_argument("--h", type=float, default=0.05, help="Step size h")
parser.add_argument("--ups", type=float, default=1, help="Self propulsion velocity")
parser.add_argument("--batch_size", type=int, default=10, help="Batch size for paralellization")
parser.add_argument("--start_set", type=int, default=1, help="first index of set label")

args = parser.parse_args()

start_time = time.time()

L_type = args.L
folder = args.folder

alphaRs = args.alphaR
HRs = args.HR

alphaTs = args.alphaT
HTs = args.HT

ups = args.ups
rule = args.rule
realizations, sets, Tf, h, ups, batch_size = args.realizations, args.sets, args.Tf, args.h, args.ups, args.batch_size
start_set = args.start_set


for i in range(len(alphaRs)):

    alphaT = alphaTs[i]
    alphaR = alphaRs[i]

    HT = HTs[i]
    HR = HRs[i]

    for set_index in range(start_set, start_set+sets):
        print(f"-- Running set {set_index}")
        set_label = str(set_index).zfill(3)
        # try:
        #     phi = utilities.read_env(L_type, 'phi', alphaR, HR, realizations, Tf, hR, start_set= start_set, sets=sets, path=DATA_PATH)
        #     print(f"-- Loaded phi")
        # except:
        print(f"-- Running phi alphaR={alphaR}, HR={HR}")
        phi = Angular(realizations=realizations, alpha=alphaR, H=HR, Tf=Tf, h=h, L_type=L_type)
        # phi.run()
        phi.run_numba()
        # phi = parallelization.run_trajectories_parallel(phi, batch_size=batch_size)
        phi.save(set_label= set_label, folder=folder)

        if "x" in args.modes:

            # try:
            #     x = utilities.read_env(L_type, 'x', alphaT, HT, realizations, Tf, h, start_set=set_index, sets=1, path=DATA_PATH, alphaR=alphaR, HR=HR, ups=ups, AHT=AHT, rule=rule, hR=hR)
            #     print(f"-- Loaded x")
            #     x.rule = rule
            # except:
            print(f"-- Running x alphaT={alphaT}, HT={HT}")
            x = xDirection(phi=phi, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h, ups=ups, L_type=L_type)
            # x.run()
            x = parallelization.run_trajectories_parallel(x, batch_size)
            x.save(set_label= set_label, folder=folder, mode='x')
    
        if "y" in args.modes:

            # try:
            # y = utilities.read_env(L_type, 'y', alphaT, HT, realizations, Tf, h, start_set=set_index, sets=1, path=DATA_PATH, alphaR=alphaR, HR=HR, ups=ups, AHT=AHT, rule=rule, hR=hR)
            # print(f"-- Loaded y")
            # y.rule = rule
            # except:
            # print(f"-- Running y alphaT={alphaT}, HT={HT}")
            y = yDirection(phi=phi, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h, ups=ups, L_type=L_type)
            # y.run()
            y = parallelization.run_trajectories_parallel(y, batch_size)
            y.save(set_label= set_label, folder=folder, mode='y')
        
        if "r" in args.modes:
            print(f"-- Running r")
            
            r = rModulus(x=x, y=y, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h, L_type=L_type)
            r.compute_r_modulus()
            r.save(set_label= set_label, folder=folder, mode='r')


elapsed_time = time.time() - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
