import pygame

from sys import exit

from pygame_button import *
from Scene_Changer import *
from Name_Entry import Name_Entry
from System_GameConfig import System_GameConfig

class Scene_Option:
    mfont = pygame.font.SysFont("Arial Black", 24, True, True)
    mfont2 = pygame.font.Font("msjh.ttf", 24)
    graphics_bg = pygame.image.load("Graphics/bg0002.png")

    audio_bgm_filename = "Audio/BGM/lobby.ogg"

    audio_se_ok_filename = "Audio/SE/button_p.wav"
    frame = 0
    def __init__(self):
        try:
            pygame.mixer.music.load(self.audio_bgm_filename)
            pygame.mixer.music.play(-1)
            self.audio_se_ok = pygame.mixer.Sound(self.audio_se_ok_filename)
        except:
            print("Mixer Init Failed!")

        self.button1_image = self.mfont.render("Change Name", 12, (192,0,0))
        self.button1_image_b = self.mfont.render("Change Name", 12, (127,127,127))
        self.button2_image = self.mfont.render("Scoreboard Reset", 12, (192,0,0))
        self.button2_image_b = self.mfont.render("Scoreboard Reset", 12, (127,127,127))
        self.button3_image = self.mfont.render("AUTO ScreenShot", 12, (192,0,0))
        self.button3_image_b = self.mfont.render("AUTO ScreenShot", 12, (127,127,127))
        self.button4_image = self.mfont.render("BT", 12, (192,0,0))
        self.button4_image_b = self.mfont.render("BT", 12, (127,127,127))
        
        self.button1 = pyButton();
        self.button1.setImage(self.button1_image, True)
        self.button2 = pyButton();
        self.button2.setImage(self.button2_image, True)
        self.button3 = pyButton();
        self.button3.setImage(self.button3_image, True)
        self.button4 = pyButton();
        self.button4.setImage(self.button4_image, True)

        self.button1.rect.y = 460
        self.button2.rect.y = 500
        self.button3.rect.y = 540
        self.button4.rect.y = 580
                                
        self.ButtonGroup = pygame.sprite.Group()
        self.ButtonGroup.add([self.button1, self.button2, self.button3])
        
        self.cfg = System_GameConfig()
        self.CurrentName = self.cfg.CurrentName
        
    def update(self, screen):
        # 退出事件處理

        mouse1, mouse2 ,mouse3 = (False,False,False)
        
        # 退出事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse1 = True
                if event.button == 2:
                    mouse2 = True
                if event.button == 3:
                    mouse3 = True
        
        cur_x, cur_y = pygame.mouse.get_pos()
        
        self.frame += 1
        screen.blit(self.graphics_bg, (0,0))
        self.ButtonGroup.draw(screen)

        if (self.button1.rect.collidepoint(cur_x,cur_y)):
            if (self.frame % 10 > 5):
                self.button1.setImage(self.button1_image)
            else:
                self.button1.setImage(self.button1_image_b)

            if (mouse1):
                if (pygame.mixer.get_init()):
                    self.audio_se_ok.play()
                name_ent = Name_Entry(self.CurrentName)
                #print(name_ent.CurrentName)
                self.CurrentName = name_ent.CurrentName
                self.cfg.CurrentName = name_ent.CurrentName
                self.cfg.write()
        else:
            self.button1.setImage(self.button1_image)

        Label_Name = self.mfont2.render("Current Name :" + self.CurrentName, 1, (255,255,255))
        screen.blit(Label_Name, (0, 420))
        
        if (self.button2.rect.collidepoint(cur_x,cur_y)):
            if (self.frame % 10 > 5):
                self.button2.setImage(self.button2_image)
            else:
                self.button2.setImage(self.button2_image_b)

            if (mouse1):
                if (pygame.mixer.get_init()):
                    self.audio_se_ok.play()
        else:
            self.button2.setImage(self.button2_image)

        if (self.button3.rect.collidepoint(cur_x,cur_y)):
            if (self.frame % 10 > 5):
                self.button3.setImage(self.button3_image)
            else:
                self.button3.setImage(self.button3_image_b)

            if (mouse1):
                if (pygame.mixer.get_init()):
                    self.audio_se_ok.play()
                    if (self.cfg.ScreenShot == 0):
                        self.cfg.ScreenShot = 1
                    else:
                        self.cfg.ScreenShot = 0

                    self.cfg.write()
        else:
            self.button3.setImage(self.button3_image)

        if (self.cfg.ScreenShot == 0):
            Label_SC = self.mfont2.render("OFF", 1, (255,255,255))
        else:
            Label_SC = self.mfont2.render("ON", 1, (255,255,255))
            
        screen.blit(Label_SC, (self.button3_image.get_width()+12, self.button3.rect.y))
        
        if (self.button4.rect.collidepoint(cur_x,cur_y)):
            if (self.frame % 10 > 5):
                self.button4.setImage(self.button4_image)
            else:
                self.button4.setImage(self.button4_image_b)

            if (mouse1):
                if (pygame.mixer.get_init()):
                    self.audio_se_ok.play()
        else:
            self.button4.setImage(self.button4_image)

        if (mouse3):
            from Scene_Title import Scene_Title
            return Scene_Changer(Scene_Title(), screen)
