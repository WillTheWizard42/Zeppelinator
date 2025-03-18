import random
import math

from constantes import *
from affichable import Affichable
from systeme_niveaux import Niveau

class Canon(Affichable):
    # création d'une classe pour les canons
    longueur_barre_hp = 60
    hauteur_barre_hp = 10    

    def __init__(self, x, y, vivant, 
                 liste_images = [canon_gauche, canon_vertical, canon_droite],
                 xy_barre_hp = (100, 200), 
                 xy_offsets_debut_tir = [(70, 50), (105, 50), (135, 50)], 
                 x_debut_fin_hitbox = (15, 155),
                 temps_vol_projectile = -1,
                 points = 10,
                 degats = 1,
                 hp_max = 3,
                 borne_inf = 60,
                 borne_sup = 121,
                 nombre_tirs_max = (1,2)):

        super().__init__(x, y, vivant, liste_images, 1)
        self.xy_barre_hp = xy_barre_hp
        self.xy_offsets_debut_tir = xy_offsets_debut_tir
        self.x_debut_fin_hitbox = x_debut_fin_hitbox
        
        self.hp = hp_max
        self.hpmax = float(self.hp)
        self.temps_vol_projectile = temps_vol_projectile
        self.points = points
        self.nombre_tirs_max = nombre_tirs_max
        self.nombre_tirs_alea = random.randrange(nombre_tirs_max[0], nombre_tirs_max[1])
        self.nombre_tirs = 0
        self.degats = degats
        
        self.xy_tirs = []
        self.xy_incr = []
        self.liste_suppression = []

        self.compteur = 0
        self.borne_inf = borne_inf
        self.borne_sup = borne_sup
        self.alea = random.randrange(borne_inf, borne_sup)

    def draw(self, ecran):
        # dessine les canons et les projectiles
        super().draw(ecran)
        
        if self.vivant:            
            x_debut = self.xy[0] + self.xy_barre_hp[0]
            y_debut = self.xy[1] + self.xy_barre_hp[1]

            pygame.draw.rect(ecran, noir, (x_debut, y_debut, Canon.longueur_barre_hp, Canon.hauteur_barre_hp), 1)
            ecran.fill(blanc, (x_debut + 1, y_debut + 1, Canon.longueur_barre_hp - 2, Canon.hauteur_barre_hp - 2))
            ecran.fill(vert, (x_debut + 1, y_debut + 1, (self.hp / self.hpmax) * (Canon.longueur_barre_hp - 2), Canon.hauteur_barre_hp - 2))
        
        for i in range(0, len(self.xy_tirs)):
            ecran.blit(projectile, tuple(self.xy_tirs[i]))

    def tir(self, xy_zeppelin):
        
        if self.vivant:
            if self.nombre_tirs < self.nombre_tirs_alea:
                if (self.compteur - self.alea) % 15 == 0:

                    x_debut = self.xy[0] + self.xy_offsets_debut_tir[self.angle][0]
                    y_debut = self.xy[1] + self.xy_offsets_debut_tir[self.angle][1]
                    
                    self.xy_tirs.append([x_debut, y_debut])
                    
                    dist_alea = random.random() * 200
                    angle_alea = random.random() * 360
                    
                    temps = self.temps_vol_projectile
                    
                    if temps < 0:
                        temps = random.uniform(120, 180)
                    
                    x_vise = xy_zeppelin[0] + taille_zeppelinator / 2 - dist_alea * math.cos(math.radians(angle_alea))
                    y_vise = xy_zeppelin[1] - taille_zeppelinator / 2 - dist_alea * math.sin(math.radians(angle_alea))
                    
                    x_ajout = (x_vise - x_debut) / temps
                    y_ajout = (y_vise - y_debut) / temps
                    
                    self.xy_incr.append((x_ajout, y_ajout))

                    self.nombre_tirs += 1

            if self.nombre_tirs == self.nombre_tirs_alea:
                self.nombre_tirs = 0
                self.compteur = 0
                self.nombre_tirs_alea = random.randrange(self.nombre_tirs_max[0], self.nombre_tirs_max[1])
                self.alea = random.randrange(self.borne_inf, self.borne_sup)

    def update_angle(self, x_zeppelin):
        if -200 <= self.xy[0] - x_zeppelin <= 200:
            self.angle = 1
        elif self.xy[0] - x_zeppelin > 200:
            self.angle = 0
        else:
            self.angle = 2

    def update_compteur(self, zeppelinator):
        self.compteur += 1
        if self.compteur >= self.alea:
            self.tir(zeppelinator.get_position())

    def update_tirs(self, zeppelinator):

        if len(self.xy_tirs) > 0:
            for i in range(len(self.xy_tirs)):
                if self.xy_tirs[i][0] > largeur_ecran or self.xy_tirs[i][0] < -30 or self.xy_tirs[i][1] > hauteur_ecran or self.xy_tirs[i][1] < -30:
                    self.liste_suppression.append(i)
                else:
                    if zeppelinator.test_collision(self.xy_tirs[i], self.degats):
                        self.liste_suppression.append(i)

                self.xy_tirs[i][0] += self.xy_incr[i][0]
                self.xy_tirs[i][1] += self.xy_incr[i][1]

            for i in range(len(self.liste_suppression) - 1, -1, -1):
                self.xy_tirs.pop(self.liste_suppression[i])
                self.xy_incr.pop(self.liste_suppression[i])

            self.liste_suppression = []

    def update(self, zeppelinator):
        self.update_tirs(zeppelinator)
        if not self.vivant:
            return

        self.update_angle(zeppelinator.get_position()[0])
        self.update_compteur(zeppelinator)
        
    def test_collision_bombe(self, x_bombe):
        if self.vivant:
            if self.xy[0] + self.x_debut_fin_hitbox[0] < x_bombe < self.xy[0] + self.x_debut_fin_hitbox[1]:
                self.hp -= 1 
                Niveau.incrementer_score(self.points)

            if self.hp <= 0:
                self.vivant = False

    def reset(self):
        self.vivant = False
        self.hp = self.hpmax

        self.xy_tirs = []
        self.xy_incr = []
        self.liste_suppression = []

    def respawn(self):
        self.reset()
        self.vivant = True

    def est_vivant(self):
        return self.vivant