"""
This is the graph module. It contains the classes Graph and GraphImplicit
"""


class Graph:
    """
    A minimal class for directed weighted graph represented as adjacency list.
    
    Attributes:
    -----------
    edges: dict
        A dictionary that contains the list of neighbors of each node with its weight.
        Ex: edges = {v0: [(v1, 21), (v2, 12)],
                     v1: [(v0, 74), (v2, 32)],
                     ...}

    Methods:
    --------
    neighbors(self, node):
        Returns the list of all neighbors of a node

    shortest_path(self):
        Returns the shortest past from the node 'start' to the node 'end' using the Dijkstra method
    """

    def __init__(self, edges):
        self._edges = edges

    def __str__(self):
        '''
        Prints the graph as text.
        '''
        output = f"A graph with {len(self._edges)} nodes and the following adjacency list:\n"
        return output+self._edges.__str__()

    def neighbors(self, node):
        if node not in self._edges:
            return []
        return self._edges[node]

    def shortest_path(self, start, end):

        # Initialisation
        distances = {start: 0} 
        predecessors = {start: None}
        not_visited = [start]

        # Historique pour l'utilisation de l'oracle
        historique = []

        while not_visited:
            # Recherche du noeud le plus proche
            min_node = None
            for node in not_visited:
                if min_node is None or distances[node] < distances[min_node]:
                    min_node = node

            # Cas extrême : soit le programme est fini ou alors ne peut pas finir
            if min_node == end:
                break
            if distances[min_node] == float('inf'):
                break
                
            not_visited.remove(min_node)
            
            # Utilisation de l'oracle pour enlever les noeuds Pareto
            if not self.oracle(min_node, historique): # SI on n'a pas besoin d'examiner le noeud, on le saute
                continue 
            
            # Détermination du meilleur noeud
            for neighbor, weight in self.neighbors(min_node):
                dist = distances[min_node] + weight
                
                if neighbor not in distances:
                    distances[neighbor] = float('inf')
                    not_visited.append(neighbor)

                if dist < distances[neighbor]:
                    distances[neighbor] = dist
                    predecessors[neighbor] = min_node

        # Reconstruction du chemin optimal

        if end not in distances or distances[end] == float('inf'):
            return [], float('inf')

        path = []
        current_node = end

        while current_node is not None:
            path.append(current_node)
            current_node = predecessors[current_node]

        path = path[::-1]
        return path, distances[end]
        
class GraphImplicit(Graph):
    def __init__(self, neighbors):
        self.f = neighbors

    def neighbors(self, node):
        return self.f(node)

    def oracle(self, node, historique):
        u, fatigue = node
        
        for other_node in historique:
            v, fatigue2 = other_node
            if u == v and fatigue >= fatigue2:
                return False 
        historique.append(node)
        return True

    def heuristic(self, node, distances_simples, end_physique): # distances_simples : dict des distances physiques précalculées vers l'arrivée
        u, fatigue = node
        if fatigue == 0 or u == end_physique:
            return 0
        dist_min = distances_simples[(u, 0)]
        return fatigue * dist_min