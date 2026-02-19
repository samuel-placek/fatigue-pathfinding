from network import *
from graph import Graph

import sys 
from pathlib import Path

# Load the network

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))
NET_DIR = ROOT / "examples"

network_file = "/home/onyxia/work/Emmanuelle-Chocron---Samuel-Placek/examples/small.txt"
network = Network.from_file(NET_DIR / "small.txt")


# Part 1

# 1.1 - Case of a network without any fatigue ie a graph
def simple_case(network, start, end):
    graph = Network.build_simple_graph(network)
    return Graph.shortest_path(graph, start, end)

# 1.2 - Etablishment of an extended graph to take into account the fatigue
def extended_graph(network, start, end):
    graph = Network.build_extended_graph(network)
    return Graph.shortest_path(graph, start, end)

# 1.3 - Creation du graphe étendu en utilisant une méthode implicite 

def implicit_graph(network, start, end):
    graph = Network.build_implicit_graph(network)
    return graph.shortest_path(start, end)


#path, time = implicit_graph(network, ('lozere', 1), ('saclay', 0))
#print(path, time)


#print(graph.shortest_path(("lozere", 1), ("saclay", 0)))

#print(graph)


path, _ = implicit_graph(network, ('lozere', 1), ('saclay', 0))


Network.draw_network(network, path)