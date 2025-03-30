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


def proportinal_allocation(scores_list:list, model_unsplitted_dim:int) -> list:
    """
    this func is used to allocate the conculation tast of the inference according to the scores_list.
    :param scores_list: the list of the scores, which is used to allocate the calculation task.
    :param model_unsplitted_dim: the total number wait for splitting.
    :return: the list of the allocation result.
    """
    if not scores_list:
        raise ValueError("scores_list cannot be empty")
    
    if model_unsplitted_dim < 0:
        raise ValueError("model_unsplitted_dim must > 0")
    
    scores = [float(s) for s in scores_list]

    total_weight = sum(scores)

    # Calculation of the theoretical assigned value
    exact_allocations = [model_unsplitted_dim * (s / total_weight) for s in scores]

    integer_parts = [int(a) for a in exact_allocations]
    fractional_parts = [a - int(a) for a in exact_allocations]

    # Calculate the remaining number to be allocated
    total_allocated = sum(integer_parts)
    remaining = model_unsplitted_dim - total_allocated

    if remaining < 0:
        raise RuntimeError("Algorithm error: allocation value exceeds total")
    
    if remaining > 0:
        # Sort indices in descending order by fractional part
        # 从两个维度的降序排列：1. 小数部分从大到小；2. 得分从大到小
        sorted_indices = sorted(
            range(len(fractional_parts)),
            key=lambda i: (-fractional_parts[i], -scores[i])
        )
        
        # Allocate the remaining quantity
        for i in sorted_indices[:remaining]:
            integer_parts[i] += 1
    
    return integer_parts
