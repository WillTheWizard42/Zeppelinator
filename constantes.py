import pygame
from pygame.locals import *

pygame.display.init()
pygame.display.set_mode()

largeur_ecran = 1680
hauteur_ecran = 1050

taille_projectile = 30
taille_bombe = 90

largeur_rectangle_ui = 100
hauteur_rectangle_ui = 30

blanc = (255, 255, 255)
noir = (0, 0, 0)
vert = (0, 255, 0)

zeppelinator_gauche = pygame.transform.scale(pygame.image.load('assets/Zeppelinator.png'), (250, 250))
zeppelinator_droite = pygame.transform.scale(pygame.image.load('assets/ZeppelinatorDroite.png'), (250, 250))

canon_vertical = pygame.transform.scale(pygame.image.load('assets/CanonVertical.png'), (250, 250))
canon_droite = pygame.transform.scale(pygame.image.load('assets/CanonDroit.png'), (250, 250))
canon_gauche = pygame.transform.scale(pygame.image.load('assets/CanonGauche.png'), (250, 250))

boss1_vertical = pygame.transform.scale(pygame.image.load('assets/BossTank.png'), (300, 300))
boss1_droite = pygame.transform.scale(pygame.image.load('assets/BossTankDroit.png'), (300, 300))
boss1_gauche = pygame.transform.scale(pygame.image.load('assets/BossTankGauche.png'), (300, 300))

boss2_vertical = pygame.transform.scale(pygame.image.load('assets/BossSniper.png'), (300, 300))
boss2_droite = pygame.transform.scale(pygame.image.load('assets/BossSniperDroit.png'), (300, 300))
boss2_gauche = pygame.transform.scale(pygame.image.load('assets/BossSniperGauche.png'), (300, 300))

boss3_vertical = pygame.transform.scale(pygame.image.load('assets/CanonVertical.png'), (350,350))
boss3_droite = pygame.transform.scale(pygame.image.load('assets/CanonDroit.png'), (350,350))
boss3_gauche = pygame.transform.scale(pygame.image.load('assets/CanonGauche.png'), (350,350))

projectile = pygame.transform.scale(pygame.image.load("assets/Projectile.png"), (50,50))
bombe = pygame.transform.scale(pygame.image.load("assets/Ogive.png"), (taille_bombe, taille_bombe))

fond = pygame.transform.scale(pygame.image.load("assets/fond.png").convert(), (largeur_ecran,hauteur_ecran))
pausescreen = pygame.transform.scale(pygame.image.load("assets/pause.png").convert_alpha(), (largeur_ecran,hauteur_ecran))
gameoverscreen = pygame.transform.scale(pygame.image.load("assets/gameoverscreen.png").convert_alpha(), (largeur_ecran,hauteur_ecran))

police_ecriture1 = pygame.font.SysFont("arial", 16, True)
police_ecriture2 = pygame.font.SysFont("arial", 150)

explosions = [ pygame.transform.scale(pygame.image.load("assets/Explosion{}.png".format(i)), (100, 100)) for i in range(1, 9) ]

taille_zeppelinator = 250.0
nb_canon_max = 6

indice_boss_1 = 6
indice_boss_2 = 7
indice_boss_3 = 8