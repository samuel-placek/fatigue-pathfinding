# Fatigue-Aware Pathfinding

> 🇫🇷 [Version française](README.fr.md)

**Finding the fastest route when every step makes you more tired**: from Dijkstra to A\* on state-augmented graphs, with complexity analysis and a playable two-player game.

*ENSAE Paris · 1st-year programming project (2026) · Samuel Placek & Emmanuelle Chocron*

![Example network and optimal path](assets/network.png)

## The problem

An agent travels through a road network. Each road has a **length** and a **fatigue coefficient**. The time needed to cross a road is its length multiplied by the agent's current fatigue, and **fatigue only increases** along the way.

The goal is to reach the destination in **minimum total time**. Because fatigue depends on the path already taken, passing through the same crossroads with two different fatigue levels is not the same situation. A classic shortest-path algorithm is not enough.

## Approach

*n = nodes, m = edges, k = explored (node, fatigue) states*

| Step | Idea | Complexity |
|---|---|---|
| **1.1 No fatigue** | Reduce to a weighted graph and run **Dijkstra** with a binary heap | O((n + m) log n) |
| **1.2 With fatigue** | Build an **extended state graph** whose nodes are (node, fatigue) pairs, explored by BFS; arrival "super-nodes" collect every fatigue level at the destination, then reuse Dijkstra unchanged | O(k² + mk) to build |
| **1.3 Implicit graph** | Only generate the part of the extended graph that is needed: a `GraphImplicit` subclass computes neighbors **on demand** | O(mk / n) for neighbor generation |
| **2.1 Pruning** | An "oracle" discards **Pareto-dominated** states (reached with both more fatigue and more time) | Fewer states explored |
| **2.2 A\*** | **Admissible heuristic**: since fatigue never decreases, the remaining time is at least *shortest remaining length × current fatigue*. All shortest remaining lengths come from a **single reverse Dijkstra** from the destination | O((mk / n) log k) |

Detailed reasoning and complexity proofs: [docs/technical-details.md](docs/technical-details.md).

## Two-player game

![Two-player game (Pygame version)](assets/game.png)

Two players race from the start to the destination; the lowest total time wins. The game engine has two interfaces sharing the same logic:

- **Terminal version**: no external dependency, safe input handling, position / time / fatigue shown at each turn. Works on cloud environments such as Onyxia.
- **Pygame version**: nodes placed automatically on a grid with random offsets to avoid overlaps, reachable neighbors highlighted in green, destination in gold.

## Project structure

```
code/
  network.py   Network class: roads, lengths, fatigue; builds the simple, extended and implicit graphs
  graph.py     Graph and GraphImplicit classes: Dijkstra, Pareto pruning, A*
  game.py      Two-player game (terminal and Pygame)
  main.py      Interactive entry point: run the tests, run any function on a chosen network, or play the game
  answers.py   Answers to the project questions
examples/      Test networks: small, medium and large, each with no / small / large fatigue
tests/         Unit tests (unittest and pytest)
assets/        Images: example network (Graphviz) and game screenshot
docs/          Detailed reasoning and complexity proofs (English and French)
```

## Getting started

```bash
pip install -r requirements.txt
python code/main.py
```

`main.py` opens an interactive menu (prompts are in French):

1. **Run the tests**
2. **Run a function** from `answers.py` on a network of your choice (e.g. `small.txt`); the menu asks for each argument
3. **Play the two-player game**, in the terminal or with Pygame

The tests can also be run directly with `python -m pytest tests/`.

Graph rendering also requires the [Graphviz](https://graphviz.org/download/) system package (`brew install graphviz` on macOS, `sudo apt-get install graphviz` on Ubuntu).

## Authors

**Samuel Placek** · **Emmanuelle Chocron**: ENSAE Paris
