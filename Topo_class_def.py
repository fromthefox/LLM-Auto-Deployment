"""
Define the class of Topo
"""

class Topo():
    def __init__(self, network_matrix, nodes_dict, user_config_path):
        """
        network is a 2d-matrix of the network topology
        nodes_dict is a dictionary of the nodes' information
        """
        self.network_matrix = network_matrix
        self.nodes_dict = nodes_dict
        self.user_config_path = user_config_path