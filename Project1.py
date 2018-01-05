import pygame, datetime
import time
from pygame.locals import *
from sys import exit
import os

from Scene_Title import Scene_Title
######### INIT #########
FPS = 60 # frames per second, the general speed of the program

WINDOWWIDTH = 435 # size of window's width in pixels
WINDOWHEIGHT = 720 # size of windows' height in pixels

BGCOLOR = (0,0,0)

Scene = 0

######### INIT #########

def main():
    global FPSCLOCK, screen
    global Scene
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,32"
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), 0, 32)
    myfont = pygame.font.SysFont("Arial Black", 15)
    last_key = pygame.key.get_pressed()
    try:
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
    except:
        print("Mixer Init Failed!")

    try:
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 2048)
    except:
        print("Mixer Init Failed!")
        
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Bubble Pop Battle Remake")

    Scene = Scene_Title()

    while True:
        screen.fill(BGCOLOR)
        
        label = myfont.render("FPS:"+str(int(FPSCLOCK.get_fps())),  1, (255,255,0))

        newscene = Scene.update(screen)
        if (newscene != None):
            Scene = newscene

            try:
                if (type(Scene.NewScreen) != None):
                    screen = Scene.NewScreen
            except:
                print("", end='')


        keys = pygame.key.get_pressed()
        if (keys[K_F8] and not last_key[K_F8]):
            now = datetime.datetime.now()#time
            w_time=now.strftime('screenshot/%Y-%m-%d %H-%M-%S.png') #time-str

            try:
                if not os.path.exists('screenshot'):
                    os.makedirs('screenshot')

                pygame.image.save(screen.copy(), w_time)

                print("已儲存圖片：%s" % w_time)
            except Exception as e:
                print("儲存圖片時發生錯誤：")
                print(e)
        last_key = keys
        screen.blit(label, (0, WINDOWHEIGHT-20))
        pygame.display.flip()

        
        #FPSCLOCK.tick(FPS)
        FPSCLOCK.tick_busy_loop(FPS)
        
if __name__ == '__main__':
    main()
