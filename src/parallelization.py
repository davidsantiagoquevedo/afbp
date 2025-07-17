import numpy as np
import multiprocessing as mp

def to_shared_array(array):
    shared_array = mp.Array('d', array.size, lock=False)
    temp = np.frombuffer(shared_array, dtype=array.dtype)
    temp[:] = array.flatten(order = "C")
    return shared_array

def to_numpy_array(shared_array, shape):
    array = np.ctypeslib.as_array(shared_array)
    return array.reshape(shape)

def  run_parallel(env):
    """
    Parallely runs independent Brownian trajectories.
    
    Parameters
    ----------
    env : env
        Environment class that defines the type of motion and paramteters
    compute_single_trajectory : func
        Function that runs a single trajectory

    Returns
    -------
    """
        
    batch_size = 10

    # Initialize matrix
    init_matrix = np.zeros((env.n, env.realizations), dtype = np.float64)  

    # Create multiprocessing array to which the different processes can access to. 
    # Thanks to temp, we can write a numpy array to a mp array and initialize it in this case.
    shared_matrix = to_shared_array(init_matrix)    #Returns initialized shared array

    # Create bridge to a nupy vector 
    stored_matrix = to_numpy_array(shared_matrix, init_matrix.shape)

    lock = mp.Lock()
    # execute in batches
    for r in range(0, env.realizations, batch_size):
        # execute all tasks in a batch
        processes = [mp.Process(target = env.trajectory, 
                                args=(env, p, stored_matrix, lock)) for p in range(r, r + batch_size)]

        # start all processes
        for process in processes:
            process.start()
        # wait for all processes to complete
        for process in processes:
            process.join()