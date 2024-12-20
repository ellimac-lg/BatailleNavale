#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 15:54:46 2024

@author: clg
"""
import time
import affichage
import random

DEBUG = False

MSG_DS_LEAU =  ["dans l'eau...",
                "ah ça pour faire des vagues...",
                "mais ya rien là !",
                "peux mieux faire",
                "plouf...",
                "un coup pour rien",
                "Splash stratégique !",
                "un tir à la mer !",
                "bof...",
                "Eau mon Dieu",
                "un plan qui tombe à l'eau",
                "Eau rage ! Eau désespoir !",
                "dommaaage...",
                "presque mais.. non",
                "des ptits ronds dans l'eau...",
                "faudrait apprendre à viser..",
                "raaaaté !",
                "applique toi un peu..",
                "à part faire peur aux poissons..",
                "mon petit neveu ferait mieux..",
                "marin d'eau douce va !",
                "faudrait voir à gagner en précision.."]

### init

# grille du joueur
user_grid = None
# grille du computer
computer_grid = None
# bateaux du joueur
user_boats = None
# bateaux du computer
computer_boats = None

def init():
    # grille du joueur
    global user_grid
    user_grid = [["O"] * 10 for _ in range(10)]
    # grille du computer
    global computer_grid
    computer_grid = [["O"] * 10 for _ in range(10)]
    # bateaux du joueur
    global user_boats
    user_boats = []
    # bateaux du computer
    global computer_boats
    computer_boats = []
    
    affichage.init()

def boat_coordinates (boat):
    "retourne un tableau de coordonnéées du bateau"
    (ligne, colonne, longueur, horizontal) = boat
    coordinates = []
    for i in range(longueur):
        if horizontal:
            coordinates.append((ligne, colonne+i))
        else:
            coordinates.append((ligne+i, colonne))
    return coordinates

def in_boat (boat, ligne, colonne):
    "retourne True si les coordonés sont dans le bateau"
    list_coord = boat_coordinates(boat) 
    for coord in list_coord:
        (coord_ligne, coord_colonne) = coord
        if (coord_ligne == ligne) and (coord_colonne == colonne):
            return True
    return False

def check_boat (new_boat, boats):
    "vérifie qu'un bateaux ne se chevauchent pas les autres et que sa longueur n'est pas déjà utilisée"
    # check pas de croisements des bateaux
    new_boat_coords = boat_coordinates(new_boat)
    for each_boat in boats:
        each_boat_coords = boat_coordinates(each_boat)
        for nbcoord in new_boat_coords:
            for ebcoord in each_boat_coords:
                if nbcoord == ebcoord:
                    return False
    
    # check que le bateau ne dépasse pas de la grille
    (ligne, colonne, longueur, horizontal) = new_boat
    if horizontal:
        if colonne -1 + longueur > 10: # dépassement à droite
            return False
    else:
        if ligne -1 + longueur > 10: # dépassement en bas
            return False
        
    # si tout s'est bien passé jusque là le bateau est valide
    return True

def random_boat(longueur):
    "creation aleatoire d'un bateau d'une certaine longueur"
    ligne = random.randint(1, 10)
    colonne = random.randint(1, 10)
    horizontal = (random.randint(0, 1) == 1)
    return (ligne, colonne, longueur, horizontal)
 
        
try:
    while True:
        
        init()
        
        ################################
        ### selection bateaux computer #
        ################################
        
        # creation aleatoire d'un bateau de longueur 4
        check = False
        # tant que le bateau créé n'est pas valide on re-essaie
        while check == False:
            boat4 = random_boat(4) 
            check = check_boat(boat4, computer_boats)
            if check:
                # si valide on ajoute le bateau dans la liste
                computer_boats.append(boat4)
                
        # creation aleatoire d'un bateau de longueur 3
        check = False
        # tant que le bateau créé n'est pas valide on re-essaie
        while check == False:
            boat3 = random_boat(3)
            check = check_boat(boat3, computer_boats)
            if check:
                # si valide on ajoute le bateau dans la liste
                computer_boats.append(boat3)
                
        # creation aleatoire d'un bateau de longueur 2
        check = False
        # tant que le bateau créé n'est pas valide on re-essaie
        while check == False:  
            boat2 = random_boat(2)
            check = check_boat(boat2, computer_boats)
            if check:
                # si valide on ajoute le bateau dans la liste
                computer_boats.append(boat2)
        
        # on ne doit pas afficher les bateaux du computer
        # mais on le fait quand même pour debugguer
        if DEBUG:
            affichage.draw_boat(affichage.COMPUTER, *boat4)
            affichage.draw_boat(affichage.COMPUTER, *boat3)
            affichage.draw_boat(affichage.COMPUTER, *boat2)
            
        #############################
        ### selection bateaux users #
        #############################
        
        affichage.set_text('Bienvenue, choisis et place tes navires ')
        
        l2=True
        l3=True
        l4=True
        
        while len(user_boats)<3 :
            # demande au joueur de placer un bateu sur la grille
            boat = affichage.choose_boat(l2, l3, l4)
            print(boat)
            # vérifie si le bateau est valide
            check = check_boat (boat, user_boats)
            if check: # bateau valide
                # il ne faut plus selectionner de bateau de cette longueur
                if boat[2] == 2:
                    l2 = False
                if boat[2] == 3:
                    l3 = False
                if boat[2] == 4:
                    l4 = False
                user_boats.append(boat) # ajout dans la liste
                affichage.draw_boat(affichage.USER, *boat) # affichage
        
        ################################
        ### La partie peut commencer   #
        ################################
        
        # nombre de touchés
        user_hits = 0
        computer_hits = 0
        
        affichage.set_text('Tire sur la grille de droite ')
        
        # shoot phase
        while (user_hits < 9) and (computer_hits < 9):
            
            ###############
            ### User joue #
            ###############
            print("### User joue ###")
            already_played = True
            # tant que ce n'est pas un nouveau coup...
            while already_played:
                # récupère le coup du user
                coup = affichage.choose_shoot()
                print(coup)
                # vérifie si ce coup a déjà été joué
                if computer_grid [ coup[0]-1 ] [ coup[1]-1 ] == "X":
                    already_played = True
                    affichage.set_text('Tu as déjà tiré ici... ')
                else: 
                    already_played = False
            # enregistre le coup dans la grille du computer
            computer_grid [ coup[0]-1 ] [ coup[1]-1 ] = "X"
            
            # vérifie si touché et coulé
            hit = False
            for boat in computer_boats:
                # vérifie si bateau touché
                hit = in_boat(boat, coup[0], coup[1]) 
                if hit: # touché
                    affichage.set_text('Touché !') 
                    user_hits = user_hits + 1 # arrivé à 9 c'est gagné
                    # vérifie si coulé
                    coordinates = boat_coordinates(boat)
                    sinked = True
                    for coord in coordinates:
                        if computer_grid [coord[0]-1][coord[1]-1] == 'O':
                            sinked = False
                    if sinked:
                        affichage.set_text('Touché Coulé ! ') 
                        # si le bateau est coulé on l 'affiche
                        affichage.draw_boat(affichage.COMPUTER, *boat)
                        # il faut réafficher les points rouges sur le bateau coulé
                        for coord in coordinates:
                            affichage.draw_shoot(affichage.COMPUTER, coord[0], coord[1], True)
                    break
                else: affichage.set_text(MSG_DS_LEAU[random.randint(0, len(MSG_DS_LEAU)-1)])
            # afficher le coup sur la grille du computer (en rouge si c'est un hit)
            affichage.draw_shoot(affichage.COMPUTER, coup[0], coup[1], hit)
            
            time.sleep(1) # petit temps d'attente
            
            #################
            # computer joue #
            #################
            print("### Computer joue ###")
            already_played = True
            # tant que ce n'est pas un nouveau coup...
            while already_played:
                # le computer joue qu hasard coup 
                coup = (random.randint(1, 10) , random.randint(1, 10))
                print(coup)
                # vérifie si ce coup a déjà été joué
                if user_grid [ coup[0]-1 ] [ coup[1]-1 ] == "X":
                    already_played = True
                else: 
                    already_played = False
            # enregistre le coup dans la grille du user
            user_grid [ coup[0]-1 ] [ coup[1]-1 ] = "X"
            
            # vérifie si touché et coulé
            hit = False
            for boat in user_boats:
                # vérifie si bateau touché
                hit = in_boat(boat, coup[0], coup[1]) 
                if hit:
                    affichage.set_text('Aïe ! ') 
                    computer_hits = computer_hits  + 1 # arrivé à 9 c'est gagné
                    # vérifie si coulé
                    coordinates = boat_coordinates(boat)
                    sinked = True
                    for coord in coordinates:
                        if user_grid [coord[0]-1][coord[1]-1] == 'O':
                            sinked = False
                    if sinked:
                        affichage.set_text('Aïe Aïe Aïe !! ') 
                    break
            # afficher le coup sur la grille du computer (en rouge si c'est un hit)
            affichage.draw_shoot(affichage.USER, coup[0], coup[1], hit)
            
            
        # vérifie qui a gagné
        if user_hits == 9:
            affichage.set_text('Félicitations ! Tu as gagné ! ')
        if computer_hits == 9:
            affichage.set_text('Dommage, tu as perdu ... ')
        affichage.display()
        
        # bouton reset
        affichage.reset()
  
except:
    # fermer pygame en cas d'exception
    affichage.end()
    raise




