import pygame

from pygame.locals import *

class Scene_Changer:

    def __init__(self, newscene, screen):
        self.frame = 0
        self.Img_LastScene = screen.copy()
        self.Img_NewScene = screen.copy()
        newscene.update(self.Img_NewScene)
        self.new_scene = newscene
        
    def update(self, screen):
        
        self.Img_NewScene.set_alpha(self.frame)

        screen.blit(self.Img_LastScene, (0,0))
        screen.blit(self.Img_NewScene, (0,0))
        self.frame+=8
        
        if (self.frame >= 256):
            return self.new_scene
