from systeme_explosion import Explosions
from systeme_niveaux import Niveau
from affichable import Affichable
from constantes import *

class Zeppelinator(Affichable):
    
    vitesse = 10
    vitesse_bombe = 20

    def __init__(self, x, y, vivant, liste_images, image_bombe):
        super().__init__(x, y, vivant, liste_images, 1)
        self.compteur = 60
        self.xy_bombe = [0, 0]
        self.bombardement = False
        self.hp = 10
        self.hp_max = float(self.hp)
        self.image_bombe = image_bombe

    def bombarder(self):
        if self.compteur >= 60:
            self.xy_bombe = [ self.xy[0] + 80, self.xy[1] + 150 ]
            self.bombardement = True
            self.compteur = 0

    def keytest(self):
        # Associe chaque clé à une action
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.xy[1] -= Zeppelinator.vitesse
        if pressed[pygame.K_DOWN]:
            self.xy[1] += Zeppelinator.vitesse
        if pressed[pygame.K_RIGHT]:
            self.xy[0] += Zeppelinator.vitesse
            self.angle = 1
        if pressed[pygame.K_LEFT]:
            self.xy[0] -= Zeppelinator.vitesse
            self.angle = 0
        if pressed[pygame.K_SPACE]:
            self.bombarder()

    def draw(self, ecran):
        super().draw(ecran)

        hp = self.hp
        hp_max = self.hp_max
        compteur = self.compteur

        # rectangle hp
        pygame.draw.rect(ecran, noir, (30, 30, largeur_rectangle_ui, hauteur_rectangle_ui), 1)
        ecran.fill(blanc, (31, 31, largeur_rectangle_ui - 2, hauteur_rectangle_ui - 2))
        ecran.fill((255 - (hp / hp_max) * 255, (hp / hp_max) * 255, 0), (31, 31, (hp / hp_max) * (largeur_rectangle_ui - 2), hauteur_rectangle_ui - 2))
        txt_hp = police_ecriture1.render("HP", True, noir)
        nb_hp = police_ecriture1.render(str(hp), True, noir)
        ecran.blit(txt_hp, (140, 35))
        ecran.blit(nb_hp, (75, 35))

        # rectangle bombe
        pygame.draw.rect(ecran, noir, (1550, 30, largeur_rectangle_ui, hauteur_rectangle_ui), 1)
        ecran.fill(blanc, (1551, 31, largeur_rectangle_ui - 2, hauteur_rectangle_ui - 2))
        ecran.fill(
            (255 - (compteur / 60.0) * 255, (compteur / 60.0) * 255, 0),
            (1551, 31, (compteur / 60.0) * (largeur_rectangle_ui - 2), hauteur_rectangle_ui - 2),
        )
        txt_bombe = police_ecriture1.render("Bomb:", True, noir)
        nb_bombe = police_ecriture1.render(str(round(compteur / 60.0, 2)) + " s", True, noir)
        ecran.blit(txt_bombe, (1470, 35))
        ecran.blit(nb_bombe, (1580, 35))

        # bombe
        if self.bombardement:
            ecran.blit(self.image_bombe, (self.xy_bombe[0], self.xy_bombe[1]))

    def limiter_position(self):
        self.xy[0] = min(max(self.xy[0], 0), 1420)
        self.xy[1] = min(max(self.xy[1], -50), 270)

    def test_collision(self, xy, degats):
        touche = False
        if self.angle == 1:
            if (
                self.xy[0] + 10 < xy[0] + 25 < self.xy[0] + 70
                and self.xy[1] + 90 < xy[1] + 25 < self.xy[1] + 160
                or self.xy[0] + 70 < xy[0] + 25 < self.xy[0] + 140
                and self.xy[1] + 50 < xy[1] + 25 < self.xy[1] + 200
                or self.xy[0] + 140 < xy[0] + 25 < self.xy[0] + 240
                and self.xy[1] + 80 < xy[1] + 25 < self.xy[1] + 170
            ):
                touche = True
        
        elif self.angle == 0:
            if (
                self.xy[0] + 10 < xy[0] + 25 < self.xy[0] + 110
                and self.xy[1] + 80 < xy[1] + 25 < self.xy[1] + 170
                or self.xy[0] + 110 < xy[0] + 25 < self.xy[0] + 180
                and self.xy[1] + 50 < xy[1] + 25 < self.xy[1] + 200
                or self.xy[0] + 180 < xy[0] + 25 < self.xy[0] + 240
                and self.xy[1] + 80 < xy[1] + 25 < self.xy[1] + 170
            ):
                touche = True
        
        if touche:
            self.hp = max(self.hp - degats, 0)
            if self.hp == 0:
                self.vivant = False

            Niveau.incrementer_score(-10)
            Explosions.ajout_explosion(xy, (-25, -25))

            return True
        
        return False

    def update(self, liste_canons):

        self.keytest()
        self.limiter_position()
        if self.compteur < 60:
            self.compteur += 1
        
        if self.bombardement:
            self.xy_bombe[1] += Zeppelinator.vitesse_bombe
            
            if self.xy_bombe[1] > 750:
                self.bombardement = False

                Explosions.ajout_explosion(self.xy_bombe, (-5, -5))
                for canon in liste_canons:
                    canon.test_collision_bombe(self.xy_bombe[0])

    def regen_hp(self, hp):
        self.hp = min(self.hp + hp, self.hp_max)

    def est_vivant(self):
        return self.vivant
    
    def get_position(self):
        return self.xy
    
    def respawn(self, xy, angle):
        self.compteur = 60
        self.xy_bombe = [0, 0]
        self.bombardement = False
        self.hp = self.hp_max
        self.vivant = True
        self.xy = xy
        self.angle = angle