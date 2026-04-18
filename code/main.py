from network import *
from graph import *
from game import *
import answers
import subprocess
import inspect
import ast

import sys 
from pathlib import Path

# Charger l'environnement du réseau

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))
NET_DIR = ROOT / "examples"


# Choix du mode de lancement

MODE = None
while MODE is None:
    try:
        MODE = int(input("Que voulez vous lancer ? tests (1), exécution de fonction (2) ou le jeu à deux joueurs (3) ? "))
        if MODE not in [1, 2, 3]:
            MODE = None
            print("Format incorrect, la réponse doit être entre 1 et 3\n")
    except Exception:
        print("Format incorrect, la réponse doit être un chiffre\n")


if MODE == 1: # Lancement des fonctions de test
    subprocess.run(["python", "-m", "unittest", "tests.test_network_from_file"], cwd=ROOT)

if MODE == 2 or MODE == 3: # Exécution de fonctions
    # Chargement d'un fichier network voulu par l'utilisateur
    network = None
    fichier_valide = False
    
    while not fichier_valide:
        nom_fichier = input("\nVeuillez entrer le nom du fichier réseau (ex: 'small.txt') : ")
        chemin_fichier = NET_DIR / nom_fichier

        if chemin_fichier.is_file():
            network = Network.from_file(str(chemin_fichier))
            fichier_valide = True 
        else:
            print("Erreur : Fichier introuvable.\n")

    if MODE == 2:
        # Exécution d'une fonction
        fc = input("\nQuelle fonction voulez-vous lancer ? ")

        while not (hasattr(answers, fc) and callable(getattr(answers, fc))):
            print("Cette fonction n'existe pas. Veuillez réessayer.")
            fc = input("\nQuelle fonction voulez-vous lancer ? ")

        fonction_a_lancer = getattr(answers, fc)
        signature = inspect.signature(fonction_a_lancer)

        arguments_fournis = {}

        # Récupération des arguments à fournir
        if signature.parameters:
            for nom_param, param in signature.parameters.items():
                # On sait déjà qu'on va travailler avec la variable network : inutile de re demander
                if nom_param == "network":
                    arguments_fournis["network"] = network
                    continue

                a_un_defaut = param.default != inspect.Parameter.empty

                if a_un_defaut:
                    message = f" -> Valeur pour '{nom_param}' (Entrée pour garder le défaut) : "
                else:
                    message = f" -> Entrez la valeur obligatoire pour '{nom_param}' : "

                saisie = input(message)

                # Gestion des valeurs par défaut
                if saisie.strip() == "" and a_un_defaut:
                    continue

                try:
                    valeur_convertie = ast.literal_eval(saisie)
                except (ValueError, SyntaxError):
                    valeur_convertie = saisie
                arguments_fournis[nom_param] = valeur_convertie

        # On exécute la fonction avec les arguements voulus 
        resultat = fonction_a_lancer(**arguments_fournis)
        print(f"\nRésultat renvoyé par la fonction : {resultat}")

    else:
        jouer_course_abstraite(network)