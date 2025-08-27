from world import Base
import numpy as np

def read_env(mode, alpha, H, sets, Tf, h, realizations):

    for set_index in range(sets):
        set_label = str(set_index+1).zfill(3)
        set_index += 1
        
        env = Base(realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
        
        filepath = (
            f"data/{mode}_r{env.realizations}_"
            f"alpha{env.alpha}_"
            f"H{env.H}_"
            f"Tf{env.Tf}_"
            f"h{env.h}_"
            f"set{set_label}.pkl"
        )

        env = Base.load(filepath)
        
        if set_index==1:
            env_multiset = env
        else:
            env_multiset.realizations += realizations
            env_multiset.trajectories = np.vstack((env_multiset.trajectories, env.trajectories))

    return env_multiset
