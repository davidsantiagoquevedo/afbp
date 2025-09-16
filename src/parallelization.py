import numpy as np
import multiprocessing as mp
from tqdm import tqdm
from world import Angular, xDirection, yDirection

def single_trajectory_helper(env, p, r, stored_matrix, lock):
    """
    Function that runs a single trajectory

    """
    env.make_B_H()
    if isinstance(env, Angular):
        if env.L_type == 'L1':         
            traj = env.run_one_L1()
        elif env.L_type == 'L2':
            traj = env.run_one_L2()
    else:
        traj = env.run_one(r)

    with lock:
        stored_matrix[p, :] = traj

def to_shared_array(array):
    shared_array = mp.Array('d', array.size, lock=False)
    temp = np.frombuffer(shared_array, dtype=array.dtype)
    temp[:] = array.flatten(order = "C")
    return shared_array

def to_numpy_array(shared_array, shape):
    array = np.ctypeslib.as_array(shared_array)
    return array.reshape(shape)

def run_trajectories_parallel(env, batch_size = 12):
    """
    Parallely runs independent Brownian trajectories.
    
    Parameters
    ----------
    env : env
        Environment class that defines the type of motion and paramteters
    batch_size : int 
        Number of nodes for paralell running 
    Returns
    -------
    """

    # Initialize matrix
    init_matrix = np.zeros((env.realizations, env.n), dtype = np.float64)  

    # Create multiprocessing array to which the different processes can access to. 
    # Thanks to temp, we can write a numpy array to a mp array and initialize it in this case.
    shared_matrix = to_shared_array(init_matrix)    #Returns initialized shared array

    # Create bridge to a nupy vector 
    stored_matrix = to_numpy_array(shared_matrix, init_matrix.shape)

    lock = mp.Lock()
    # execute in batches
    for r in tqdm(range(0, env.realizations, batch_size)):
        # execute all tasks in a batch
        processes = [mp.Process(target = single_trajectory_helper, 
                                args=(env, p, r, stored_matrix, lock)) for p in range(r, r + batch_size)]

        # start all processes
        for process in processes:
            process.start()
        # wait for all processes to complete
        for process in processes:
            process.join()

        env.trajectories = stored_matrix
        # env.make_B_H()
    
    return env