"""
Overall framework
"""
from central_node_selection import select_central_node
from initial_topo import create_topo
from model_preprocessing import model_usage_memory_prediction, model_selection
from function_modules import dict2list
from compute_score_module import dynamic_weights, total_score

if __name__ == "__main__":

    # 1. Get the necessary information and Create the Topo
    topo_info = create_topo()

    # 2. Select the model file and determine the relevant information
    model_params_num = model_selection("llama-3-8B")
    model_usage_memory = model_usage_memory_prediction(model_params_num, "float32")

    # 3. Initial centre node selection
    central_node_index = select_central_node(topo_info, model_usage_memory)

    # 4. Calculation of the distribution of tasks

    # 4.1. Preparation work
    nodes_info_dict = dict2list(topo_info.nodes_dict, topo_info.network_matrix, central_node_index)

    # 4.2. calculate the score for each node
    dynamic_weights_array = dynamic_weights(nodes_info_dict)
    scores_list = total_score(nodes_info_dict, dynamic_weights_array)

    # 4.3. Determination of the proportion of mandates to be allocated

    