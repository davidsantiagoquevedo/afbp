from world import Base
import numpy as np

def read_env(mode, alpha, H, realizations, Tf, h, start_set, sets, alphaR=None, HR=None, nu=None):
    
    if mode == 'phi':
        alphaH = f"alphaR{alpha}_HR{H}"
    else:
        alphaH = f"alphaT{alpha}_HT{H}_alphaR{alphaR}_HR{HR}_nu{nu}"

    for set_index in range(start_set, start_set+sets):
        set_label = str(set_index).zfill(3)
        
        env = Base(realizations=realizations, alpha=alpha, H=H, Tf=Tf, h=h)
        
        filepath = (
            f"data/{mode}_"
            f"{alphaH}_"
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
