# Technical details: reasoning and complexity

*ENSAE Paris · 1st-year programming project (2026) · Emmanuelle Chocron & Samuel Placek*

← [Back to README](../README.md) · 🇫🇷 [Version française](details-techniques.md)

This repository contains the source code of ENSAE's 2026 programming project. The goal is to model an agent moving through an environment constrained by fatigue, and to find optimal paths.

## Part 1 - Minimum-time path

### Part 1.1: No-fatigue case

This first step focuses on finding the fastest path between a start point and a destination, in an environment where the fatigue coefficient is constant and equal to 1 ($f(e) = 1$).

#### Implementation choices and program architecture

Following the specifications, the code is built around two main classes:

1.  **`Network` class**:
    * Represents the full environment: roads, lengths and fatigue coefficients.
    * **Added method**: `build_simple_graph(self)`. Builds a graph, i.e. the special case of a network without fatigue. This reduces the problem to a classic weighted-graph problem.

2.  **`Graph` class**:
    * Represents the mathematical structure of the graph (nodes and weighted edges).
    * **Added method**: `shortest_path(self, start, end)`. Implements **Dijkstra's algorithm** to find the shortest path.

#### Why Dijkstra's algorithm?
In this part, edges have non-negative lengths ($l(e) \ge 0$) and fatigue does not accumulate, so the problem reduces to finding a shortest path in a graph with non-negative weights. Dijkstra's algorithm is the standard and most efficient solution for this case.

#### Complexity
The complexity of `shortest_path` is $\mathcal{O}((n+m)\log(n))$, with $n$ the number of nodes and $m$ the number of edges. For heap extraction, each node is visited at most once and each `heappop` costs $\mathcal{O}(\log(n))$. Since `heappop` is called at most $n$ times, the total extraction cost is $\mathcal{O}(n\log(n))$. For heap insertion, the `heappush` line runs at most once per edge. Each `heappush` costs $\mathcal{O}(\log(n))$ and in the worst case the heap holds $\mathcal{O}(m)$ elements, so the total insertion cost is $\mathcal{O}(m\log(n))$.

### Part 1.2: Case with fatigue
We now consider the general case: finding a shortest path in an extended graph. We first represent the extended graph in the `Graph` class. Once it is built, the Dijkstra algorithm from the previous question can be reused.

1. `build_extended_graph` function in the `Network` class:
   The key idea: each node $u$ of the original graph becomes a pair (u, fatigue) in the extended graph. This models the fact that passing through the same crossroads with a different fatigue level is not the same situation.

   The `queue` drives a breadth-first search (BFS). BFS guarantees that states are explored in increasing layers of fatigue, which is consistent with the cumulative nature of fatigue.

   Final remark on this function: what we call `super_node` are canonical arrival nodes. Since the fatigue at arrival is unpredictable (it depends on the path taken), we create a "collector" node (u, 0) towards which all states (u, \*) converge for free (cost 0). This makes it possible to call `shortest_path(start, (destination, 0))` without knowing the final fatigue.

2. Reusing `shortest_path(self, start, end)` in the `Graph` class:
   Having just built an extended graph means `shortest_path(self, start, end)` can be used exactly as implemented in 1.1. The method is the same; the only difference is that it is called on an extended graph instead of a simple one.

#### Complexity
The complexity of `shortest_path(self, start, end)` was established above. For `build_extended_graph`: the function explores the extended graph with a BFS. Let $n$ be the number of nodes of the original graph, $m$ the number of edges, and $k$ the number of distinct $(u, \text{fatigue})$ states explored.

The main loop runs $k$ times. At each iteration, `queue.pop(0)` shifts all remaining elements, costing $\mathcal{O}(k)$ in the worst case, hence $\mathcal{O}(k^2)$ in total. In addition, the check `next_state not in visited_states` scans a list of up to $k$ elements and is performed once per extended edge, for a total cost of $\mathcal{O}(mk)$. The inner loop over neighbors contributes $\mathcal{O}(mk/n)$, dominated by $\mathcal{O}(mk)$.

The total complexity is therefore $\mathcal{O}(k^2 + mk)$.

### Part 1.3: Improving the previous solution by building only the necessary part of the extended graph
Since `shortest_path` only needs access to a node's neighbors when that node is visited, all that is required is a working `neighbors` method.
To do this, we created a subclass of `Graph` called `GraphImplicit`, which takes as argument not a list of edges but a function that returns the edges of a given node. We chose a generic design: the `GraphImplicit` subclass lives in the `graph` module, and the `network` module has a method that builds the implicit graph for a given network. Since `GraphImplicit` is a kind of graph, it made more sense to put it in `Graph`.
More precisely:
1. In the `Graph` class: `GraphImplicit` is a subclass representing an implicit graph, i.e. a graph whose nodes are not all listed in advance but generated on the fly through a `neighbors` function. Nodes are (u, fatigue) tuples representing a state.
   Design choice: an implicit representation, suited to very large or even potentially infinite graphs.

2. In the `Network` class: `build_implicit_graph` builds an implicit graph of extended (node, fatigue) states. We chose not to enumerate all states in advance, since `generate_neighbors` generates them on demand.

   In `generate_neighbors`, each node is an extended state (position, accumulated fatigue). Encoding the fatigue in the node turns the problem into a simple graph traversal.

#### Complexity
For `build_implicit_graph`, the cost is shifted to each call to `generate_neighbors`. For a state (u, fatigue), the function goes through the neighbors of u in `self._roads`, i.e. deg(u) neighbors, and builds the corresponding list in $\mathcal{O}(\deg(u))$. Over a whole path search exploring $k$ distinct states, the total cost of the calls to `generate_neighbors` is:

$$O\left(\sum_{(u,f) \text{ explored}} \deg(u)\right) = O\left(k \cdot \frac{m}{n}\right)$$

which is $\mathcal{O}(mk/n)$ in the worst case. This is a significant gain over `build_extended_graph`, which cost $\mathcal{O}(k^2 + mk)$ because of its ill-suited data structures.

### Bonus: drawing the graph and the minimum-time path

This project uses **Graphviz** to render network images. To use the graph rendering feature, `graphviz` must be installed.

**1. Python package:**
Open a terminal and run:
```bash
pip install graphviz
```

**2. System software:**
The Python package is only an interface. The Graphviz software itself must be installed on your machine:

* **Windows:** download the installer from [graphviz.org/download](https://graphviz.org/download/) (check *"Add Graphviz to the system PATH"* during installation).
* **macOS:** open a terminal and run `brew install graphviz`
* **Linux (Ubuntu/Debian):** open a terminal and run `sudo apt-get install graphviz`

We first created the network, then computed the associated optimal path with `shortest_path`, and finally generated the `mon_reseau` graph.

![Example network and optimal path](../assets/network.png)

Edges are labeled with the pair ($fatigue$, $length$) rather than $time$: without the fatigue multiplier, the choice of the shortest path could look paradoxical when reading the graph.

## Part 2 - Algorithmic improvements

### Part 2.1: Pruning

To start optimizing the program (by improving the implicit-graph method), we use a "pruning" method to remove Pareto-dominated nodes: if a node $v$ is reached with fatigue $f$ at time $t$, while $v$ had already been reached with both lower fatigue and lower time, the option ($v$, $f$, $t$) can be discarded.

To do this, we implement an "oracle": a function that takes a node $node$ as input and answers the question "Is it useful to visit $node$?". It maintains a history list of every node already visited (those for which the oracle said yes) and compares the node under examination with that history.

All that remains is to adapt `shortest_path` accordingly. To avoid conflicts with the previous parts, and since we only work with the implicit graph here, we create a new `shortest_path` method in the `GraphImplicit` class that uses the oracle.

### Part 2.2: A\* algorithm

Before implementing the algorithm, we need a suitable heuristic, i.e. a way to solve the problem faster. To be admissible, it must never overestimate the actual cost of reaching the destination, here the time.
Now, $time = length \times fatigue$, and fatigue can only increase: for the next edge $e$, $f(e) \ge$ current_fatigue.
So we need to minimize the remaining length to the destination, which gives $t_{min} = l_{min} \times$ current_fatigue.

To get $l_{min}$, the distance between a node and the destination, we run Dijkstra on the simple graph (the graph without fatigue).
However, running the algorithm from every node to get $l_{min}$ would be expensive. We therefore run Dijkstra in reverse: called from the destination, it returns a dictionary `simple_dist` of the form { $node$ : $l$ }, where $l$ is the distance between $node$ and the destination. A single Dijkstra call thus gives all the distances we need.

Finally, implementing A\* only requires reusing `shortest_path`, except that the next node `min_node` is chosen as the one minimizing $distance + heuristic$ instead of the distance alone.

#### Complexity of A\*
The structure is identical to Dijkstra on the extended graph, with the extra cost of computing the f-score. The main loop performs at most $k$ heap extractions, each in $\mathcal{O}(\log(k))$, for a total of $\mathcal{O}(k \log(k))$. For each extracted state, its neighbors are explored through `self.neighbors` (at most deg(u) neighbors for a state (u, fatigue)), with one heap insertion each in $\mathcal{O}(\log(k))$. The total number of neighbors explored over all iterations is $\mathcal{O}(mk/n)$, giving a total insertion cost of $\mathcal{O}(mk/n \log(k))$. Rebuilding the path through `came_from` costs at most $\mathcal{O}(k)$.
The total complexity is therefore: $$O\left(\left(k + \frac{m \cdot k}{n}\right) \log(k)\right) = O\left(\frac{m \cdot k}{n} \log(k)\right)$$

## Part 3: Extension - The two-player game

The goal is to reach the destination node with the **lowest total time**.

![Two-player game (Pygame version)](../assets/game.png)

To make the project robust and user-friendly, the game engine comes with two interfaces sharing the same algorithmic logic:

### 1. Terminal version (console mode)
This version works on Onyxia, since it does not open an external window as `pygame` does.
How it works:
* **Safe game loop:** user input is handled with strict checks on reachable nodes.
* **State display:** position, time and fatigue are shown clearly at each turn, directly in the console.
* **No dependencies:** no external library needed.

### 2. Graphical version (Pygame mode)
This version provides a visual, interactive representation.
How it works:
* **Dynamic layout:** since graph nodes have no native geographic coordinates, we developed a grid placement algorithm with random offsets to spread the cities evenly without overlaps.
* **Conditional rendering:** colors adapt in real time to the game state (reachable neighbors highlighted in green, destination node in gold, player tokens offset to avoid overlapping).

The terminal version runs with plain Python; the graphical version requires the `pygame` library.

Open a terminal at the root of the project and run:
```bash
pip install pygame
```
