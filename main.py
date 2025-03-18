#!/usr/bin/env python

import asyncio
import pygame
from pygame.locals import *

pygame.init()

from constantes import *
from canon import Canon
from zeppelinator import Zeppelinator

from systeme_explosion import Explosions
from systeme_niveaux import Niveau

def draw(ecran, liste_canons, zeppelinator):
    ecran.blit(fond, (0, 0))

    for canon in liste_canons:
        canon.draw(ecran)

    zeppelinator.draw(ecran)
    Explosions.draw(ecran)
    Niveau.draw(ecran)

def pause(ecran):
    paused = True
    quit = False
    pygame.mixer.music.fadeout(1500)
    pos_musique = pygame.mixer.music.get_pos()
    while paused:
        for event in pygame.event.get():
            # Unpause
            if (
                event.type == pygame.KEYDOWN 
                and event.key == pygame.K_ESCAPE

                or event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and 508 < event.pos[0] < 1173
                and 345 < event.pos[1] < 494
            ):
                paused = False
                pygame.mixer.music.play(-1, pos_musique / 1000.0)
            # Quit
            elif (
                event.type == pygame.QUIT
                or event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and 665 < event.pos[0] < 999
                and 525 < event.pos[1] < 674
            ):
                paused = False
                quit = True

        ecran.blit(pausescreen, (0, 0))
        pygame.display.flip()

    return quit

def gameover(ecran, liste_canons, zeppelinator):
    
    pygame.mixer.music.fadeout(1500)
    
    lost = True
    quit = False
    
    while lost:
        for event in pygame.event.get():
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and 508 < event.pos[0] < 1173
                and 345 < event.pos[1] < 494
            ):
                lost = False
                Niveau.reinitialiser()

                for canon in liste_canons:
                    canon.reset()
                
                zeppelinator.respawn([10, 10], 1)
                Explosions.reinitialiser()
                break

            elif (
                event.type == pygame.QUIT
                or event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and 665 < event.pos[0] < 999
                and 525 < event.pos[1] < 674
            ):
                lost = False
                quit = True
                break

        ecran.blit(gameoverscreen, (0, 0))
        pygame.display.flip()
    
    return quit

async def main():

    ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran), FULLSCREEN)

    pygame.mixer.music.load("assets/Musique.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    pygame.display.set_caption("Zeppelinator")

    canon1 = Canon(26, 595, False)
    canon2 = Canon(301, 595, False)
    canon3 = Canon(577, 595, False)
    canon4 = Canon(853, 595, False)
    canon5 = Canon(1129, 595, False)
    canon6 = Canon(1404, 595, False)

    boss1 = Canon(700, 560, False, [boss1_gauche, boss1_vertical, boss1_droite], (125, 299), [(75, 0), (120, 0), (175, 0)], (25, 175), 180, 50, 2, 15)
    boss2 = Canon(700, 560, False, [boss2_gauche, boss2_vertical, boss2_droite], (125, 299), [(55, 0), (125, 0), (170, 0)], (50, 160), 60, 50, 5, 6, 180, 181)
    boss3 = Canon(700, 505, False, [boss3_gauche, boss3_vertical, boss3_droite], (155, 320), [(115, 90), (155, 80), (200, 85)], (90, 190), 120, 50, 1, 6, 150, 151, (7, 15))

    liste_canons = [canon1, canon2, canon3, canon4, canon5, canon6, boss1, boss2, boss3]

    zeppelinator = Zeppelinator(10, 10, True, [zeppelinator_gauche, zeppelinator_droite], bombe)

    quit = False
    clock = pygame.time.Clock()

    while not quit:
        # Boucle principale

        if Niveau.doit_update():
            zeppelinator.update(liste_canons)

            for canon in liste_canons:
                canon.update(zeppelinator)

            Explosions.update()
        
        quit = Niveau.update(liste_canons, zeppelinator)
        draw(ecran, liste_canons, zeppelinator)
        pygame.display.flip()

        clock.tick(60)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())