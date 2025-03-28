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

def select_central_node(nodes_list):
    """
    Select the central node based on the network score
    """
    # Get the network score
    network_scores = np.array([get_network_metrics(node)['score'] for node in nodes_list])
    # Get the index of the node with the highest network score
    return np.argmax(network_scores)