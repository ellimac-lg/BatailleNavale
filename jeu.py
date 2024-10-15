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

### init

# grille du joueur
user_grid = [["O"] * 10 for _ in range(10)]
# grille du computer
computer_grid = [["O"] * 10 for _ in range(10)]
# bateaux du joueur
user_boats = []
# bateaux du computer
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
    # TODO: a coder
    # check dans grid
    # check pas de croisements des bateaux
    # longueurs boats 2.3.4
    return True

    
#############################
### selection bateaux users #
#############################

while len(user_boats)<3 :
    # demande au joueur de placer un bateu sur la grille
    boat = affichage.choose_boat()
    print(boat)
    # vérifie si le bateau est valide
    check = check_boat (boat, user_boats)
    if check: # bateau valide
        user_boats.append(boat) # ajout dans la liste
        affichage.draw_boat(affichage.USER, *boat) # affichage
    #time.sleep(1)

################################
### selection bateaux computer #
################################
# TODO : randomiser

boat1 = (5,4,3,True)
computer_boats.append(boat1)
if DEBUG:
    affichage.draw_boat(affichage.COMPUTER, *boat1)
#time.sleep(1)
boat2 = (2,1,4,True)
computer_boats.append(boat2)
if DEBUG:
    affichage.draw_boat(affichage.COMPUTER, *boat2)
#time.sleep(1)
boat3 = (7,8,2,False)
computer_boats.append(boat3)
if DEBUG:
    affichage.draw_boat(affichage.COMPUTER, *boat3)
#time.sleep(1)

# nombre de touchés
user_hits = 0
computer_hits = 0

try:
    
    # shoot phase
    while (user_hits < 9) and (computer_hits < 9):
        
        #################
        ### User joue ###
        #################
        print("### User joue ###")
        already_played = True
        # tant que ce n'est pas un nouveau coup...
        while already_played == True:
            # récupère le coup du user
            coup = affichage.choose_shoot()
            print(coup)
            # vérifie si ce coup a déjà été joué
            if computer_grid [ coup[0]-1 ] [ coup[1]-1 ] == "X":
                already_played = True
                print("already played")
            else: 
                already_played = False
        # enregistre le coup dans la grille du computer
        computer_grid [ coup[0]-1 ] [ coup[1]-1 ] = "X"
        
        # vérifie si touché et coulé
        hit = False
        for boat in computer_boats:
            # vérifie si bateau touché
            hit = in_boat(boat, coup[0], coup[1]) 
            if hit == True: # touché
                print("Touché")   
                user_hits = user_hits + 1 # arrivé à 9 c'est gagné
                # vérifie si coulé
                coordinates = boat_coordinates(boat)
                sinked = True
                for coord in coordinates:
                    if computer_grid [coord[0]-1][coord[1]-1] == 'O':
                        sinked = False
                if sinked == True:
                    print("Coulé")   
                    # si le bateau est coulé on l 'affiche
                    affichage.draw_boat(affichage.COMPUTER, *boat)
                    # il faut réafficher les points rouges sur le bateau coulé
                    for coord in coordinates:
                        affichage.draw_shoot(affichage.COMPUTER, coord[0], coord[1], True)
                break
        # afficher le coup sur la grille du computer (en rouge si c'est un hit)
        affichage.draw_shoot(affichage.COMPUTER, coup[0], coup[1], hit)
        
        time.sleep(1) # petit temps d'attente
        
        #################
        # computer joue #
        #################
        print("### Computer joue ###")
        already_played = True
        # tant que ce n'est pas un nouveau coup...
        while already_played == True:
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
            if hit == True:
                print("Touché")  
                computer_hits = computer_hits  + 1 # arrivé à 9 c'est gagné
                # vérifie si coulé
                coordinates = boat_coordinates(boat)
                sinked = True
                for coord in coordinates:
                    if user_grid [coord[0]-1][coord[1]-1] == 'O':
                        sinked = False
                if sinked == True:
                    print("Coulé")   
                break
        # afficher le coup sur la grille du computer (en rouge si c'est un hit)
        affichage.draw_shoot(affichage.USER, coup[0], coup[1], hit)
        
        
    # vérifie qui a gagné
    if user_hits == 9:
        print("USER GAGNE !!!!!")
    if computer_hits == 9:
        print("COMPUTER GAGNE !!!!!")
    # TODO afficher le gagant à l'écran
    
    # TODO: Reset button
    
    affichage.end()
    
except:
    # fermer pygame en cas d'exception
    affichage.end()
    raise 
    



