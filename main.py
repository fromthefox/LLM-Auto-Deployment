"""
Overall framework
"""

import argparse
from central_node_selection import select_central_node
from initial_topo import create_topo
from model_preprocessing import model_usage_memory_prediction, model_selection
from function_modules import dict2list
from compute_score_module import dynamic_weights, total_score
from function_modules import proportinal_allocation
from Distributed_Llama_Py.model_inference_main_for_server import infenerce_main_for_server


if __name__ == "__main__":

    # 0. Parse the command line arguments
    parser = argparse.ArgumentParser(description="Distributed Llama Inference")
    parser.add_argument('--host_index', type=int, default=None, help='host index of the current node')
    args = parser.parse_args()

    host_index = args.host_index

    # 1. Get the necessary information and Create the Topo, load the user_config
    topo_info = create_topo()
    user_config_path = topo_info.user_config_path

    # 2. Select the model file and determine the relevant information
    model_info_dict = model_selection("llama-3-8B")
    model_path = model_info_dict["model_path"]
    tokenizer_path = model_info_dict["tokenizer_path"]
    config_path = model_info_dict["config_path"]
    model_params_num = model_info_dict["params_num"]
    model_unsplitted_dim = model_info_dict("unsplitted_dim")
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
    allocation_list = proportinal_allocation(scores_list, model_unsplitted_dim)

    # 5. Calling the distributed-llama-python interface to perform distributed inference
    inference_result = infenerce_main_for_server(
        allocation_list=allocation_list,
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        user_config_path=user_config_path
    )

    print(inference_result)