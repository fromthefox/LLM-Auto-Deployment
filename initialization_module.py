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

def compute_network_score(node_network)->float:
    """
    Compute the network score for a node
    """
    pass

def select_central_node(topo_info: Topo) -> int:
    """
    Select the central node based on the network score, and return the best central node as index
    """
    network_info = topo_info.network
    # network_info is a NxN matrix, where N is the number of nodes
    network_scores_of_nodes = []
    for node_network in network_info:
        network_scores_of_nodes.append(compute_network_score(node_network))
    max_value = max(network_scores_of_nodes)
    max_index = network_scores_of_nodes.index(max_value)
    return max_index
