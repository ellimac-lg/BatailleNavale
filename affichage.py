#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 18:42:17 2024

@author: clg
"""

import pygame
import sys

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
BLOCK_SIZE = 40

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREY = (120,120,120)

USER = "user"
COMPUTER = "COMPUTER"

pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

#surface de fenetre/taille
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# # creation image
# button = pygame.Surface((10, 5))
# button.fill('green')
# # position de l'image
# button_rect = button.get_rect()   #pygame.Rect(30, 50, 10, 5)
# button_rect.x = 50


grid1 = None
grid2 = None
grid1_rect = None
grid2_rect = None

def get_grid(player):
    if player == USER: return grid1
    if player == COMPUTER: return grid2
    end()

def create_grid():
    " creation d une grille vierge"
    
    grid_size = BLOCK_SIZE*11
    # surfqce grille
    grid = pygame.Surface((grid_size, grid_size))
    
    #tracé de la grille
    for x in range(0, grid_size, BLOCK_SIZE):
        for y in range(0, grid_size, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(grid, WHITE, rect, 2)
    
    # ecriture des coordonnées, ecriture ds grid
    font = pygame.font.SysFont(None, BLOCK_SIZE) # police d'écriture
    for i in range(1,11):
        
        #1.2.3...
        n=str(i)
        texte_surf = font.render( n , True, WHITE) # surface texte
        # rect pour plqcer le texte dqns lq grille
        texte_rect = texte_surf.get_rect()
        texte_rect.centerx = BLOCK_SIZE/2 + BLOCK_SIZE*i
        texte_rect.centery = BLOCK_SIZE/2 
        # ecriture sur lq grille
        grid.blit(texte_surf, texte_rect)
        
        #A.B.C...
        n= chr(ord('A') + i-1 ) #utilisation code ascii
        texte_surf = font.render( n , True, WHITE)
        texte_rect = texte_surf.get_rect()
        texte_rect.centerx = BLOCK_SIZE/2 
        texte_rect.centery = BLOCK_SIZE/2 + BLOCK_SIZE*i 
        grid.blit(texte_surf, texte_rect)
    
    return grid

def draw_shoot(player, ligne, colonne, hit=False):
    "draw a blue circle in grid at the coordinates , ligne, colonne"
    
    grid = get_grid(player)
    # Defining coordinates of the centre of the circle
    center = (BLOCK_SIZE/2 + BLOCK_SIZE * colonne, BLOCK_SIZE/2 + BLOCK_SIZE * ligne)
    radius = BLOCK_SIZE/3
    
    # bleu pour les coups dans l'eau, rouge pour les touchés
    if hit == False:
        color = BLUE
    else:
        color = RED
    # dessine le cercle sur la grille
    pygame.draw.circle(grid, color, center, radius)
    display()
    

def draw_boat(player, ligne, colonne, longueur, horizontal=True):
    "dessine un bateau dans la grille"
    
    grid = get_grid(player)
    # definit les coordonnées du coin en haut à gauche du bateau
    x = BLOCK_SIZE*colonne+1
    y = BLOCK_SIZE*ligne+1
    # longueur et largeur du bateau
    # à inverser selon que le bateau est vertical ou horizontal
    if horizontal == True:
        l = BLOCK_SIZE*longueur-2
        w = BLOCK_SIZE-2
    else:
        w = BLOCK_SIZE*longueur-2
        l = BLOCK_SIZE-2
    # rectangle a dessiner
    rect = pygame.Rect(x, y, l, w)
    # dessine le rectangle sur la grille
    pygame.draw.rect(grid, GREY, rect)
    #display()


def init():
    
    global grid1
    global grid2
    global grid1_rect 
    global grid2_rect 
    
    # creation des grilles
    grid1 = create_grid()
    grid2 = create_grid()
    
    # afficher grid1
    grid1_rect = grid1.get_rect()
    grid1_rect.x = 50
    grid1_rect.y = 50
    
    # afficher grid2
    grid2_rect = grid2.get_rect()
    grid2_rect.x = 550
    grid2_rect.y = 50


# fonction bidon pour le placement des bateaux
TEST_BOAT = [ (1,2, 4, True), (4,6, 3, False), (7,8, 2, True)]
boat_nb = 0

def choose_boat(l2=True, l3=True, l4=True):
    "let the user place a boat on grid1"
    # TODO: liste fixe pour le moment
    
    ligne = 0
    colonne = 0
    longueur = 0
    horizontal = None
    
    # rectangle a dessiner
    rectv4 = pygame.Rect( grid2_rect.x, grid2_rect.y, BLOCK_SIZE, BLOCK_SIZE*4)
    rectv3 = pygame.Rect( grid2_rect.x+BLOCK_SIZE*2, grid2_rect.y, BLOCK_SIZE, BLOCK_SIZE*3)
    rectv2 = pygame.Rect( grid2_rect.x+BLOCK_SIZE*4, grid2_rect.y, BLOCK_SIZE, BLOCK_SIZE*2)
    recth4 = pygame.Rect( grid2_rect.x, grid2_rect.y+BLOCK_SIZE*5, BLOCK_SIZE*4, BLOCK_SIZE)
    recth3 = pygame.Rect( grid2_rect.x, grid2_rect.y+BLOCK_SIZE*7, BLOCK_SIZE*3, BLOCK_SIZE)
    recth2 = pygame.Rect( grid2_rect.x, grid2_rect.y+BLOCK_SIZE*9, BLOCK_SIZE*2, BLOCK_SIZE)
    
    while True:
        

        # dessine le rectangle sur la grille
        if l4: pygame.draw.rect(screen, GREY, rectv4)
        if l3: pygame.draw.rect(screen, GREY, rectv3)
        if l2: pygame.draw.rect(screen, GREY, rectv2)
        if l4: pygame.draw.rect(screen, GREY, recth4)
        if l3: pygame.draw.rect(screen, GREY, recth3)
        if l2: pygame.draw.rect(screen, GREY, recth2)
        
        # pour capturer les événements
        for event in pygame.event.get():
            # fermer la fenetre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # evenement click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # bouton gauch
                    (x, y) = event.pos # coordonnées du click
                    print(f"Click en x: {x} et y: {y}")
                    if l4 and rectv4.collidepoint(x, y):
                        longueur = 4
                        horizontal = False
                        selected_rect = rectv4
                    if l3 and rectv3.collidepoint(x, y):
                        longueur = 3
                        horizontal = False
                        selected_rect = rectv3
                    if l2 and rectv2.collidepoint(x, y):
                        longueur = 2
                        horizontal = False
                        selected_rect = rectv2
                    if l4 and recth4.collidepoint(x, y):
                        longueur = 4
                        horizontal = True
                        selected_rect = recth4
                    if l3 and recth3.collidepoint(x, y):
                        longueur = 3
                        horizontal = True
                        selected_rect = recth3
                    if l2 and recth2.collidepoint(x, y):
                        longueur = 2
                        horizontal = True
                        selected_rect = recth2
                 
        if longueur != 0:
            break
        # affichage des grille
        display(only_user_grid=True)
        
    print(f"forme bateau longueur:{longueur} horizontal:{horizontal}")
        
    while True:
        

        # dessine le rectangle sur la grille
        if l4: pygame.draw.rect(screen, GREY, rectv4)
        if l3: pygame.draw.rect(screen, GREY, rectv3)
        if l2: pygame.draw.rect(screen, GREY, rectv2)
        if l4: pygame.draw.rect(screen, GREY, recth4)
        if l3: pygame.draw.rect(screen, GREY, recth3)
        if l2: pygame.draw.rect(screen, GREY, recth2) 
        pygame.draw.rect(screen, RED, selected_rect, 2)
        
        # pour capturer les événements
        for event in pygame.event.get():
            # fermer la fenetre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # evenement click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # bouton gauch
                    (x, y) = event.pos # coordonnées du click
                    print(f"Click en x: {x} et y: {y}")
                    
                    # conversion des coordonnées en ligne, colonne de la grille 1
                    colonne = int((x-grid1_rect.x)/BLOCK_SIZE)
                    ligne = int((y-grid1_rect.y)/BLOCK_SIZE)
                    print(f"Click en ligne: {ligne} et colonne: {colonne}")
                    # est ce que le clique est bien dans la grille 2
        if (colonne>=1) and (colonne<=10) and (ligne>=1) and(ligne<=10):
            # terminé, on renvoie le résultat
            break
                 
        # affichage des grille
        display(only_user_grid=True)
        
    return (ligne, colonne, longueur, horizontal)
    # global boat_nb
    # boat = TEST_BOAT[boat_nb % len(TEST_BOAT)]
    # boat_nb = boat_nb + 1 
    # display()
    #return boat
    

def choose_shoot():
    " display the grids and waits for a click in grid2"

    while True:
    
        # pour capturer les événements
        for event in pygame.event.get():
            # fermer la fenetre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # evenement click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # bouton gauch
                    (x, y) = event.pos # coordonnées du click
                    # conversion des coordonnées en ligne, colonne de la grille 2
                    colonne = int((x-grid2_rect.x)/BLOCK_SIZE)
                    ligne = int((y-grid2_rect.y)/BLOCK_SIZE)
                    print(f"Click en ligne: {ligne} et colonne: {colonne}")
                    # est ce que le clique est bien dans la grille 2
                    if (colonne>=1) and (colonne<=10) and (ligne>=1) and(ligne<=10):
                        # terminé, on renvoie le résultat
                        return ( ligne, colonne )
        
        # affichage des grille
        display()
    
    
def display(only_user_grid=False):
    "Affichage des grille"
    
    # afficher les grille
    screen.blit(grid1, grid1_rect)
    if only_user_grid == False: 
        screen.blit(grid2, grid2_rect)
    
    # TODO: affichage d'un texte
    
    # Affichage sur l'écran
    pygame.display.update()
    
    # Ensure program maintains a rate
    clock.tick(30)
    
    # re-initialiser l' écran
    screen.fill(BLACK)
 
def end():
    pygame.quit()
    #sys.exit()
    

### TESTS    

def test():
    init() 
    
    try:    
        # draw_boat(USER, 6, 6, 4)
        # draw_boat(COMPUTER, 2, 7, 3, False)
        # draw_shoot(USER, 5, 7)
        # draw_shoot(USER, 2, 4)
        # draw_shoot(COMPUTER, 2, 7, hit=True)
        
        # click = choose_shoot()
        # print(click)
            
        
        # while True:
            
        #     # pour capturer les événements
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             sys.exit()
         
        #     display()
            
        boat = choose_boat()
        print(boat)
        
    except:
        # fermer pygame en cas d'exception
        end()
        raise 
    end()
    
#test()