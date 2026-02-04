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
        """
        source = network if network is not None else self

        extended_edges = {}
        start_state = (source.start, 1) # On est en 'pleine forme' au début.
        queue = [start_state]
        visited_states = [start_state]
        
        while queue:
            current_state = queue.pop(0)
            u, current_fatigue = current_state
            
            if u in source.roads:
                # Eviter d'avoir une erreur dans le cas ou current_state n'est pas encore une clé du dictionnaire
                if current_state not in extended_edges:
                    extended_edges[current_state] = []

                for v, length, fatigue_cost in source.roads[u]:
                    new_fatigue = current_fatigue + fatigue_cost
                    travel_time = length * current_fatigue
                    next_state = (v, new_fatigue)
                    extended_edges[current_state].append((next_state, travel_time))
                    
                    if next_state not in visited_states:
                        visited_states.append(next_state)
                        queue.append(next_state)
                        
        return Graph(extended_edges)
