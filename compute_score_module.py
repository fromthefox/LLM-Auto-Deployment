"""
This module is used to calculate the score of each node based on the arithmetic, bandwidth and memory of the entire topology
"""
import numpy as np
from scipy.stats import entropy
import bandwidth_evaluation_module
import arithmetic_evaluation_module


def dynamic_weights(arithmetic_list, bandwidth_list, memory_list, base_weights = np.array([0.5, 0.4, 0.1]), dynamic_ratio = 0.7):
    # min-max normalization
    def minmax_scale(arr):
        arr = np.array(arr)
        return (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
    
    # kl-divergence calculation
    def kl_divergence(arr):
        uniform_dist = np.ones_like(arr)/len(arr)
        observed_dist = arr / arr.sum()
        return entropy(observed_dist, uniform_dist)

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

