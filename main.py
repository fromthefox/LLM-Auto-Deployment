"""
Overall framework
"""
from central_node_selection import select_central_node
from initial_topo import create_topo

if __name__ == "__main__":

    # 1. Get the necessary information and Create the Topo
    topo_info = create_topo()

    # 2. Select the model file and determine the relevant information
    

    # 3. Initial centre node selection
    central_node_index = select_central_node(topo_info)

    # 3. 