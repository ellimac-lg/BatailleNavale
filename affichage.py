#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 18:42:17 2024

@author: clg
"""

import pygame
import sys

# réglages affichage
BLOCK_SIZE = 40

# couleurs
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREY = (120,120,120)
GREEN = (1, 215, 88)

# music
MP4_FILE = "music_chill.mp3"

# designation des joueurs
USER = "user"
COMPUTER = "COMPUTER"

#initialisation
pygame.init()

# Load and play background music
pygame.mixer.init()
pygame.mixer.music.load(MP4_FILE)
pygame.mixer.music.play(loops=-1)


# Setup the clock for a decent framerate
clock = pygame.time.Clock()

#surface de fenetre/taille
WINDOW_WIDTH = BLOCK_SIZE*25
WINDOW_HEIGHT = BLOCK_SIZE*15
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#variables globales
# texte qui s'affiche sur la fenêtre
text = ""
font_text = pygame.font.SysFont(None, BLOCK_SIZE) # police d'écriture
# grilles
grid1 = None
grid2 = None
grid1_rect = None
grid2_rect = None

def get_grid(player):
    "donne la grille du player"
    if player == USER: return grid1
    if player == COMPUTER: return grid2
    end()

def create_grid():
    " creation d une grille vierge"
    
    grid_size = BLOCK_SIZE*11
    # surface grille
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
    if horizontal:
        l = BLOCK_SIZE*longueur-2
        w = BLOCK_SIZE-2
    else:
        w = BLOCK_SIZE*longueur-2
        l = BLOCK_SIZE-2
    # rectangle a dessiner
    rect = pygame.Rect(x, y, l, w)
    # dessine le rectangle sur la grille
    pygame.draw.rect(grid, GREY, rect)
    

def init():
    
    global grid1
    global grid2
    global grid1_rect 
    global grid2_rect 
    global text
    
    # creation des grilles
    grid1 = create_grid()
    grid2 = create_grid()
    
    # afficher grid1
    grid1_rect = grid1.get_rect()
    grid1_rect.x = BLOCK_SIZE
    grid1_rect.y = BLOCK_SIZE
    
    # afficher grid2
    grid2_rect = grid2.get_rect()
    grid2_rect.x = grid1_rect.right + BLOCK_SIZE
    grid2_rect.y = BLOCK_SIZE

    text = ""


def choose_boat(l2=True, l3=True, l4=True):
    "let the user place a boat on grid1"
    
    ligne = 0
    colonne = 0
    longueur = 0
    horizontal = None
    
    # rectangles a dessiner pour le choix des bateaux
    rectv4 = pygame.Rect( grid2_rect.x, grid2_rect.y, BLOCK_SIZE, BLOCK_SIZE*4)
    rectv3 = pygame.Rect( grid2_rect.x+BLOCK_SIZE*2, grid2_rect.y, BLOCK_SIZE, BLOCK_SIZE*3)
    rectv2 = pygame.Rect( grid2_rect.x+BLOCK_SIZE*4, grid2_rect.y, BLOCK_SIZE, BLOCK_SIZE*2)
    recth4 = pygame.Rect( grid2_rect.x, grid2_rect.y+BLOCK_SIZE*5, BLOCK_SIZE*4, BLOCK_SIZE)
    recth3 = pygame.Rect( grid2_rect.x, grid2_rect.y+BLOCK_SIZE*7, BLOCK_SIZE*3, BLOCK_SIZE)
    recth2 = pygame.Rect( grid2_rect.x, grid2_rect.y+BLOCK_SIZE*9, BLOCK_SIZE*2, BLOCK_SIZE)
    
    ### Selection du bateau ###
    while True:
        
        # dessine les rectangles sur la grille
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
                    # est ce qu'un des bateaux a été selectionné
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
        # si un bateau a été selectionné passons à la suite
        if longueur != 0:
            break
        # affichage des grille
        display(only_user_grid=True)
        
    print(f"forme bateau longueur:{longueur} horizontal:{horizontal}")
        
    ### Placement du bateau ###
    while True:
        
        # dessine les rectangles sur la grille
        if l4: pygame.draw.rect(screen, GREY, rectv4)
        if l3: pygame.draw.rect(screen, GREY, rectv3)
        if l2: pygame.draw.rect(screen, GREY, rectv2)
        if l4: pygame.draw.rect(screen, GREY, recth4)
        if l3: pygame.draw.rect(screen, GREY, recth3)
        if l2: pygame.draw.rect(screen, GREY, recth2) 
        # entoure le bateau selectionné de rouge
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
        # est ce que le clique est bien dans la grille
        if (colonne>=1) and (colonne<=10) and (ligne>=1) and(ligne<=10):
            # terminé, on renvoie le résultat
            break
                 
        # affichage
        display(only_user_grid=True)
        
    # retourne le bateau selectionné et placé sur la grille
    return (ligne, colonne, longueur, horizontal)
    

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

def reset():
    " display the grids and waits for a click in reset button"

    # affichage d'un texte
    texte_surf = font_text.render( "reset" , True, WHITE) # surface texte
    # rect pour plqcer le texte dqns lq grille
    texte_rect = texte_surf.get_rect()
    texte_rect.x = grid2_rect.centerx
    texte_rect.y = grid2_rect.bottom + BLOCK_SIZE
    # rectangle pour le bouton, plus gros mais centré comme le texte
    bouton_rect = texte_rect.scale_by(1.5)
    bouton_rect.centerx = texte_rect.centerx
    bouton_rect.centery = texte_rect.centery
    
    while True:
        
        # ecriture sur l'écran
        pygame.draw.rect(screen, GREEN, bouton_rect, 0, int(BLOCK_SIZE/4) )
        pygame.draw.rect(screen, WHITE, bouton_rect, 2, int(BLOCK_SIZE/4) )
        screen.blit(texte_surf, texte_rect)
    
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
                    # est ce que le click est dqns le buton reset
                    if bouton_rect.collidepoint(x, y):
                        return                    
        
        # affichage des grille
        display()


def set_text(t):
    global text
    text = t
    
def display(only_user_grid=False):
    "Affichage des grille"
    
    # afficher les grille
    screen.blit(grid1, grid1_rect)
    if only_user_grid == False: 
        screen.blit(grid2, grid2_rect)
    
    # affichage d'un texte
    texte_surf = font_text.render( text , True, WHITE) # surface texte
    # rect pour plqcer le texte dqns lq grille
    texte_rect = texte_surf.get_rect()
    texte_rect.x = grid1_rect.left
    texte_rect.y = grid1_rect.bottom + BLOCK_SIZE
    # ecriture sur lq grille
    screen.blit(texte_surf, texte_rect)
    
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

if __name__ == "__main__":
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
            
        #boat = choose_boat()
        #print(boat)
        reset()
        
        end()
        
    except:
        # fermer pygame en cas d'exception
        end()
        raise 
    
    
