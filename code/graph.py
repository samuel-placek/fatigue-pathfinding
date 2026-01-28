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
    neighbours(self, node):
        Returns the list of all neighbors of a node

    shortest_path(self):
        Returns the shortest past from the node 'start' to the node 'end' using the Dijkstra method
    """

    def __init__(self, edges):
        self._edges = edges

    def neighbours(self, node):
        if node not in self._edges:
            return []
        return self._edges[node]

    def shortest_path(self, start, end):

        # Initialisation
        distances = {node: float('inf') for node in self._edges}
        distances[start] = 0
        
        predecessors = {node: None for node in self._edges}
        
        not_visited = list(self._edges.keys())

        while not_visited:
            # Research of the nearest node
            min_node = None
            for node in not_visited:
                if min_node is None:
                    min_node = node
                elif distances[node] < distances[min_node]:
                    min_node = node

            # Extreme cases : either the program is done or can not be finished
            if min_node == end:
                break
            if distances[min_node] == float('inf'):
                break
                
            not_visited.remove(min_node)
            
            # Determination of the best node
            for neighbour, weight in Graph.neighbours(self, min_node):
                dist = distances[min_node] + weight
                
                if dist < distances[neighbour]:
                    distances[neighbour] = dist
                    predecessors[neighbour] = min_node

        # Reconstruction of the shortest path
        path = []
        current_node = end
        
        if distances[end] == float('inf'):
            return [], float('inf')

        while current_node is not None:
            path.append(current_node)
            current_node = predecessors[current_node]

        path = path[::-1]
        return path, distances[end]