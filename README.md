# ENSAE 1A - Projet de Programmation 2026 - Emmanuelle Chocron / Samuel Placek

Ce dépôt contient le code source du projet de programmation 2026 de l'ENSAE. L'objectif est de modéliser le déplacement d'un agent dans un environnement contraint par la fatigue et de trouver des chemins optimaux. 

## Partie 1 - Chemin de temps minimal

### Partie 1.1 : Cas sans fatigue

Cette première étape du projet se concentre sur la recherche du chemin le plus rapide entre un point de départ et un point d'arrivée, en considérant un environnement où le coefficient de fatigue est nul ($f(e) = 0$).

#### Choix d'implémentation et architecture du programme

Conformément aux spécifications, nous avons structuré le code autour de deux classes principales :

1.  **Classe `Network`** :
    * Représente l'environnement complet avec les routes, les longueurs et les coefficients de fatigue.
    * **Méthode ajoutée** : `build_simple_graph(self)`. Cette méthode transforme permet de construite un graphe, qui est un cas particulier de network où il n'y a pas        de fatigue. Cela permet de se ramener à un problème de graphe pondéré classique.

2.  **Classe `Graph`** :
    * Représente la structure mathématique du graphe (noeuds et arêtes pondérées).
    * **Méthode ajoutée** : `shortest_path(self, start, end)`. Cette méthode implémente l'**algorithme de Dijkstra** qui permet d'obtenir le plus court chemin.

#### Pourquoi l'algorithme de Dijkstra ?
Puisque nous travaillons dans cette partie avec des arêtes ayant des longueurs positives ($l(e) \ge 0$) et sans accumulation de fatigue, le problème se réduit à la recherche d'un plus court chemin dans un graphe pondéré à poids positifs. L'algorithme de Dijkstra est la solution standard la plus efficace pour ce cas de figure.

#### Compléxité de l'algorithme

