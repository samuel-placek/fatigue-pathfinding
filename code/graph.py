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


    def heuristic(self, node, distances_simples, end): # distances_simples : dict des distances physiques précalculées vers l'arrivée
        u, fatigue = node
        if fatigue == 0 or u == end:
            return 0
        dist_min = distances_simples[(u, 0)]
        return fatigue * dist_min


    def reversed_dijkstra(self, end):
        # création du graphe inversé
        routes_inverses = {noeud: [] for noeud in self._roads.keys()}
        
        for origine, destinations in self._roads.items():
            liste_dest = destinations
            for info_route in liste_dest:
                destination = info_route[0]
                poids = info_route[1] 
                if destination in routes_inverses:
                    routes_inverses[destination].append((origine, poids))

        # Dijkstra sur le graphe inversé
        distances_simples = {}
        noeuds_non_visites = list(self._roads.keys()) 

        for noeud in noeuds_non_visites:
            distances_simples[(noeud, 0)] = float('inf') 

        distances_simples[(end, 0)] = 0

        while noeuds_non_visites:
            noeud_actuel = None
            dist_min = float('inf')
            for noeud in noeuds_non_visites:
                if distances_simples[(noeud, 0)] < dist_min:
                    dist_min = distances_simples[(noeud, 0)]
                    noeud_actuel = noeud            
            if noeud_actuel is None:
                break
                
            noeuds_non_visites.remove(noeud_actuel)
            
            for voisin, poids in routes_inverses[noeud_actuel]:
                if voisin in noeuds_non_visites:
                    nouvelle_dist = dist_min + poids        
                    if nouvelle_dist < distances_simples[(voisin, 0)]:
                        distances_simples[(voisin, 0)] = nouvelle_dist
                        
        return distances_simples


    import heapq

    def a_star(self, start, end, fatigue_initiale, distances_simples):
        """
        Trouve le chemin le plus court en utilisant l'algorithme A*.
        Les noeuds sont gérés sous la forme de tuples : (lieu_physique, fatigue_accumulee).
        """

        start_node = (start, fatigue_initiale)
        open_set = []
        
        h_start = self.heuristic(start_node, distances_simples, end)
        heapq.heappush(open_set, (h_start, start_node))
        
        came_from = {}
        g_score = {start_node: 0}
        
        while open_set:
            current_f, current_node = heapq.heappop(open_set)
            u_actuel, fatigue_actuelle = current_node
            
            if u_actuel == end_physique:
                chemin = [current_node]
                while current_node in came_from:
                    current_node = came_from[current_node]
                    chemin.append(current_node)
                chemin.reverse()
                
                return chemin, g_score[(u_actuel, fatigue_actuelle)]
            
            voisins = self._roads.get(u_actuel, [])
            if isinstance(voisins, dict):
                liste_dest = voisins.items()
            else:
                liste_dest = voisins
                
            for info_route in liste_dest:
                voisin = info_route[0]
                poids = info_route[1]
                nouvelle_fatigue = fatigue_actuelle + poids 
                voisin_node = (voisin, nouvelle_fatigue)
                tentative_g_score = g_score[current_node] + poids
                
                if tentative_g_score < g_score.get(voisin_node, float('inf')):
                    came_from[voisin_node] = current_node
                    g_score[voisin_node] = tentative_g_score
                    h_score = self.heuristic(voisin_node, distances_simples, end_physique)
                    f_score = tentative_g_score + h_score
                    heapq.heappush(open_set, (f_score, voisin_node))
                                 
        return None, float('inf')