class Affichable:
    # création d'une classe pour les canons
    def __init__(self, x, y, vivant, liste_images, angle):
        self.xy = [x, y]
        self.liste_images = liste_images
        self.vivant = vivant
        self.angle = angle

    def draw(self, ecran):
        if self.vivant:
            ecran.blit(self.liste_images[self.angle], (self.xy[0], self.xy[1]))