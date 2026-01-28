# Emmanuelle Chocron - Samuel Placek
Projet de Programmation accéléré de 1A 


## Partie 1 - Chemin de temps minimal

### 1.1 - Cas particulier sans fatigue 

On considère dans ce premier paragraphe un network où pour toute arête e, f(e)=0. Il s'agit alors d'un simple graphe pondéré.
L'idée principale est donc d'utilisé un algortihme de plus court chemin classique : l'algorithme de Dijkstra. 
Pour cela, on implémenté d'abord dans la classe Network une méthode build_simple_graphe afin de construire le graphe à partir d'un network.
