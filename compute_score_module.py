"""
This module is used to calculate the score of each node based on the arithmetic, bandwidth and memory of the entire topology
"""
import numpy as np
from scipy.stats import entropy
from function_modules import minmax_scale, kl_divergence, robust_normalize


def dynamic_weights(nodes_info_dict, base_weights = np.array([0.5, 0.4, 0.1]), dynamic_ratio = 0.7):
    """
    func: compute the dynamic weight accrodding to the list of three dimensions.
    input: nodes info dict, including arithmetic, bandwidth and memory.
    output: the dynamic weights of the three dimensions.
    """
    arithmetic_list, bandwidth_list, memory_list = nodes_info_dict["arithmetic"], nodes_info_dict["bandwidth"], nodes_info_dict["memory"]

    # calculate norm_res
    norm_arith = minmax_scale(arithmetic_list)
    norm_bw = minmax_scale(bandwidth_list)
    norm_mem = minmax_scale(memory_list)
    
    # calculate KL-entropy
    entropy_arith = kl_divergence(norm_arith)
    entropy_bw = kl_divergence(norm_bw)
    entropy_mem = kl_divergence(norm_mem)
    total_entropy = entropy_arith + entropy_bw + entropy_mem
    
    # base weights: Ensure hard weighting of memory
    # [arithmetic, bd, memory]
    
    # dynamic adapt
    # normalization
    dynamic_part = np.array([
        entropy_arith/(total_entropy+1e-8),
        entropy_bw/(total_entropy+1e-8),
        entropy_mem/(total_entropy+1e-8)
    ])
    
    # Composite weighting calculation
    final_weights = (1-dynamic_ratio) * base_weights + dynamic_ratio * dynamic_part
    return final_weights / final_weights.sum()


"""
the three func. below are used to suit the weights. 
For future used.
"""
def compute_suitability(compute_power):
    """
    Computational power fitness (Sigmoid suppression over/under)
    """
    k = 0.1
    threshold = np.median(compute_power)
    return 1 / (1 + np.exp(k * (compute_power - threshold)))

def latency_penalty(latency_list):
    """
    Exponential penalty for nodes with higher than average latency
    """
    avg_latency = np.mean(latency_list)
    return np.exp(-0.1 * (latency_list - avg_latency))

def memory_filter(memory_list, min_required=16):
    """
    filter the nodes based on memory requirement.
    but not now, this is a placeholder for future use.
    """
    pass


def total_score(nodes_info_dict:dict, dynamic_weights:np.ndarray)->list:
    """
    func: compute the total score of the nodes based on 3 dimensions
    input: nodes_info_dict, including arithmetic, bandwidth and memory
    output: the list including the score of each node
    """
    # 1. Get the necessary information
    arithmetic_list, bandwidth_list, memory_list = nodes_info_dict["arithmetic"], nodes_info_dict["bandwidth"], nodes_info_dict["memory"]
    
    # mem_mask = memory_filter(memory, task_demand["memory"])
    # Memory Hard Filtering


    norm_arith = robust_normalize(arithmetic_list)
    norm_bw = robust_normalize(bandwidth_list)
    norm_mem = robust_normalize(memory_list)

    weights = np.array(dynamic_weights)
    weights = weights / (weights.sum() + 1e-8)

    hybrid_scores = []
    for a, b, m in zip(norm_arith, norm_bw, norm_mem):
        # Arithmetic weighted guarantee basis values
        base_score = np.dot([a, b, m], weights)
        
        # Geometric weighting improves equilibrium
        geo_score = (a**weights[0]) * (b**weights[1]) * (m**weights[2])
        
        # Harmonize the advantages of both
        hybrid = 0.7 * geo_score + 0.3 * base_score
        hybrid_scores.append(hybrid)
    
    final_scores = (final_scores - final_scores.min()) / (final_scores.max() - final_scores.min() + 1e-8)

    return hybrid_scores