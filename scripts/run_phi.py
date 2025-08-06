import sys
sys.path.append("src/")
from world import *
import time
import parallelization
import argparse

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("--alpha", nargs='+', type=float, default=0.5, help="Alpha value")
parser.add_argument("--sets", type=int, default=5, help="Number of sets")
parser.add_argument("--realizations", type=int, default=1200, help="Number of realizations")
parser.add_argument("--Tf", type=float, default=10, help="Tf value")
parser.add_argument("--h", type=float, default=0.05, help="h value")
args = parser.parse_args()

start_time = time.time()

alphas = args.alpha
sets = args.sets
realizations = args.realizations
Tf = args.Tf
h = args.h

envs=[]
for alpha in alphas:    
        
    print("----Running for alpha", alpha)

    H = (2-alpha)/2
    for set_index in range(sets):

        print("--Running for set", set_index)
        set_label = str(set_index+1).zfill(3)
        set_index += 1
        env = angular_fbm(realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
        
        env.phi_matrix = parallelization.run_trajectories_parallel(env, batch_size=30)
        env.run_solution()
        
        env.save(folder="data")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
