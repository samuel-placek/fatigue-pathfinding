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
        source = network if network is not None else self
        simple_edges = {}

        for node, neighbors_list in source._roads.items():
            new_neighbors = []
            for neighbor in neighbors_list:
                v, length, fatigue = neighbor
                new_neighbors.append((v, length))
            simple_edges[node] = new_neighbors

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
            source = network if network is not None else self

            extended_edges = {}
            start_state = (source.start, 1) # On est en 'pleine forme' au début : fatigue de 1.
            queue = [start_state] # Liste des sommets qu'on devra visiter ensuite
            visited_states = [start_state] # Liste des sommets qu'on a déjà visités pour ne pas répéter
            
            while queue:
                current_state = queue.pop(0)
                # On récupère le sommet qu'on a ajouté en premier : système de file
                u, current_fatigue = current_state
                
                if u in source._roads:
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

                    if u in source._roads:
                        for v, length, fatigue_cost in source._roads[u]:
                            new_fatigue = current_fatigue + fatigue_cost
                            travel_time = length * current_fatigue
                            next_state = (v, new_fatigue)
                            extended_edges[current_state].append((next_state, travel_time))
                            
                            if next_state not in visited_states:
                                visited_states.append(next_state)
                                queue.append(next_state)

            return Graph(extended_edges)

    def build_implicit_graph(self, network=None):
        ''' 
        Builds a function generate_neighbors which gives the neighbors of a selected node
        '''

        source = network if network is not None else self

        def generate_neighbors(extended_node):
            u, current_fatigue = extended_node
            
            neighbors = []
            
            if u in source.roads:
                for v, length, fatigue in source.roads[u]:
                    new_fatigue = current_fatigue + fatigue
                    travel_time = length * current_fatigue
                    extended_neighbor = (v, new_fatigue)
                    neighbors.append((extended_neighbor, travel_time))
            
            return neighbors
        return GraphImplicit(generate_neighbors)
