import pygame
import random
import animation

#creer une classe qui va gerer la notion de monstre sur notre jeu
class Monster(animation.AnimateSprite):
    
    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.3
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 540 - offset
        self.velocity = random.randint(1,2)
        self.loot_amount = 10
        self.start_animation()
        
    def set_loot_amount(self, amount):
        self.loot_amount = amount
    
    def dammage(self, amount):
        #infliger les degats
        self.health -= amount
        
        #verifier si son nouveau nombre de points de vie est inferieur ou egal a 0
        if self.health <= 0:
            #reapparaitre comme un nouveau monstre
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1,2)
            self.health = self.max_health
            #ajouter le nombre de point a ce score
            self.game.add_score(self.loot_amount)
            
            #si la barre d'evenement est chargé a son maximum
            if self.game.comet_event.is_full_loaded():
                #retirer du jeu
                self.game.all_monsters.remove(self)
                
                #appel de la methode pour essayer de declencher la pluie de cometes
                self.game.comet_event.attempt_fall()
    
    def update_animation(self):
        self.animate(loop=True)
    
    def update_health_bar(self, surface):
        
        #dessiner notre barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 10, self.rect.y - 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 10, self.rect.y - 20, self.health, 5])
        
        
    def forward(self):
        #le deplacement ne se fait que si il n'y a pas de collision avec un groupe de joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        #si le monstre est en collision avec le joueur
        else:
            #infliger des degats
            self.game.player.dammage(self.attack)

#definir une classe pour la momie
class Mummy(Monster):
    
    def __init__(self, game):
        super().__init__(game, 'mummy', (130,130))
        self.set_loot_amount(20)

class Alien(Monster):
    
    def __init__(self, game):
        super().__init__(game, 'alien', (300,300), 140)
        self.health = 250
        self.max_health = 250
        self.set_loot_amount(80)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            