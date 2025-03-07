"""
本模块用于根据整个拓扑的算力、带宽、内存等因素来对各个节点进行得分计算
"""

def compute_score(arithmetic_list, bandwidth_list, memory_list):
    w1, w2, w3 = 0.4, 0.3, 0.3

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


