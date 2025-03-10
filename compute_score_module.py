"""
This module is used to calculate the score of each node based on the arithmetic, bandwidth and memory of the entire topology
"""
import numpy as np
from scipy.stats import entropy
import bandwidth_evaluation_module
import arithmetic_evaluation_module

def compute_score(weights, arithmetic_list, bandwidth_list, memory_list):
    w1, w2, w3 = weights[0], weights[1], weights[2]

    max_arithmetic = max(arithmetic_list)
    max_bandwidth = max(bandwidth_list)
    max_memory = max(memory_list)

    score_list = []

    for i in range(len(arithmetic_list)):
        normalized_arithmetic = arithmetic_list[i]/max_arithmetic
        normalized_bandwidth = bandwidth_list[i]/max_bandwidth
        normalized_memory = memory_list[i]/max_memory
        score = w1 * normalized_arithmetic + w2 * normalized_bandwidth + w3 * normalized_memory
        score_list.append(score)
    return score_list


def dynamic_weights(arithmetic_list, bandwidth_list, memory_list):
    # min-max normalization
    def minmax_scale(arr):
        arr = np.array(arr)
        return (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
    
    # calculate norm_res
    norm_arith = minmax_scale(arithmetic_list)
    norm_bw = minmax_scale(bandwidth_list)
    norm_mem = minmax_scale(memory_list)
    
    # def KL-entropy
    def kl_divergence(arr):
        uniform_dist = np.ones_like(arr)/len(arr)
        observed_dist = arr / arr.sum()
        return entropy(observed_dist, uniform_dist)
    
    # calculate KL-entropy
    entropy_arith = kl_divergence(norm_arith)
    entropy_bw = kl_divergence(norm_bw)
    entropy_mem = kl_divergence(norm_mem)
    total_entropy = entropy_arith + entropy_bw + entropy_mem
    
    # base weights: Ensure hard weighting of memory
    base_weights = np.array([0.3, 0.3, 0.4])  # [arithmetic, bd, memory]
    
    # dynamic adapt
    dynamic_part = np.array([
        entropy_arith/(total_entropy+1e-8),
        entropy_bw/(total_entropy+1e-8),
        entropy_mem/(total_entropy+1e-8)
    ])
    
    # Composite weighting calculation
    final_weights = 0.3 * base_weights + 0.7 * dynamic_part
    return final_weights / final_weights.sum()


def evaluate_bandwidth(candidate, all_nodes):
    """
    From here we get two metrics, shortboard bandwidth and bandwidth equalisation
    """
    bw_list = [bandwidth_evaluation_module.get_bw(node, candidate) for node in all_nodes if node != candidate]
    # bw_list is a symmetric matrix (math.)
    min_bw = min(bw_list)
    avg_bw = np.mean(bw_list)
    max_bw = max(bw_list)
    uniformity = 1 - (max_bw - min_bw)/avg_bw
    # A high degree of equilibrium indicates that the bandwidth from all nodes to the central node is in the approximation interval
    return {
        'min_bw': min_bw,
        # min_bw stands for short board effect
        'uniformity': max(uniformity, 0.1)
    }

def compute_suitability(compute_power):
    """
    Computational power fitness (Sigmoid suppression over/under)
    """
    k = 0.1
    threshold = 50
    return 1 / (1 + np.exp(k * (compute_power - threshold)))

def total_score(candidate, all_nodes):
    bw = evaluate_bandwidth(candidate, all_nodes)
    compute = arithmetic_evaluation_module.get_compute_power(candidate)
    suit = compute_suitability(compute)
    return np.log(bw['min_bw'] + 1e-8) * bw['uniformity'] * suit