import pygame
from comet import Comet

#creer une classe pour gerer cet evenement
class CometFallEvent:
    
    #lors du chargement -> creer un compteur
    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 5
        self.game = game
        #un groupe de sprite pour stocker nos cometes
        self.all_comets = pygame.sprite.Group()
        self.fall_mode = False
        
    def add_percent(self):
        self.percent += self.percent_speed / 100
    
    def is_full_loaded(self):
        return self.percent >= 100
    
    def reset_percent(self):
        self.percent = 0
    
    def meteor_fall(self):
        #boucle pour les valeurs 1 et 10
        for i in range(1, 10):
            #apparaite une premiere boulle de feu
            self.all_comets.add(Comet(self))
    
    def attempt_fall(self):
        #la jauge d'evenement est totalement charger
        if self.is_full_loaded() and len(self.game.all_monsters) == 0:
            self.meteor_fall()
            self.fall_mode = True #activer l'evenement
            
    def update_bar(self, surface):
        
        #ajouter du pourcentage a la bar
        self.add_percent()
        
        #barre noir (en arriere plan)
        pygame.draw.rect(surface, (0,0,0), [
            0, #axe x
            surface.get_height() - 20, #axe y
            surface.get_width(), #longueur de la fenetre
            10 #l'epaisseur de la bar
        ])
        #barre rouge (jauge d'event)
        pygame.draw.rect(surface, (187,11,11), [
            0, #axe x
            surface.get_height() - 20, #axe y
            (surface.get_width() / 100) * self.percent, #longueur de la fenetre
            10 #l'epaisseur de la bar
        ])