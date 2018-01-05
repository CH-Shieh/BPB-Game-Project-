import pygame
import sqlite3

class Scene_GameOver:
    def __init__(self, gamemode = 1, playerdata = (0,0), extradata = []):
        self.gamemode = gamemode
        maxcombo, score = playerdata        
        
