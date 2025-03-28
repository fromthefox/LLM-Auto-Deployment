"""
this file is used to create the initial topology of the project
By default all information about the entire topology is known, i.e. it is straightforward to give the res
"""

# Intent parsing can even be added here to do it lol
from Topo_class_def import Topo

def create_topo():
    """
    Create the topology of the network
    """
    network = [
        [0, 10, 20, 30, 40],
        [10, 0, 10, 20, 30],
        [20, 10, 0, 10, 20],
        [30, 20, 10, 0, 10],
        [40, 30, 20, 10, 0]
    ]
    # Mbps
    nodes_dict = {
        0: {"arithmetic": 0.5, "memory": 0.5},
        1: {"arithmetic": 0.6, "memory": 0.6},
        2: {"arithmetic": 0.7, "memory": 0.7},
        3: {"arithmetic": 0.8, "memory": 0.8},
        4: {"arithmetic": 0.9, "memory": 0.9}
    }
    """
    Here, in actuality NETWORK can be given directly like this, since we built the topology ourselves and know the bandwidth by default;
    Arithmetic and memory need to be calculated by the previous arithmetic_evaluation_module and bandwidth_evaluation_module to get the
    """
    topo = Topo(network, nodes_dict)

    return topo