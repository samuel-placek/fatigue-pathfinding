import random
import pygame
import sys
import math

def jeu_terminal(network):
    """
    Jeu au tour par tour à deux joueurs sur le réseau.
    Le temps de trajet dépend de la fatigue accumulée au moment du départ.
    """
    # Initialisation de la carte
    villes = list(network._roads.keys())
    if len(villes) < 2:
        print("Erreur : Le réseau est trop petit.")
        return

    depart = random.choice(villes)
    arrivee = random.choice([v for v in villes if v != depart])

    print(f"\n{'='*50}")
    print(f"Objectif : aller de {depart} à {arrivee} ")
    print(f"{'='*50}\n")

    # Initialisation des joueurs
    joueurs = {
        "Joueur 1": {"position": depart, "temps": 0, "fatigue": 1, "fini": False, "chemin": [depart]},
        "Joueur 2": {"position": depart, "temps": 0, "fatigue": 1, "fini": False, "chemin": [depart]}
    }

    # Le jeu tourne tant qu'au moins un joueur n'a pas fini
    while not (joueurs["Joueur 1"]["fini"] and joueurs["Joueur 2"]["fini"]):
        
        for nom, data in joueurs.items():
            if data["fini"]:
                continue # Ce joueur a déjà gagné/perdu, on passe son tour

            print(f"\n{'*'*20} Tour de {nom} {'*'*20}")
            print(f"Position : {data['position']} | Temps total : {data['temps']} | Fatigue actuelle : {data['fatigue']}")
            
            # On récupère les routes possibles
            options = network._roads.get(data['position'], [])
            
            if not options:
                print(f"Impasse ! {nom} est éliminé")
                data["fini"] = True
                data["temps"] = float('inf') # Temps infini car disqualifié
                continue

            print("Routes disponibles :")
            for i, (voisin, longueur, f_route) in enumerate(options):
                temps_trajet = longueur * data['fatigue']
                nouvelle_fatigue = data['fatigue'] + f_route
                print(f"  {i+1}. Vers {voisin} (temps : {temps_trajet}min, fatigue du chemin : {nouvelle_fatigue})")

            choix_valide = False
            while not choix_valide:
                try:
                    choix = int(input(f"Choix (1-{len(options)}) : ")) - 1
                    if 0 <= choix < len(options):
                        choix_valide = True
                        voisin_choisi, longueur_choisie, fatigue_choisie = options[choix]
                        
                        data['temps'] += (longueur_choisie * data['fatigue'])
                        data['fatigue'] += fatigue_choisie
                        data['position'] = voisin_choisi
                        data['chemin'].append(voisin_choisi)

                        if data['position'] == arrivee:
                            print(f"\n{nom} est arrivé à destination en {data['temps']} minutes !")
                            data['fini'] = True

                    else:
                        print("Choix invalide, veuillez entrer un numéro correspondant à une route.")
                except ValueError:
                    print("Veuillez entrer un chiffre.")

    # 6. Fin de partie et Résultats
    print(f"\n{'='*15} RÉSULTATS {'='*15}")
    t1 = joueurs["Joueur 1"]["temps"]
    t2 = joueurs["Joueur 2"]["temps"]
    
    print(f"Joueur 1 : {t1} minutes")
    print(f"Joueur 2 : {t2} minutes")
    
    if t1 < t2:
        print("Le joueur 1 gagne !")
    elif t2 < t1:
        print("Le joueur 1 gagne !")
    else:
        print("Égalité")


# --- CONFIGURATION ---
LARGEUR, HAUTEUR = 1200, 800
ZONE_CARTE_LARGEUR = 600
PANNEAU_LARGEUR = 300

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
COULEUR_J1 = (0, 100, 250)
COULEUR_J2 = (250, 50, 50)

def generer_positions_abstraites(sommets):
    """
    Répartit les sommets sur une grille pour qu'ils soient bien distribués.
    """
    positions = {}
    nb = len(sommets)

    # On "quadrille" pour avoir une réparition propre des sommets
    colonnes = math.ceil(math.sqrt(nb))
    lignes = math.ceil(nb / colonnes) if colonnes > 0 else 1
    
    largeur_cellule = ZONE_CARTE_LARGEUR // colonnes if colonnes > 0 else ZONE_CARTE_LARGEUR
    hauteur_cellule = HAUTEUR // lignes if lignes > 0 else HAUTEUR
    
    # On répartit aléatoirement les sommets
    sommets_aleatoires = list(sommets)
    random.shuffle(sommets_aleatoires)
    
    index = 0
    for l in range(lignes):
        for c in range(colonnes):
            if index < nb:
                x = PANNEAU_LARGEUR + (c * largeur_cellule) + largeur_cellule // 2
                y = (l * hauteur_cellule) + hauteur_cellule // 2

                # Avoir une répartition un peu plus "aléatoire" et pas rigide
                x += random.randint(-largeur_cellule//4, largeur_cellule//4)
                y += random.randint(-hauteur_cellule//4, hauteur_cellule//4)
                
                positions[sommets_aleatoires[index]] = (x, y)
                index += 1
    return positions

def dessiner_ui(ecran, joueurs, tour_actuel, message_fin):
    pygame.draw.rect(ecran, (240, 240, 240), (0, 0, PANNEAU_LARGEUR, HAUTEUR))
    pygame.draw.rect(ecran, (240, 240, 240), (LARGEUR - PANNEAU_LARGEUR, 0, PANNEAU_LARGEUR, HAUTEUR))
    
    # On veut travailler avec la police "Segoe UI" mais si on la trouve pas on prend celle par défaut
    try:
        police = pygame.font.SysFont("Segoe UI", 25)
    except:
        police = pygame.font.Font(None, 30)
    
    for i, j in enumerate(joueurs):
        # Se placer à gauche de l'écran pour la joueur 1 et à droit pour le joueur 2
        base_x = 20 if i == 0 else LARGEUR - PANNEAU_LARGEUR + 20
        couleur = COULEUR_J1 if i == 0 else COULEUR_J2
        
        img = police.render(f"JOUEUR {i+1}", True, couleur)
        ecran.blit(img, (base_x, 30))
        
        ecran.blit(police.render(f"Position: {j['pos']}", True, NOIR), (base_x, 80))
        ecran.blit(police.render(f"Temps: {j['temps']:.1f}min", True, NOIR), (base_x, 120))
        ecran.blit(police.render(f"Fatigue: {j['fatigue']}", True, NOIR), (base_x, 160))
        
        if tour_actuel == i and not j['fini'] and not message_fin:
            pygame.draw.circle(ecran, couleur, (base_x + 10, 220), 8)
            ecran.blit(police.render("À VOUS !", True, couleur), (base_x + 30, 205))

def jeu_pygame(network):
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Fortnite")
    
    villes = list(network._roads.keys())
    if len(villes) < 2:
        pygame.quit()
        return

    # On place les villes et on choisit un point de départ et d'arrivée
    coords = generer_positions_abstraites(villes)
    depart = random.choice(villes)
    arrivee = random.choice([v for v in villes if v != depart])
    
    joueurs = [
        {"pos": depart, "temps": 0.0, "fatigue": 1, "fini": False, "chemin": [depart]},
        {"pos": depart, "temps": 0.0, "fatigue": 1, "fini": False, "chemin": [depart]}
    ]
    
    tour_actuel = 0 # 0 = J1 / 1 = J2
    message_fin = ""
    en_cours = True

    while en_cours:
        j_courant = joueurs[tour_actuel]
        options = network._roads.get(j_courant["pos"], []) # Récupère les chemins possibles
        
        for event in pygame.event.get(): # On regarde chaque action de l'utilisateur 
            if event.type == pygame.QUIT:
                en_cours = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not message_fin: # S'il y a un clique 
                mx, my = pygame.mouse.get_pos()
                
                for element in options:
                    # Si c'est un graph (network sans fatigue) on prend une fatigue de 1
                    if len(element) == 3:
                        voisin, longueur, f_route = element
                    else:
                        voisin, longueur = element[0], element[1]
                        f_route = 1
                        
                    vx, vy = coords[voisin]
                    distance_clic = math.hypot(mx - vx, my - vy)
                    
                    if distance_clic <= 40: # On regarde si l'utilsateur à cliqué sur le sommet
                        j_courant["temps"] += longueur * j_courant["fatigue"]
                        j_courant["fatigue"] += f_route
                        j_courant["pos"] = voisin
                        
                        if voisin == arrivee:
                            j_courant["fini"] = True
                        
                        tour_actuel = (tour_actuel + 1) % 2 # On passe au joueur suivant
                        if joueurs[tour_actuel]["fini"] and not all(p["fini"] for p in joueurs):
                             tour_actuel = (tour_actuel + 1) % 2
                             
                        break

        if all(p["fini"] for p in joueurs) and not message_fin: # Vérification de fin de partie
            t1, t2 = joueurs[0]["temps"], joueurs[1]["temps"]
            if t1 < t2: message_fin = "JOUEUR 1 GAGNE !"
            elif t2 < t1: message_fin = "JOUEUR 2 GAGNE !"
            else: message_fin = "ÉGALITÉ !"

        ecran.fill(BLANC) # Ne pas superposer chaque dessin
        
        # Dessiner les liaisons entre deux sommets reliés
        for u, routes in network._roads.items():
            for element in routes:
                v = element[0]
                pygame.draw.line(ecran, GRIS, coords[u], coords[v], 2)
        
        voisins_possibles = [o[0] for o in options] if not j_courant["fini"] else []
        
        for v, pos in coords.items():
            color = (50, 50, 50)
            radius = 12
            
            est_cliquable = v in voisins_possibles
            
            if v == arrivee:
                if est_cliquable:
                    color = (0, 220, 0) # Vert vif : Coup gagnant possible !
                    radius = 25
                else:
                    color = (255, 215, 0) # Or : Arrivée normale
                    radius = 20
            elif est_cliquable:
                color = (100, 200, 100) # Vert clair : Option cliquable
                radius = 16
                
            pygame.draw.circle(ecran, color, pos, radius)
            
            try:
                fnt = pygame.font.SysFont("Arial", 15)
            except:
                fnt = pygame.font.Font(None, 20)
            ecran.blit(fnt.render(str(v), True, NOIR), (pos[0]-10, pos[1]+15))

        # Représenter les joueur sans qu'il ne se superposent
        for i, j in enumerate(joueurs):
            offset = -15 if i == 0 else 15
            px, py = coords[j["pos"]]
            pygame.draw.circle(ecran, COULEUR_J1 if i == 0 else COULEUR_J2, (px + offset, py), 10)

        dessiner_ui(ecran, joueurs, tour_actuel, message_fin)

        # On affiche le message de fin à la fin de la partie 
        if message_fin:
            try:
                fnt_fin = pygame.font.SysFont("Arial", 50, bold=True)
            except:
                fnt_fin = pygame.font.Font(None, 60)
            txt = fnt_fin.render(message_fin, True, (0, 150, 0))
            ecran.blit(txt, (LARGEUR//2 - txt.get_width()//2, 50))

        pygame.display.flip()

    pygame.quit()