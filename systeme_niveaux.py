from constantes import *
from systeme_explosion import Explosions

class Niveau:
    
    score = 0
    niveau = 2
    augmente = True
    temps_entre_niveau = 180
    compteur = 0

    perdu = False
    pause = False

    pos_musique = 0

    def incrementer_score(points):
        Niveau.score += points
        if Niveau.score < 0:
            Niveau.score = 0

    def draw(ecran):
        txt_points = police_ecriture1.render("Score: " + str(Niveau.score), True, noir)
        ecran.blit(txt_points, (1000, 35))

        if Niveau.augmente:
            lvl = police_ecriture2.render("Level {}:".format(Niveau.niveau - 1), True, noir)
            ecran.blit(lvl, (500, 400))

        if Niveau.perdu:
            ecran.blit(gameoverscreen, (0, 0))
        if Niveau.pause:
            ecran.blit(pausescreen, (0, 0))

    def reinitialiser(liste_canons, zeppelinator):
        pygame.mixer.music.play(-1)
        
        Niveau.augmente = True
        Niveau.score = 0
        Niveau.niveau = 2
        Niveau.pause = False
        Niveau.perdu = False

        for canon in liste_canons:
            canon.reset()
        
        zeppelinator.respawn([10, 10], 1)
        Explosions.reinitialiser()

    def spawn_canons_et_boss(liste_canons, indice_boss):
        for i in range(nb_canon_max // 2 - 1):
            liste_canons[i].respawn()
        
        for i in range(nb_canon_max // 2 + 1, nb_canon_max):
            liste_canons[i].respawn()

        liste_canons[indice_boss].respawn()

    def spawn_canons(liste_canons, nombre):
        nombre = max(min(nombre, nb_canon_max), 0)
        indice_depart = nb_canon_max // 2 - nombre // 2
        indice_fin = nb_canon_max // 2 + nombre // 2

        for i in range(indice_depart, indice_fin):
            liste_canons[i].respawn()

    def test_incr_niveau(liste_canons, zeppelinator):
        vivants = False
        for canon in liste_canons:
            if canon.est_vivant():
                vivants = True
                break

        if not Niveau.augmente and not vivants:
            if (Niveau.niveau + 2) % 3 == 0:
                zeppelinator.regen_hp(5)
            else:
                zeppelinator.regen_hp(1)

            Niveau.niveau += 1
            Niveau.augmente = True
            Niveau.score += 50
            for canon in liste_canons:
                canon.reset()

        if Niveau.augmente:
            Niveau.compteur += 1
            if Niveau.compteur >= Niveau.temps_entre_niveau:
                Niveau.compteur = 0
                Niveau.augmente = False

                if (Niveau.niveau - 1) % 9 == 0:
                    Niveau.spawn_canons_et_boss(liste_canons, indice_boss_3)
                elif (Niveau.niveau - 1) % 6 == 0:
                    Niveau.spawn_canons_et_boss(liste_canons, indice_boss_2)
                elif (Niveau.niveau - 1) % 3 == 0:
                    Niveau.spawn_canons_et_boss(liste_canons, indice_boss_1)
                elif Niveau.niveau == 2:
                    Niveau.spawn_canons(liste_canons, 2)
                elif Niveau.niveau == 3:
                    Niveau.spawn_canons(liste_canons, 4)
                else:
                    Niveau.spawn_canons(liste_canons, 6)

    def toggle_pause():
        Niveau.pause = not Niveau.pause
        if Niveau.pause:
            pygame.mixer.music.fadeout(1500)
            Niveau.pos_musique = pygame.mixer.music.get_pos()

        else:
            pygame.mixer.music.play(-1, Niveau.pos_musique / 1000.0)

    def keytest(liste_canons, zeppelinator):
        quit = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                break

            if Niveau.perdu:
                
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and 508 < event.pos[0] < 1173
                    and 345 < event.pos[1] < 494
                ):
                    Niveau.reinitialiser(liste_canons, zeppelinator)
                    break

                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and 665 < event.pos[0] < 999
                    and 525 < event.pos[1] < 674
                ):
                    quit = True
                    break
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    Niveau.toggle_pause()
                    break
                
                if Niveau.pause:
                    # Cliquer sur continuer
                    if (event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1
                        and 508 < event.pos[0] < 1173
                        and 345 < event.pos[1] < 494
                    ):
                        Niveau.toggle_pause()
                        break

                    # Cliquer sur quitter
                    elif (event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1
                        and 665 < event.pos[0] < 999
                        and 525 < event.pos[1] < 674
                    ):
                        quit = True
                        break

        return quit

    def doit_update():
        return not Niveau.perdu and not Niveau.pause

    def update(liste_canons, zeppelinator):
        Niveau.test_incr_niveau(liste_canons, zeppelinator)
        
        quit = Niveau.keytest(liste_canons, zeppelinator)

        if not zeppelinator.est_vivant():
            Niveau.perdu = True

        return quit
