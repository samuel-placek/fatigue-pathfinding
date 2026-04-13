from network import *
from graph import *
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

MODE = int(input("Que voulez vous lancer ? tests (1) ou exécution de fonction (2) ? "))

if MODE == 1: # Lancement des fonctions de test
    subprocess.run(["python", "-m", "unittest", "tests.test_network_from_file"], cwd=ROOT)

if MODE == 2: # Exécution de fonctions
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

    # Exécution d'une fonction
    fc = input("\nQuelle fonction voulez-vous lancer ? ")

    while not (hasattr(answers, fc) and callable(getattr(answers, fc))):
        print("Cette fonction n'existe pas. Veuillez réessayer.")
        fc = input("\nQuelle fonction voulez-vous lancer ? ")

    fonction_a_lancer = getattr(answers, fc)
    signature = inspect.signature(fonction_a_lancer)

    arguments_fournis = {}

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

    resultat = fonction_a_lancer(**arguments_fournis)
    print(f"\nRésultat renvoyé par la fonction : {resultat}")