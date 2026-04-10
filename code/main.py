from network import *
from graph import *
import answers
import subprocess
import inspect
import ast

import sys 
from pathlib import Path

# Charger le réseau

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))
NET_DIR = ROOT / "examples"

network_file = "/home/onyxia/work/Emmanuelle-Chocron---Samuel-Placek/examples/small.txt"
network = Network.from_file(NET_DIR / "small.txt")

'''
A enelever avant le rendu final !!!!
print(answers.simple_case(network, "lozere", "saclay"))
'''

print(answers.algo_a_star(network, "lozere", "saclay"))




# Choix du mode de lancement

#MODE = int(input("Que voulez vous lancer ? tests (1) ou exécution de fonction (2) ? "))

if MODE == 1: # Lancement des fonctions de test
    subprocess.run(["python", "-m", "unittest", "tests.test_network_from_file"], cwd=ROOT)

if MODE == 2: # Exécution de fonctions
    fc = input("Quelle fonction voulez vous lancer ? ")

    while not (hasattr(answers, fc) and callable(getattr(answers, fc))): # On regarde si la fonction existe
        print("Cette fonction n'existe pas. Veuillez réessayer.")
        fc = input("Quelle fonction voulez vous lancer ? ")
    
    fonction_a_lancer = getattr(answers, fc)
    signature = inspect.signature(fonction_a_lancer)
    parametres_attendus = signature.parameters
    arguments_fournis = {}
    variables_disponibles = {"network": network}

    if parametres_attendus: # On demande à l'utilisateur de choisir les arguments pour lancer la fonction
        for nom_param, param in signature.parameters.items():
            
            # On vérifie si la fonction a déjà une valeur par défaut pour cet argument
            a_un_defaut = param.default != inspect.Parameter.empty
            
            if a_un_defaut:
                message = f"  -> Valeur pour '{nom_param}' (Appuyez sur Entrée pour garder le défaut) : "
            else:
                message = f"  -> Entrez la valeur obligatoire pour '{nom_param}' : "
                
            saisie = input(message)
            
            # Si l'utilisateur n'a rien tapé ET qu'il y a un paramètre par défaut, on l'ignore !
            if saisie.strip() == "" and a_un_defaut:
                continue
            
            # Si l'utilisateur a tapé une variable connue dans notre dictionnaire
            if saisie in variables_disponibles:
                valeur_convertie = variables_disponibles[saisie]
            else:
                try:
                    valeur_convertie = ast.literal_eval(saisie)
                except (ValueError, SyntaxError):
                    valeur_convertie = saisie
                    
            arguments_fournis[nom_param] = valeur_convertie

    resultat = fonction_a_lancer(**arguments_fournis)
    print(f"\n Résultat renvoyé par la fonction : {resultat}")
