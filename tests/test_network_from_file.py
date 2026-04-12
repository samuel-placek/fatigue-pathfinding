import sys 
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

import unittest 
from network import Network
from answers import *

class Test_NetworkLoading(unittest.TestCase):
    def test_network_small(self):
        network = Network.from_file(NET_DIR / "small.txt")
        self.assertEqual(network.start, "lozere")
        self.assertEqual(network.end, "saclay")
        self.assertEqual(network._roads, {'lozere': [('ensae', 10, 2), ('guichet', 20, 0)], 
                                          'ensae': [('saclay', 45, 0)], 
                                          'guichet': [('ensae', 15, 1)],
                                          'saclay': []})


class Test_Part1(unittest.TestCase):
    # Question 1

    def test_build_simple_graph(self):
        network = Network.from_file(NET_DIR / "small.txt")
        graph = Network.build_simple_graph(network)
        self.assertEqual(graph._edges, {'lozere': [('ensae', 10), ('guichet', 20)],
                                        'ensae': [('saclay', 45)],
                                        'guichet': [('ensae', 15)],
                                        'saclay': []})

    def test_shortest_path(self):
        network = Network.from_file(NET_DIR / "small.txt")
        small_graph = network.build_simple_graph(network)

        start, end = "lozere", "saclay"
        path, dist = small_graph.shortest_path(start, end)

        self.assertEqual(path, ["lozere", "ensae", "saclay"])
        self.assertEqual(dist, 55)
    
    # Question 2
    def test_build_extended_graph(self):
        network = Network.from_file(NET_DIR / "small.txt")
        extended_graph = Network.build_extended_graph(network)

        start, end = ("lozere", 1), ("saclay", 0)
        path, time = extended_graph.shortest_path(start, end)

        self.assertEqual(extended_graph._edges, {
                                                ('lozere', 1): [(('lozere', 0), 0), (('ensae', 3), 10), (('guichet', 1), 20)],
                                                ('lozere', 0): [],
                                                ('ensae', 3): [(('ensae', 0), 0), (('saclay', 3), 135)],
                                                ('ensae', 0): [],
                                                ('guichet', 1): [(('guichet', 0), 0), (('ensae', 2), 15)],
                                                ('guichet', 0): [],
                                                ('saclay', 3): [(('saclay', 0), 0)],
                                                ('saclay', 0): [],
                                                ('ensae', 2): [(('ensae', 0), 0), (('saclay', 2), 90)],
                                                ('saclay', 2): [(('saclay', 0), 0)]})
        self.assertEqual(path, [('lozere', 1), ('guichet', 1), ('ensae', 2), ('saclay', 2), ('saclay', 0)])
        self.assertEqual(time, 125)

    # Question 3
    def test_implicit_graph(self):
        network = Network.from_file(NET_DIR / "small.txt")
        implicit_graph = Network.build_implicit_graph(network)

        start, end = ("lozere", 1), ("saclay", 0)
        path, time = implicit_graph.shortest_path(start, end)

        self.assertEqual(path, [('lozere', 1), ('guichet', 1), ('ensae', 2), ('saclay', 2), ('saclay', 0)])
        self.assertEqual(time, 125)

class Test_Part2(unittest.TestCase):
    def test_algo_a_star(self):
        network = Network.from_file(NET_DIR / "small.txt")
        start, end = "lozere", "saclay"
        path, time = algo_a_star(network, start, end)

        self.assertEqual(path, [('lozere', 1), ('guichet', 1), ('ensae', 2), ('saclay', 2), ('saclay', 0)])
        self.assertEqual(time, 125)


if __name__ == '__main__':
    unittest.main()
