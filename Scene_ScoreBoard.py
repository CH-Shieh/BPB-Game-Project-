import pygame

from sys import exit

from pygame_button import *
from Scene_Changer import *
from DB import DB
class Scene_ScoreBoard:
    mfont = pygame.font.SysFont("Arial Black", 24, True, True)
    mfont2 = pygame.font.Font("msjh.ttf", 24)
    graphics_bg = pygame.image.load("Graphics/bg0004.png")

    audio_bgm_filename = "Audio/BGM/bgm_03.ogg"
    frame = 0
    WINDOWWIDTH = 800 # size of window's width in pixels
    WINDOWHEIGHT = 720 # size of windows' height in pixels
    
    def __init__(self):
        
        ####改解析度
        self.NewScreen = pygame.display.set_mode((self.WINDOWWIDTH,self.WINDOWHEIGHT), 0, 32)
        
        try:
            pygame.mixer.music.load(self.audio_bgm_filename)
            pygame.mixer.music.play(-1)
        except:
            print("Mixer Init Failed!")

        self.button1_image = self.mfont.render("Name", 12, (255,255,128))
        self.button2_image = self.mfont.render("Score", 12, (255,255,128))
        self.button3_image = self.mfont.render("Combo", 12, (255,255,128))
        self.button4_image = self.mfont.render("Time", 12, (255,255,128))
        self.button5_image = self.mfont.render("Sync", 12, (255,255,128))
        
        self.button1 = pyButton();
        self.button1.setImage(self.button1_image, True)
        self.button2 = pyButton();
        self.button2.setImage(self.button2_image, True)
        self.button3 = pyButton();
        self.button3.setImage(self.button3_image, True)
        self.button4 = pyButton();
        self.button4.setImage(self.button4_image, True)
        self.button5 = pyButton();
        self.button5.setImage(self.button5_image, True)

        self.button1.rect.x = 20   
        self.button1.rect.y = 40

        self.button2.rect.x = 220   
        self.button2.rect.y = 40
        
        self.button3.rect.x = 340   
        self.button3.rect.y = 40
        
        self.button4.rect.x = 460   
        self.button4.rect.y = 40
        
        self.button5.rect.x = 720   
        self.button5.rect.y = 40

        self.score_list = []
        self.load_score()
        
        self.ButtonGroup = pygame.sprite.Group()
        self.ButtonGroup.add([self.button1, self.button2, self.button3, self.button4, self.button5])

        self.CurrentName = "NoName"

    def load_score(self):
        database = DB()
        self.score_list = database.read()
        
    def update(self, screen):
        # 退出事件處理

        mouse1, mouse2 ,mouse3 = (False,False,False)
        
        # 退出事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEMOTION:
                cur_x, cur_y = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    mouse3 = True
        
        cur_x, cur_y = pygame.mouse.get_pos()
        

        mouse1, mouse2, mouse3 =  pygame.mouse.get_pressed()
        
        self.frame += 1
        screen.blit(self.graphics_bg, (0,0))
        self.ButtonGroup.draw(screen)

        ####分數列表繪製
        for i in range(len(self.score_list)):
            if (i%2 == 0):
                color = (255,255,255)
            else:
                color = (192,192,192)
            i_name = self.mfont2.render(str(self.score_list[i][1]), 1, color)
            i_score = self.mfont2.render(str(self.score_list[i][2]), 1, color)
            i_combo = self.mfont2.render(str(self.score_list[i][3]), 1, color)
            i_time = self.mfont2.render(str(self.score_list[i][4]), 1, color)
            i_online = self.mfont2.render(str(self.score_list[i][5]), 1, color)

            screen.blit(i_name, (self.button1.rect.x, self.button1.rect.y + 40*(i+1)))
            screen.blit(i_score, (self.button2.rect.x, self.button2.rect.y + 40*(i+1)))
            screen.blit(i_combo, (self.button3.rect.x, self.button3.rect.y + 40*(i+1)))
            screen.blit(i_time, (self.button4.rect.x, self.button4.rect.y + 40*(i+1)))
            screen.blit(i_online, (self.button5.rect.x, self.button5.rect.y + 40*(i+1)))
            
        if (mouse3 == True):
            from Scene_Title import Scene_Title
            return Scene_Changer(Scene_Title(), screen)
