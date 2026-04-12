"""
This is the graph module. It contains the classes Graph and GraphImplicit
"""

import heapq

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
        distances = {start: 0}
        predecessors = {start: None}
        queue = [(0, start)]
        visited = set()
        
        while queue:
            current_dist, current_node = heapq.heappop(queue)
            if current_node in visited:
                continue
            visited.add(current_node)

            # Cas extrême
            if current_node == end:
                break

            # Exploration des voisins
            for neighbor, weight in self.neighbors(current_node):
                dist = current_dist + weight
                if dist < distances.get(neighbor, float('inf')):
                    distances[neighbor] = dist
                    predecessors[neighbor] = current_node
                    heapq.heappush(queue, (dist, neighbor))

        # Reconstruction du chemin
        if end not in distances or distances[end] == float('inf'):
            return [], float('inf')
            
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
            
        return path[::-1], distances[end]

        
class GraphImplicit(Graph):
    def __init__(self, neighbors):
        self.f = neighbors

    def neighbors(self, node):
        return self.f(node)

    def oracle(self, node, historique):
        u, fatigue = node
        
        for other_node in historique:
            v, fatigue2 = other_node
            if u == v and fatigue2 != 0 and fatigue >= fatigue2:
                return False          
        historique.append(node)
        return True

    def shortest_path(self, start, end):
        distances = {start: 0}
        predecessors = {start: None}
        queue = [(0, start)]
        historique = set()
        
        while queue:
            current_dist, min_node = heapq.heappop(queue)
            if current_dist > distances.get(min_node, float('inf')):
                continue
            if min_node == end:
                break

            # Utilisation de l'oracle
            if not self.oracle(min_node, historique):
                continue
                
            historique.add(min_node)

            # Détermination du meilleur noeud
            for neighbor, weight in self.neighbors(min_node):
                dist = distances[min_node] + weight
                
                if dist < distances.get(neighbor, float('inf')):
                    distances[neighbor] = dist
                    predecessors[neighbor] = min_node
                    heapq.heappush(queue, (dist, neighbor))

        # Reconstruction du chemin
        if end not in distances or distances[end] == float('inf'):
            return [], float('inf')
            
        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        
        return path[::-1], distances[end]

    def heuristic(self, node, distances_simples, end):
        nom_ville, fatigue = node
        return distances_simples.get(nom_ville, float('inf'))

    def a_star(self, start, end, fatigue_initiale, distances_simples):
        start_node = (start, fatigue_initiale)
        h_start = self.heuristic(start_node, distances_simples, end)
        open_set = [(h_start, start_node)]
        came_from = {}
        g_score = {start_node: 0}

        while open_set:
            current_f, current_node = heapq.heappop(open_set)
            u_actuel, fatigue_actuelle = current_node

            if u_actuel == end:
                temps_final = g_score[current_node]
                
                # Reconstruction du chemin
                chemin = []
                curr = current_node
                while curr in came_from:
                    chemin.append(curr)
                    curr = came_from[curr]
                chemin.append(curr) # On ajoute le point de départ
                chemin.reverse()
                chemin.append((end, 0))
                return chemin, temps_final

            # Exploration des voisins
            for voisin_node, poids in self.neighbors(current_node).items():
                tentative_g_score = g_score[current_node] + poids

                if tentative_g_score < g_score.get(voisin_node, float('inf')):
                    came_from[voisin_node] = current_node
                    g_score[voisin_node] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(voisin_node, distances_simples, end)
                    heapq.heappush(open_set, (f_score, voisin_node))

        return None, float('inf')