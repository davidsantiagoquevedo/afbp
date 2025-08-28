from world import Base
import numpy as np

def read_env(mode, alpha, H, realizations, Tf, h, sets):

    for set_index in range(sets):
        set_label = str(set_index+1).zfill(3)
        set_index += 1
        
        env = Base(realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
        
        filepath = (
            f"data/{mode}_"
            f"alpha{alpha}_"
            f"H{H}_"
            f"r{realizations}_"
            f"Tf{Tf}_"
            f"h{h}_" 
            f"set{set_label}.pkl"
        )

        env = Base.load(filepath)
        
        if set_index==1:
            env_multiset = env
        else:
            env_multiset.realizations += realizations
            env_multiset.trajectories = np.vstack((env_multiset.trajectories, env.trajectories))

    return env_multiset
