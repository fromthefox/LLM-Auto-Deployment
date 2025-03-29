"""
some modules to use
"""
import numpy as np
from scipy.stats import entropy

def dict2list(nodes_info_dict:dict, network_matrix:list, central_node_index:int) -> dict:
    """
    the nodes_info_dict here is same as the format initializaed in the initial_topo.py file.
    same with network matrix.
    convert the topo dict info to list info.
    this is a format converter, convert the initial topo format into the format we need to compute the node score.
    """
    network_list = network_matrix[central_node_index]
    _ = network_list.pop(central_node_index) # remove the central node from the network list.
    nodes_arithmetic_list = []
    nodes_memory_list = []
    for i in range(len(network_list)):
        nodes_arithmetic_list.append(nodes_info_dict[i]["arithmetic"])
        nodes_memory_list.append(nodes_info_dict[i]["memory"])
    
    res_dict = {
        "arithmetic": nodes_arithmetic_list,
        "memory": nodes_memory_list,
        "bandwidth": network_list
    }

    return res_dict


# min-max normalization
def minmax_scale(arr):
    arr = np.array(arr)
    return (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)


# kl-divergence calculation
def kl_divergence(arr):
    uniform_dist = np.ones_like(arr)/len(arr)
    observed_dist = arr / arr.sum()
    return entropy(observed_dist, uniform_dist)

# robust normalization
def robust_normalize(arr):
    q10 = np.percentile(arr, 10)
    q90 = np.percentile(arr, 90)
    return (arr - q10) / (q90 - q10 + 1e-8)