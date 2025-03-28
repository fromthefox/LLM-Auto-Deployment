"""
This initialisation module is used to select the locally optimal central node in the unselected phase of the central node
"""
"""
对W也进行切分，作为分布式的一部分，那么中心节点几乎就没有计算量了。
因此中心节点只需要考虑网络因素的影响即可。
两种方案：
1. 设计一个新的得分机制，Score = network_score - compute_score
2. 根据network排序后，选择一个算力阈值之下的最高network得分节点

对于第一种方案，应该不需要权重，只需要归一化即可，因为网络得分和计算得分的量纲不同。
"""
import numpy as np
from Topo_class_def import Topo

def compute_network_score(node_index, node_network)->float:
    """
    Compute the network score for a node
    """
    bw_list = [bw for i, bw in enumerate(node_network) if i != node_index and bw > 0]
    avg_bw = np.mean(bw_list)
    min_bw = np.min(bw_list)
    std_bw = np.std(bw_list)

    score_avg = np.log10(avg_bw) if avg_bw > 0 else 0
    score_min = np.log(min_bw + 1)  # +1防止0值
    score_stability = 1 - (std_bw / (avg_bw + 1e-8))  # 防止除零

    raw_score = (
        0.6 * score_avg + 0.2 * score_min + 0.2 * score_stability
    )

    return raw_score



def select_central_node(topo_info: Topo) -> int:
    """
    Select the central node based on the network score, and return the best central node as index
    """
    network_info = topo_info.network
    # network_info is a NxN matrix, where N is the number of nodes
    network_scores_of_nodes = []
    for node_index, node_network in enumerate(network_info):
        network_scores_of_nodes.append(compute_network_score(node_index, node_network))
    max_value = max(network_scores_of_nodes)
    max_index = network_scores_of_nodes.index(max_value)
    return max_index
