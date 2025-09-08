import sys
sys.path.append("src/")
from world import *
import time
import parallelization
import argparse
import utilities
import warnings
warnings.filterwarnings("ignore") 

parser = argparse.ArgumentParser()
parser.add_argument("--modes", nargs='+', default=["phi"], choices=["phi", "x", "y", "r"], help="Which motion to simulate: phi, x, y, r"
)
parser.add_argument("--alphaR", nargs='+', type=float, default=[0.5], help="Rotational alpha value(s)")
parser.add_argument("--alphaT", type=float, default=1, help="Translational alpha value")
parser.add_argument("--HR", nargs='+', type=float, default=[0.5], help="H value(s). Required if alpha=1.")
parser.add_argument("--AHT", type=float, default=1, help="Translational noise coefficient")
parser.add_argument("--realizations", type=int, default=1000, help="Number of realizations")
parser.add_argument("--sets", type=int, default=1, help="Number of sets")
parser.add_argument("--Tf", type=float, default=10, help="Final time Tf")
parser.add_argument("--h", type=float, default=0.05, help="Step size h")
parser.add_argument("--nu", type=float, default=1, help="Self propulsion velocity")
parser.add_argument("--batch_size", type=int, default=10, help="Batch size for paralellization")
parser.add_argument("--start_set", type=int, default=1, help="first index of set label")

args = parser.parse_args()

start_time = time.time()

alphaRs = args.alphaR
HRs = args.HR

alphaT = args.alphaT
nu = args.nu
AHT = args.AHT

realizations, sets, Tf, h, nu, batch_size = args.realizations, args.sets, args.Tf, args.h, args.nu, args.batch_size
start_set = args.start_set

HT = (2 - alphaT) / 2

for alphaR in alphaRs:

    for HR in HRs:
        print(f"---- Running for alphaT={alphaT}, alphaR={alphaR}, HR={HR}")
        for set_index in range(start_set, start_set+sets):
            print(f"-- Running set {set_index}")
            set_label = str(set_index).zfill(3)
            try:
                phi = utilities.read_env('phi', alphaR, HR, realizations, Tf, h, start_set=set_index, sets=1)
                print(f"-- Loaded phi")
            except:
                print(f"-- Running phi")
                phi = Angular(realizations=realizations, alpha=alphaR, H=HR, Tf=Tf, h=h)
                # phi.run()
                phi = parallelization.run_trajectories_parallel(phi, batch_size=batch_size)
                phi.save(set_label= set_label, folder="data")

            if "x" in args.modes:

                try:
                    x = utilities.read_env('x', alphaT, HT, realizations, Tf, h, start_set=set_index, sets=1, alphaR=alphaR, HR=HR, nu=nu, AHT=AHT)
                    print(f"-- Loaded x")
                except:
                    print(f"-- Running x")
                    x = xDirection(phi=phi, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h, nu=nu, AHT=AHT)
                    # x.run()
                    x = parallelization.run_trajectories_parallel(x, batch_size)
                    x.save(set_label= set_label, folder="data", mode='x')
                
            if "y" in args.modes:

                try:
                    y = utilities.read_env('y', alphaT, HT, realizations, Tf, h, start_set=set_index, sets=1, alphaR=alphaR, HR=HR, nu=nu, AHT=AHT)
                    print(f"-- Loaded y")
                except:
                    print(f"-- Running y")
                    y = yDirection(phi=phi, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h, nu=nu, AHT=AHT)
                    # y.run()
                    y = parallelization.run_trajectories_parallel(y, batch_size)
                    y.save(set_label= set_label, folder="data", mode='y')
                
            if "r" in args.modes:
                print(f"-- Running r")
                
                r = rModulus(x=x, y=y, realizations=realizations, alpha=alphaT, H=HT, Tf=Tf, h=h)
                r.compute_r_modulus()
                r.save(set_label= set_label, folder="data", mode='r')


elapsed_time = time.time() - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
