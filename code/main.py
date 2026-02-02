from network import Network
from graph import Graph

# Load the network
network_file = "/home/onyxia/Emmanuelle-Chocron---Samuel-Placek/examples/small.txt"
network = Network.from_file(network_file)


# Part 1

# 1.1 - Case of a network without any fatigue ie a graph
def simple_case(network, start, end):
    graph = Network.build_simple_graph(network)
    return Graph.shortest_path(graph, start, end)