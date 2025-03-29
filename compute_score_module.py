"""
This module is used to calculate the score of each node based on the arithmetic, bandwidth and memory of the entire topology
"""
import numpy as np
from scipy.stats import entropy
from function_modules import minmax_scale, kl_divergence


def dynamic_weights(nodes_info_dict, base_weights = np.array([0.5, 0.4, 0.1]), dynamic_ratio = 0.7):

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


def total_score(nodes_info_dict, dynamic_weights, task_demand):
    """
    this func is used to compute the score of each node baseed on weights.
    """
    arithmetic_list, bandwidth_list, memory_list = nodes_info_dict["arithmetic"], nodes_info_dict["bandwidth"], nodes_info_dict["memory"]
    
    # mem_mask = memory_filter(memory, task_demand["memory"])
    # Memory Hard Filtering


    norm_arith = minmax_scale(arithmetic_list)
    norm_bw = minmax_scale(bandwidth_list)
    norm_mem = minmax_scale(memory_list)

    weights = np.array(dynamic_weights)
    weights = weights / (weights.sum() + 1e-8)

    scores = []
    for i in range(len(arithmetic_list)):
        # Weighted geometric mean with smoothing
        geo_mean = (
            (norm_arith[i] + 1e-8) ** weights[0] * 
            (norm_bw[i] + 1e-8) ** weights[1] * 
            (norm_mem[i] + 1e-8) ** weights[2]
        )
        # 应用适应性调整
        final_score = geo_mean * suit_factors * latency_penalties
        scores.append(final_score)
