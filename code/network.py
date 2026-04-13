from graph import *

class Network:
    """
    Class for a network that represents the environment (with length and fatigue on roads).
    """

    def __init__(self, roads={}, start=None, end=None):
        """
        Initializes the network from a dictionary roads.

        Parameters:
        -----------
        roads: dict
            A dictionary of the roads as an adjacency list, that is
            roads[u] = list of (v, length, fatigue)
            Ex: roads = {v0: [(v1, 21, 2), (v2, 12, 4)],
                        v1: [(v0, 74, 2), (v2, 32, 1)],
                        ...}
        start, end:
            Start and end nodes added as attributes
        """
        self._roads = roads
        self.start = start
        self.end = end

    def __str__(self):
        """
        Prints the network as text.
        """
        output = f"A network with {len(self._roads)} nodes and the following adjacency list:\n"
        return output+self._roads.__str__()

    @classmethod
    def from_file(cls, filename: str):
        """
        Creates a Network from an environment file.

        File format: one edge per line (start end length fatigue).
        """
        # Initialize adjacency list
        roads = {}

        with open(filename, "r") as testcase:
            nb, start, end = testcase.readline().strip().split()
            for _ in range(int(nb)):
                i, j, l, f = testcase.readline().strip().split()
                l, f = int(l), int(f)
                roads.setdefault(i, []).append((j, l, f))
                roads.setdefault(j, [])

        return cls(roads=roads, start=start, end=end)

    def build_simple_graph(self, network=None):
            """
            Builds an object of type Graph from the class by default, else by an imported network,
            by ignoring the fatigue coefficient.
            """
        
            simple_edges = {
                node: [(v, length) for v, length, fatigue in voisins] 
                for node, voisins in self._roads.items()
            }

            return Graph(simple_edges)

    def build_extended_graph(self, network=None):
            """
            Builds an object of type Graph from the class by default, else by an imported network, 
            by taking into account the general case of fatigue.
            Returns an object of type Graph with new nodes.

            Ex : extented_graph = {(v, fatigue) : [((v1, fatigue1), time1), ((v2, faituge2), time2)],
                                    ...}
            }
            """

            extended_edges = {}
            start_state = (self.start, 1) # On est en 'pleine forme' au début : fatigue de 1.
            queue = [start_state] # Liste des sommets qu'on devra visiter ensuite
            visited_states = [start_state] # Liste des sommets qu'on a déjà visités pour ne pas répéter
            
            while queue:
                current_state = queue.pop(0)
                # On récupère le sommet qu'on a ajouté en premier : système de file
                u, current_fatigue = current_state
                
                if u in self._roads:
                    if current_state not in extended_edges:
                        # Eviter d'avoir une erreur dans le cas où current_state n'est pas encore une clé du dictionnaire
                        extended_edges[current_state] = []
                    '''
                    On crée des 'super arrivées' afin de pouvoir appeler la fonction shortest_path avec des éléments connus,
                    par exemple, le time et la fatigue sont inconnus si on ne plonge pas dans le programme, on construit donc
                    des sommets d'arrivée de la forme (u, 0) car c'est plus pratique
                    '''
                    super_node = (u, 0)
                    if current_state != super_node:
                        extended_edges[current_state].append((super_node, 0))
                        if super_node not in extended_edges:
                            extended_edges[super_node] = []

                    if u in self._roads:
                        for v, length, fatigue_cost in self._roads[u]:
                            new_fatigue = current_fatigue + fatigue_cost
                            travel_time = length * current_fatigue
                            next_state = (v, new_fatigue)
                            extended_edges[current_state].append((next_state, travel_time))
                            
                            if next_state not in visited_states:
                                visited_states.append(next_state)
                                queue.append(next_state)

            return Graph(extended_edges)

    def build_implicit_graph(self, network=None):
        """
        Builds an object of type GraphImplicit based on the current network.
        
        This method is used for state-space search (pruning method) to generate 
        nodes and neighbors on the fly, avoiding full memory allocation for fatigue states.
        Returns an object of type GraphImplicit.
        """
        
        def generate_neighbors(extended_node):
            u, current_fatigue = extended_node

            if current_fatigue == 0: # Cas ou on est sur une super arrivée
                return []

            neighbors = []
            
            super_node = (u, 0)
            neighbors.append((super_node, 0))

            if u in self._roads:
                for v, length, fatigue in self._roads[u]:
                    new_fatigue = current_fatigue + fatigue
                    time = length * current_fatigue
                    extended_neighbor = (v, new_fatigue)
                    neighbors.append((extended_neighbor, time))
            
            return neighbors
        return GraphImplicit(generate_neighbors)


    def draw_network(self, path, filename):
        """
        Generates a visual representation of the current network using Graphviz.
        
        If a specific path is provided, it highlights the corresponding nodes and edges.
        The resulting graph is saved as an image file on the disk.
        Returns a string confirming the successful generation of the file.
        """
        import graphviz
              
        dot = graphviz.Digraph(comment='Chemin de temps minimal', format='png')
        dot.attr(rankdir='LR')

        physical_path = [state[0] for state in path]
        path_edges = []

        for i in range(len(physical_path) - 1):
            u = physical_path[i]
            v = physical_path[i+1]
            path_edges.append((u, v))

        all_nodes = list(self._roads.keys())
        for u in self._roads:
            for v, _, _ in self._roads[u]:
                all_nodes.append(v)

        for node in all_nodes:
            if node == self.start:
                dot.node(str(node), str(node), color='purple', style='filled', fillcolor='plum')
            elif node == self.end:
                dot.node(str(node), str(node), color='blue', style='filled', fillcolor='lightblue')
            else:
                dot.node(str(node), str(node))

        for u in self._roads:
            for v, length, fatigue_coeff in self._roads[u]:
                edge_label = f"len = {length}, f = {fatigue_coeff}"
                if (u, v) in path_edges:
                    dot.edge(str(u), str(v), label=edge_label, color='hotpink', penwidth='2.5', fontcolor='red')
                else:
                    dot.edge(str(u), str(v), label=edge_label)

        dot.render(filename, view=False)

    def reversed_dijkstra(self, end):
        """
        Computes the shortest path from all nodes in the network to a target node.
        
        This method ignores fatigue constraints to calculate simple distances. 
        It is primarily used to pre-compute an admissible heuristic for the A* algorithm.
        Returns a dictionary containing the minimum distance from each node to the end node.
        
        Ex : simple_distances = {'lozere': 15, 'orsay': 5, 'saclay': 0, ...}
        """
        routes_inverses = {ville: [] for ville in self._roads.keys()}
        
        for origine, destinations in self._roads.items():
            for destination, poids, fatigue_cost in destinations:
                if destination in routes_inverses:
                    routes_inverses[destination].append((origine, poids))

        distances_simples = {ville: float('inf') for ville in self._roads.keys()}
        distances_simples[end] = 0
        queue = [(0, end)]
        visited = set()

        while queue:
            dist_actuelle, noeud_actuel = heapq.heappop(queue)

            if noeud_actuel in visited:
                continue
            visited.add(noeud_actuel)

            for voisin, poids in routes_inverses[noeud_actuel]:
                nouvelle_dist = dist_actuelle + poids
                
                if nouvelle_dist < distances_simples[voisin]:
                    distances_simples[voisin] = nouvelle_dist
                    heapq.heappush(queue, (nouvelle_dist, voisin))

        return distances_simples
