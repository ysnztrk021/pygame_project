import pygame
from player import Player
from monster import Mummy
from monster import Alien
from comet_event import CometFallEvent
from sounds import SoundManager

#creer une seconde classe qui va representer notre jeu
class Game:
    
    def __init__(self):
        #definir si notre jeu a commencer ou non
        self.is_playing = False
        #generer notre joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        #generer l'evenement
        self.comet_event = CometFallEvent(self)
        self.sound_manager = SoundManager()
        #mettre le score a 0
        self.font = pygame.font.Font('assets/My_custom_font.ttf', 25)
        self.score = 0
        self.pressed = {}
        
    
    def start(self):
        self.is_playing = True
        self.all_monsters = pygame.sprite.Group()
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)
    
    def add_score(self, points=10):
        self.score += points
    
    def game_over(self):
        #remettre a neuf, retirer les monstres, remttre le joueur a 100 de vies, jeu en attente
        self.all_monster = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        self.sound_manager.play('game_over')
        
    def update(self, screen):
        #afficher le score sur l'ecran
        score_text = self.font.render(f"Score : {self.score}", 1, (0,0,0))
        screen.blit(score_text, (20,20))
        
        #appliquer l'image de mon joueur
        screen.blit(self.player.image, self.player.rect)
        
        #actualiser la barre de vie du joueur
        self.player.update_health_bar(screen)
        
        #actualiser la bar d'evenement du jeu
        self.comet_event.update_bar(screen)
        
        #actualiser l'animation du joueur
        self.player.update_animation()
        
        #recuperer les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()
            
        #recuperer les monstres de notre jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()
            
        #recuperer les comettes de notre jeu
        for comet in self.comet_event.all_comets:
            comet.fall()
        
        #appliquer l'ensemble des images de mon groupe de projectiles
        self.player.all_projectiles.draw(screen)
        
        #appliquer l'ensemble des images de mon groupe de monstre
        self.all_monsters.draw(screen)
        
        #appliquer l'ensemble des images de mon groupe de comettes
        self.comet_event.all_comets.draw(screen)
        
        #verifier si le joeur souhaşte aller a gauche ou a droite
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()
        
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
            
    def spawn_monster(self, monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))
