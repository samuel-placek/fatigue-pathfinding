import random

def game(network):
    """
    Jeu au tour par tour à deux joueurs sur le réseau.
    Le temps de trajet dépend de la fatigue accumulée au moment du départ.
    """
    # 1. Initialisation de la carte (CORRECTION ICI : _roads)
    villes = list(network._roads.keys())
    if len(villes) < 2:
        print("Erreur : Le réseau est trop petit.")
        return

    depart = random.choice(villes)
    arrivee = random.choice([v for v in villes if v != depart])

    print(f"\n{'='*50}")
    print(f"🏁 LA GRANDE COURSE : {depart} ➔ {arrivee} 🏁")
    print(f"Règle : Temps de trajet = Longueur de la route × Votre Fatigue")
    print(f"{'='*50}\n")

    # 2. Initialisation des joueurs
    joueurs = {
        "Joueur 1": {"position": depart, "temps": 0, "fatigue": 1, "fini": False, "chemin": [depart]},
        "Joueur 2": {"position": depart, "temps": 0, "fatigue": 1, "fini": False, "chemin": [depart]}
    }

    # 3. Boucle principale du jeu
    # Le jeu tourne tant qu'au moins un joueur n'a pas fini
    while not (joueurs["Joueur 1"]["fini"] and joueurs["Joueur 2"]["fini"]):
        
        for nom, data in joueurs.items():
            if data["fini"]:
                continue # Ce joueur a déjà gagné/perdu, on passe son tour

            print(f"\n{'*'*20} Tour de {nom} {'*'*20}")
            print(f"📍 Position : {data['position']} | ⏱️ Temps total : {data['temps']} | 🔋 Fatigue actuelle : {data['fatigue']}")
            
            # On récupère les routes possibles (CORRECTION ICI AUSSI : _roads)
            options = network._roads.get(data['position'], [])
            
            if not options:
                print(f"💀 Impasse ! {nom} est bloqué(e) et éliminé(e) de la course.")
                data["fini"] = True
                data["temps"] = float('inf') # Temps infini car disqualifié
                continue

            print("Routes disponibles :")
            # On précalcule et affiche les coûts pour aider le joueur
            for i, (voisin, longueur, f_route) in enumerate(options):
                # LA VRAIE FORMULE MATHÉMATIQUE ICI :
                temps_trajet = longueur * data['fatigue']
                nouvelle_fatigue = data['fatigue'] + f_route
                print(f"  {i+1}. Vers {voisin} (Prendra {temps_trajet}h, Nouvelle fatigue : {nouvelle_fatigue})")

            # 4. Saisie sécurisée
            choix_valide = False
            while not choix_valide:
                try:
                    choix = int(input(f"Choix (1-{len(options)}) : ")) - 1
                    if 0 <= choix < len(options):
                        choix_valide = True
                        
                        # 5. Mise à jour des statistiques
                        voisin_choisi, longueur_choisie, fatigue_choisie = options[choix]
                        
                        data['temps'] += (longueur_choisie * data['fatigue']) # Temps = L * F
                        data['fatigue'] += fatigue_choisie                    # Fatigue = F + f
                        data['position'] = voisin_choisi
                        data['chemin'].append(voisin_choisi)
                        
                        print(f"🚗 {nom} roule vers {voisin_choisi}...")

                        # Vérification de la victoire
                        if data['position'] == arrivee:
                            print(f"\n🎉 {nom} est arrivé(e) à destination en {data['temps']} heures !")
                            data['fini'] = True

                    else:
                        print("⚠️ Choix invalide, veuillez entrer un numéro correspondant à une route.")
                except ValueError:
                    print("⚠️ Veuillez entrer un chiffre.")

    # 6. Fin de partie et Résultats
    print(f"\n{'='*15} RÉSULTATS FINAUX {'='*15}")
    t1 = joueurs["Joueur 1"]["temps"]
    t2 = joueurs["Joueur 2"]["temps"]
    
    print(f"Joueur 1 : {t1} heures")
    print(f"Joueur 2 : {t2} heures")
    
    if t1 < t2:
        print("🏆 LE JOUEUR 1 REMPORTE LA COURSE !")
    elif t2 < t1:
        print("🏆 LE JOUEUR 2 REMPORTE LA COURSE !")
    else:
        print("🤝 ÉGALITÉ PARFAITE !")

import pygame
import sys
import math
import random

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
    # On calcule la taille de la grille (ex: 4x4 pour 16 sommets)
    colonnes = math.ceil(math.sqrt(nb))
    lignes = math.ceil(nb / colonnes)
    
    largeur_cellule = ZONE_CARTE_LARGEUR // colonnes
    hauteur_cellule = HAUTEUR // lignes
    
    # Mélanger les sommets pour un placement aléatoire sur la grille
    sommets_aleatoires = list(sommets)
    random.shuffle(sommets_aleatoires)
    
    index = 0
    for l in range(lignes):
        for c in range(colonnes):
            if index < nb:
                # Position centrale de la cellule + un petit décalage aléatoire (jitter)
                x = PANNEAU_LARGEUR + (c * largeur_cellule) + largeur_cellule // 2
                y = (l * hauteur_cellule) + hauteur_cellule // 2
                x += random.randint(-largeur_cellule//4, largeur_cellule//4)
                y += random.randint(-hauteur_cellule//4, hauteur_cellule//4)
                
                positions[sommets_aleatoires[index]] = (x, y)
                index += 1
    return positions

def dessiner_ui(ecran, joueurs, tour_actuel, message_fin):
    # Fond des panneaux
    pygame.draw.rect(ecran, (240, 240, 240), (0, 0, PANNEAU_LARGEUR, HAUTEUR))
    pygame.draw.rect(ecran, (240, 240, 240), (LARGEUR - PANNEAU_LARGEUR, 0, PANNEAU_LARGEUR, HAUTEUR))
    
    police = pygame.font.SysFont("Segoe UI", 25)
    
    for i, j in enumerate(joueurs):
        base_x = 20 if i == 0 else LARGEUR - PANNEAU_LARGEUR + 20
        couleur = COULEUR_J1 if i == 0 else COULEUR_J2
        
        # Titre Joueur
        img = police.render(f"JOUEUR {i+1}", True, couleur)
        ecran.blit(img, (base_x, 30))
        
        # Stats
        ecran.blit(police.render(f"Position: {j['pos']}", True, NOIR), (base_x, 80))
        ecran.blit(police.render(f"Temps: {j['temps']:.1f}h", True, NOIR), (base_x, 120))
        ecran.blit(police.render(f"Fatigue: {j['fatigue']}", True, NOIR), (base_x, 160))
        
        if tour_actuel == i and not j['fini'] and not message_fin:
            pygame.draw.circle(ecran, couleur, (base_x + 10, 220), 8)
            ecran.blit(police.render("À VOUS !", True, couleur), (base_x + 30, 205))

def jouer_course_abstraite(network):
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Network Race - Abstract Mode")
    
    villes = list(network._roads.keys())
    coords = generer_positions_abstraites(villes)
    
    depart = random.choice(villes)
    arrivee = random.choice([v for v in villes if v != depart])
    
    joueurs = [
        {"pos": depart, "temps": 0.0, "fatigue": 1, "fini": False, "chemin": [depart]},
        {"pos": depart, "temps": 0.0, "fatigue": 1, "fini": False, "chemin": [depart]}
    ]
    
    tour_actuel = 0
    message_fin = ""
    en_cours = True

    while en_cours:
        j_courant = joueurs[tour_actuel]
        options = network._roads.get(j_courant["pos"], [])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not message_fin:
                mx, my = pygame.mouse.get_pos()
                for voisin, longueur, f_route in options:
                    vx, vy = coords[voisin]
                    if math.hypot(mx - vx, my - vy) < 20:
                        # Calcul du temps selon ta formule
                        j_courant["temps"] += longueur * j_courant["fatigue"]
                        j_courant["fatigue"] += f_route
                        j_courant["pos"] = voisin
                        
                        if voisin == arrivee:
                            j_courant["fini"] = True
                        
                        # Changement de tour
                        tour_actuel = (tour_actuel + 1) % 2
                        if joueurs[tour_actuel]["fini"] and not all(p["fini"] for p in joueurs):
                             tour_actuel = (tour_actuel + 1) % 2

        # Détection fin de partie
        if all(p["fini"] for p in joueurs) and not message_fin:
            t1, t2 = joueurs[0]["temps"], joueurs[1]["temps"]
            if t1 < t2: message_fin = "JOUEUR 1 GAGNE !"
            elif t2 < t1: message_fin = "JOUEUR 2 GAGNE !"
            else: message_fin = "ÉGALITÉ !"

        # --- DESSIN ---
        ecran.fill(BLANC)
        
        # Dessin des routes
        for u, routes in network._roads.items():
            for v, L, F in routes:
                pygame.draw.line(ecran, GRIS, coords[u], coords[v], 2)
        
        # Dessin des sommets
        for v, pos in coords.items():
            color = (50, 50, 50)
            radius = 12
            if v == arrivee:
                color = (255, 215, 0)
                radius = 20
            elif v in [o[0] for o in options] and not j_courant["fini"]:
                color = (100, 200, 100) # Vert = cliquable
                
            pygame.draw.circle(ecran, color, pos, radius)
            # Nom du sommet
            fnt = pygame.font.SysFont("Arial", 15)
            ecran.blit(fnt.render(str(v), True, NOIR), (pos[0]-10, pos[1]+15))

        # Dessin des voitures (pions)
        for i, j in enumerate(joueurs):
            offset = -15 if i == 0 else 15
            px, py = coords[j["pos"]]
            pygame.draw.circle(ecran, COULEUR_J1 if i == 0 else COULEUR_J2, (px + offset, py), 10)

        dessiner_ui(ecran, joueurs, tour_actuel, message_fin)
        
        if message_fin:
            fnt_fin = pygame.font.SysFont("Arial", 50, bold=True)
            txt = fnt_fin.render(message_fin, True, (0, 150, 0))
            ecran.blit(txt, (LARGEUR//2 - txt.get_width()//2, 50))

        pygame.display.flip()

    pygame.quit()