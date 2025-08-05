import sys
sys.path.append("src/")
from world import *
import time
import parallelization

start_time = time.time()

# alphas = [0.1, 0.3, 0.5, 0.7, 0.9, 1]
alphas = [0.5]#0.3, 0.5, 0.7, 1]
# H = 0.1
realizations = 1200
sets = 15
# set_index = "010"
Tf = 10
h = 0.05
envs=[]


for alpha in alphas:    
        
    print("----Running for alpha", env.alpha)

    H = (2-alpha)/2
    for set_index in range(sets):

        print("--Running for set", set_index)
        set_label = str(set_index+1).zfill(3)
        set_index += 1
        env = angular_fbm(realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
        
        env.phi_matrix = parallelization.run_trajectories_parallel(env, batch_size=12)
        env.run_solution()
        
        env.save(folder="data")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
