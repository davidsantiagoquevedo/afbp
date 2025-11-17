from world import Base
import numpy as np
import os 
import shutil

def read_env(L_type, mode, alpha, H, realizations, Tf, h, start_set, sets, path, alphaR=None, HR=None, ups=None):
    
    if mode == 'phi':
        alphaH = f"alphaR{alpha}_HR{H}"
    else:

        alphaH = f"alphaT{alpha}_HT{H}_alphaR{alphaR}_HR{HR}_ups{ups}"


    for set_index in range(start_set, start_set+sets):
        set_label = str(set_index).zfill(3)
        
        env = Base(realizations=realizations, alpha=alpha, H=H, Tf=Tf, h=h, L_type=L_type)
        
        filepath = (
            f"{path}/{L_type}_{mode}_"
            f"{alphaH}_"
            f"r{realizations}_"
            f"Tf{Tf}_"
            f"h{h}_" 
            f"set{set_label}_AHfdt.pkl"
        )
        env = Base.load(filepath)

        # # Define the destination folder
        # destination_folder = "data/"

        # # Ensure the destination folder exists
        # os.makedirs(destination_folder, exist_ok=True)

        # # Build the new full path for the file
        # destination_path = os.path.join(destination_folder, os.path.basename(filepath))

        # # Move the file
        # shutil.move(filepath, destination_path)

        
        if set_index==start_set:
            env_multiset = env
        else:

            env_multiset.realizations += realizations
            env_multiset.trajectories = np.vstack((env_multiset.trajectories, env.trajectories))

    return env_multiset
