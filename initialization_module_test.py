import numpy as np
from compute_score_module import calculate_compute_scores
from function_modules import get_network_metrics

def normalize_scores(scores):
    """归一化处理得分到[0,1]范围"""
    min_score = np.min(scores)
    max_score = np.max(scores)
    return (scores - min_score) / (max_score - min_score + 1e-8)  # 添加微小值避免除零

def select_central_node(candidate_nodes):
    """
    根据方案1选择中心节点
    综合得分 = 归一化网络得分 - 归一化计算得分
    """
    # 获取网络得分和计算得分
    network_scores = np.array([get_network_metrics(node)['score'] for node in candidate_nodes])
    compute_scores = calculate_compute_scores(candidate_nodes)
    
    # 归一化处理
    norm_network = normalize_scores(network_scores)
    norm_compute = normalize_scores(compute_scores)
    
    # 计算综合得分
    combined_scores = norm_network - norm_compute
    
    # 返回得分最高的节点索引
    return np.argmax(combined_scores)

if __name__ == "__main__":
    # 测试样例
    test_nodes = [...]  # 需要替换为实际的节点数据
    selected_index = select_central_node(test_nodes)
    print(f"Selected central node index: {selected_index}")
