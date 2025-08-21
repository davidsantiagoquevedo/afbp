from world import angular_fbm
import numpy as np

def read_envs(alphas, sets, Tf, h, realizations, Hs=None):
    envs=[]
    for alpha in alphas:    
        
        if Hs is None:
            Hs = (2-alpha)/2
        
        for H in Hs:
            
            for set_index in range(sets):
                set_label = str(set_index+1).zfill(3)
                set_index += 1
                
                env = angular_fbm(realizations=realizations, set_index=set_label, alpha=alpha, H=H, Tf=Tf, h=h)
                
                filepath = (
                    f"data/r_{env.realizations}_"
                    f"alpha_{env.alpha}_"
                    f"H_{env.H}_"
                    f"Tf_{env.Tf}_"
                    f"h_{env.h}_"
                    f"set_{set_label}.pkl"
                )
                env = angular_fbm.load(filepath)
                
                if set_index==1:
                    env_multiset = env
                else:
                    env_multiset.realizations += realizations
                    env_multiset.phi_matrix = np.vstack((env_multiset.phi_matrix, env.phi_matrix))
                
            env_multiset.compute_phi_correlation()
            env_multiset.compute_mean()
            env_multiset.compute_variance()
                
            envs.append(env_multiset)
    return envs