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

def check_boat (new_boat, boats):
    # TODO: a coder
    # check dans grid
    # check pas de croisements des bateaux
    # longueurs boats 2.3.4
    return True

def boat_coordinates (boat):
    (ligne, colonne, longueur, horizontal) = boat
    coordinates = []
    for i in range(longueur):
        if horizontal:
            coordinates.append((ligne, colonne+i))
        else:
            coordinates.append((ligne+i, colonne))
    return coordinates

def in_boat (boat, ligne, colonne):
    list_coord = boat_coordinates(boat) 
    for coord in list_coord:
        (coord_ligne, coord_colonne) = coord
        if (coord_ligne == ligne) and (coord_colonne == colonne):
            return True
    return False
    

### bateaux users

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

### bateaux computer
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

#
user_hits = 0
computer_hits = 0

try:
    
    # shoot phase
    while (user_hits < 9) and (computer_hits < 9):
        
        # User joue
        already_played = True
        while already_played == True:
            click = affichage.choose_shoot()
            print(click)
            if computer_grid [ click[0]-1 ] [ click[1]-1 ] == "X":
                already_played = True
                print("already played")
            else: 
                already_played = False
        
        computer_grid [ click[0]-1 ] [ click[1]-1 ] = "X"
        print("hop 1")
        hit = False
        for boat in computer_boats:
            hit = in_boat(boat, click[0], click[1]) 
            if hit == True:
                print("Touché")   
                user_hits = user_hits + 1
                coordinates = boat_coordinates(boat)
                sinked = True
                for coord in coordinates:
                    if computer_grid [coord[0]-1][coord[1]-1] == 'O':
                        sinked = False
                if sinked == True:
                    print("Touché coulé")   
                    affichage.draw_boat(affichage.COMPUTER, *boat)
                    #TODO : affiché hit rouge sur bateau coulé
                    for coord in coordinates:
                        affichage.draw_shoot(affichage.COMPUTER, coord[0], coord[1], True)
                break
        print(f"affichage shoot user en {click}")
        affichage.draw_shoot(affichage.COMPUTER, click[0], click[1], hit)
        
        # computer joue
        time.sleep(1)
        already_played = True
        while already_played == True:
            click = (random.randint(1, 10) , random.randint(1, 10))
            print(click)
            if user_grid [ click[0]-1 ] [ click[1]-1 ] == "X":
                already_played = True
            else: 
                already_played = False
        
        user_grid [ click[0]-1 ] [ click[1]-1 ] = "X"
        
        hit = False
        for boat in user_boats:
            hit = in_boat(boat, click[0], click[1]) 
            if hit == True:
                print("Touché")  
                computer_hits = computer_hits  + 1
                coordinates = boat_coordinates(boat)
                sinked = True
                for coord in coordinates:
                    if user_grid [coord[0]-1][coord[1]-1] == 'O':
                        sinked = False
                if sinked == True:
                    print("Touché coulé")   
    
                break
        print(f"affichage shoot computer en {click}")
        affichage.draw_shoot(affichage.USER, click[0], click[1], hit)
        
        
        
        # TODO: verifie si user gagne
        
        # TODO computer joue
        
    if user_hits == 9:
        print("USER GAGNE !!!!!")
    if computer_hits == 9:
        print("COMPUTER GAGNE !!!!!")
    
    affichage.end()
    
except Exception as e:
    affichage.end()
    raise e
    



