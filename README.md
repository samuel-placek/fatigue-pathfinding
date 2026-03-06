# ENSAE 1A - Projet de Programmation 2026 - Emmanuelle Chocron / Samuel Placek

Ce dépôt contient le code source du projet de programmation 2026 de l'ENSAE. L'objectif est de modéliser le déplacement d'un agent dans un environnement contraint par la fatigue et de trouver des chemins optimaux. 

## Partie 1 - Chemin de temps minimal

### Partie 1.1 : Cas sans fatigue

Cette première étape du projet se concentre sur la recherche du chemin le plus rapide entre un point de départ et un point d'arrivée, en considérant un environnement où le coefficient de fatigue est nul ($f(e) = 0$).

#### Choix d'implémentation et architecture du programme

Conformément aux spécifications, nous avons structuré le code autour de deux classes principales :

1.  **Classe `Network`** :
    * Représente l'environnement complet avec les routes, les longueurs et les coefficients de fatigue.
    * **Méthode ajoutée** : `build_simple_graph(self)`. Cette méthode transforme permet de construite un graphe, qui est un cas particulier de network où il n'y a pas de fatigue. Cela permet de se ramener à un problème de graphe pondéré classique.

2.  **Classe `Graph`** : 
    * Représente la structure mathématique du graphe (noeuds et arêtes pondérées).
    * **Méthode ajoutée** : `shortest_path(self, start, end)`. Cette méthode implémente l'**algorithme de Dijkstra** qui permet d'obtenir le plus court chemin.

#### Pourquoi l'algorithme de Dijkstra ?
Puisque nous travaillons dans cette partie avec des arêtes ayant des longueurs positives ($l(e) \ge 0$) et sans accumulation de fatigue, le problème se réduit à la recherche d'un plus court chemin dans un graphe pondéré à poids positifs. L'algorithme de Dijkstra est la solution standard la plus efficace pour ce cas de figure.

### Complexité de l'algorithme de Dijsktra:


### Partie 1.2 : Cas avec fatigue
On considère maintenant le cas général. Il s'agit alors de chercher un plus court chemin dans un graphe étendu. Pour cela, nous avons d'abord représenter le graphe étendu dans la classe Graph. Une fois ce graphe étendu crée, il est possible de réutiliser l'algortihme de Dijskstra codé à la question précèdente. 

1. Fonction `build_extended_graph':
   Le principe clé est le suivant : chaque nœud du graphe original u devient une paire (u, fatigue) dans le graphe étendu. Cela permet de modéliser le fait que passer par le même carrefour avec une fatigue différente n'est pas la même situation.

   Nous avons fait en sorte que la file queue pilote un parcours en largeur (BFS). En effet, le choix du BFS garantit qu'on explore les états par couches croissantes de fatigue, ce qui est cohérent avec la nature cumulative de la fatigue.

   Dernière remarque sur cette fonction : ce que nous avons appelé super_node constituent des nœuds d'arrivée canoniques. Comme la fatigue à l'arrivée est imprévisible (elle dépend du chemin emprunté), on crée un nœud "collecteur" (u, 0) vers lequel tous les états (u, *) convergent gratuitement (coût 0). Cela permet d'appeler shortest_path(start, (destination, 0)) sans connaître la fatigue finale.

2. On reprend la fonction `shortest_path(self, start, end)`: 
   

#### Compléxité de l'algorithme

