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


# Partie 1

# 1.1 - Cas d'un network sans aucune fatigue, ie d'un graphe
def simple_case(network, start, end):
    graph = Network.build_simple_graph(network)
    return Graph.shortest_path(graph, start, end)

# 1.2 - Implémentation d'un graphe étendu de manière moins optimale pour considérer la faitgue
def extended_graph(network, start, end):
    graph = Network.build_extended_graph(network)
    return Graph.shortest_path(graph, start, end)

# 1.3 - Création du graphe étendu en utilisant une méthode implicite
def implicit_graph(network, start, end):
    graph = Network.build_implicit_graph(network)
    return graph.shortest_path(start, end)

def show_network(network):
    path, _ = implicit_graph(network, ('lozere', 1), ('saclay', 0))
    network.draw_network(path)

#show_network(network)

print(implicit_graph(network, ('lozere', 1), ('saclay', 0)))

# Partie 2

# 2.1 - Suppression des noeuds Pareto dominés : méthode de "prunning"

