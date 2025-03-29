"""
some modules to use
"""

def dict2list(nodes_info_dict:dict, network_matrix:list, central_node_index:int) -> dict:
    """
    convert the topo dict info to list info.
    this is a format converter, convert the initial topo format into the format we need to compute the node score.
    """
    network_list = network_matrix[central_node_index]
    nodes_arithmetic_list = []
    nodes_memory_list = []
    for i in range(len(network_list)):
        if network_list[i] != 0: # if i == 0 means is the central node, we don't need to compute the score for it.
            nodes_arithmetic_list.append(nodes_info_dict[i]["arithmetic"])
            nodes_memory_list.append(nodes_info_dict[i]["memory"])
    
    res_dict = {
        "arithmetic": nodes_arithmetic_list,
        "memory": nodes_memory_list,
        "bandwidth": network_list
    }

    return res_dict