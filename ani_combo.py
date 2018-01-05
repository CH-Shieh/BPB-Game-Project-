import pygame
from random import randint
from ani_base import *

class ani_combo(ani_base):
    font12 = pygame.font.SysFont("Arial Black", 12,False, True)
    font24 = pygame.font.SysFont("Arial Black", 24,False, True)
    font32 = pygame.font.SysFont("Arial Black", 32,False, True)
    font48 = pygame.font.SysFont("Arial Black", 48,False, True)
    def __init__(self, combocount, x, y, vec_x, vec_y, speed_x, speed_y):
        color = (255, max(0,(255 - combocount*17)), max(0,(255 - combocount*34)))
        if (combocount <= 5):
            label = self.font24.render( str(combocount), 1, color)
            label2 = self.font12.render("Combo", 1, (255,255,255))
        elif (combocount <= 10):
            label = self.font32.render( str(combocount), 3, color)
            label2 = self.font24.render("Combo", 1, (255,255,255))
        else:
            label = self.font48.render( str(combocount), 5, color)
            label2 = self.font32.render("Combo", 1, (255,255,255))

        
        new_anim = pygame.Surface((label.get_width()+label2.get_width(), label.get_height()+label2.get_height()))
        new_anim.set_colorkey((0,0,0))

        new_anim.blit(label, (0,0))
        new_anim.blit(label2, (label.get_width()/2, label.get_height()/2))
        
        self.add_anim(new_anim, x,y,vec_x,vec_y,speed_x,speed_y, -1)
