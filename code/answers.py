from network import *
from graph import *

# Partie 1 -  Chemin de temps minimal

# 1.1 - Cas d'un network sans aucune fatigue, ie d'un graphe
def simple_case(network, start, end):
    graph = network.build_simple_graph()
    return graph.shortest_path(start, end)

# 1.2 - Implémentation d'un graphe étendu de manière moins naïve pour considérer la faitgue
def extended_graph(network, start, end):
    graph = network.build_extended_graph()
    return graph.shortest_path((start, 1), (end, 0))

# 1.3 - Création du graphe étendu en utilisant une méthode implicite
def implicit_graph(network, start, end):
    graph = network.build_implicit_graph(network)
    return graph.shortest_path((start, 1), (end, 0))

def show_network(network, start, end, filename="Représentation du réseau"):
    path, _ = algo_a_star(network, start, end)
    network.draw_network(path, filename)
    return f"Graphique généré avec succès : {filename}.png"


# Partie 2 - Améliorations algorithmiques 

# 2.1 - Suppression des noeuds Pareto dominés : méthode de "prunning"
'''
En réalité, l'appel à la fonction implicit_graph en 1.3 utilise déjà la méthode de prunning car la méthode shortest_path 
de la classe GraphImplicit enlève les noeuds Pareto dominés grâce à l'utilisation de la méthode oracle
'''

# 2.2 - Algorithme A*
def algo_a_star(network, start, end):
    graph = network.build_implicit_graph()
    distances_simples = network.reversed_dijkstra(end)
    chemin, cout = graph.a_star(start, end, 1, distances_simples)
    
    if chemin is None:
        return "Destination non atteignable"
    else:
        return chemin, cout
    

# Partie 3 - Extensions 