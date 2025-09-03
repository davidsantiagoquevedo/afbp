import sys
sys.path.append("src/")
from world import *
import time
import parallelization
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--modes", nargs='+', default=["phi"], choices=["phi", "x", "y", "r"], help="Which motion to simulate: phi, x, y, r"
)
parser.add_argument("--alpha", nargs='+', type=float, default=[0.5], help="Alpha value(s)")
parser.add_argument("--H", nargs='+', type=float, default=[0.5], help="H value(s). Required if alpha=1.")
parser.add_argument("--realizations", type=int, default=1000, help="Number of realizations")
parser.add_argument("--sets", type=int, default=1, help="Number of sets")
parser.add_argument("--Tf", type=float, default=10, help="Final time Tf")
parser.add_argument("--h", type=float, default=0.05, help="Step size h")
parser.add_argument("--eta", type=float, default=1, help="Self propulsion velocity")
parser.add_argument("--batch_size", type=int, default=10, help="Batch size for paralellization")

args = parser.parse_args()

start_time = time.time()

alphas = args.alpha
Hs = args.H
realizations, sets, Tf, h, eta, batch_size = args.realizations, args.sets, args.Tf, args.h, args.eta, args.batch_size

envs = []
for alpha in alphas:
    # alpha == 1 : use provided H values
    # if alpha == 1:
    #     if Hs is None:
    #         raise ValueError("You must provide --H when alpha=1")
    #     H_values = Hs
    # # alpha != 1 : compute H automatically
    # else:
    #     H_values = [(2 - alpha) / 2]

    for H in Hs:
        print(f"---- Running for alpha={alpha}, H={H}")
        for set_index in range(1, sets+1):
            print(f"-- Running set {set_index}")
            set_label = str(set_index).zfill(3)

            # if "phi" in args.modes:
            phi = Angular(realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
            # phi.run()
            phi = parallelization.run_trajectories_parallel(phi, batch_size=batch_size)
            #phi.run_solution()
            phi.save(folder="data")

            if "x" in args.modes:
                x = xDirection(phi_trajectories=phi.trajectories, realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h, eta=eta)
                x.run()
                # x = parallelization.run_trajectories_parallel(x, batch_size=10)
                # x.run_solution()
                x.save(folder="data", mode='x')


elapsed_time = time.time() - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
