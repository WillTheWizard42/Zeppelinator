from constantes import *

class Explosions:
    
    lieu_explo = []
    stade_explo = []
    temps_explo = []
    suppr_explo = []
    temps_max_explo = 10
    nb_stades_explo = len(explosions)

    def ajout_explosion(xy, xy_offset):
        Explosions.lieu_explo.append((xy[0] + xy_offset[0], xy[1] + xy_offset[1]))
        Explosions.stade_explo.append(0)
        Explosions.temps_explo.append(0)

    def update():
        for i in range(len(Explosions.temps_explo)):
            Explosions.temps_explo[i] += 1
            if Explosions.temps_explo[i] >= Explosions.temps_max_explo:
                Explosions.stade_explo[i] += 1
                Explosions.temps_explo[i] = 0
            if Explosions.stade_explo[i] == Explosions.nb_stades_explo:
                Explosions.suppr_explo.append(i)

        for i in range(len(Explosions.suppr_explo) - 1, -1, -1):
            Explosions.temps_explo.pop(Explosions.suppr_explo[i])
            Explosions.lieu_explo.pop(Explosions.suppr_explo[i])
            Explosions.stade_explo.pop(Explosions.suppr_explo[i])

        Explosions.suppr_explo = []

    def draw(ecran):
        for i in range(len(Explosions.lieu_explo)):
            ecran.blit(explosions[Explosions.stade_explo[i]], Explosions.lieu_explo[i])

    def reinitialiser():
        Explosions.lieu_explo = []
        Explosions.stade_explo = []
        Explosions.temps_explo = []
        Explosions.suppr_explo = []