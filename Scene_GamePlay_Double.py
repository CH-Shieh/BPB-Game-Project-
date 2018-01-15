import random, pygame, math, copy
import time, datetime, os
from random import randint
from pygame.locals import *
from sys import exit
from ani_base import *
from ani_combo import *
from Scene_Changer import Scene_Changer
from Netplay import Netplay

Debug_Mode = False

class Scene_GamePlay_Double:
    WINDOWWIDTH = 435 # size of window's width in pixels
    WINDOWHEIGHT = 720 # size of windows' height in pixels
    
    BALL_COLOR_BG = ((224,0,0), (0,224,0), (0,0,224), (224,224,0))
    BALL_COLOR_FG = ((255,192,192), (192,255,192), (192,128,255), (255,255,192))

    BALL_IMG = []

    BALL_SIZE = 40
    BALL_SPEED = 10

    Black_BG = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT))
    Black_BG.fill((0,0,0))
    Black_BG.set_alpha(192)

    Black_BG_Full = pygame.Surface((1920,1920))
    Black_BG_Full.fill((0,0,0))
    Black_BG_Full.set_alpha(127)

    Img_BG_FileNames = ["Graphics/bg0001.png","Graphics/bg0002.png","Graphics/bg0003.png","Graphics/bg0004.png","Graphics/bg0005.png"]
    Img_BG = pygame.image.load(Img_BG_FileNames[randint(0,len(Img_BG_FileNames)-1)]).convert()
    Img_BG.blit(Black_BG_Full,(0,0))
    Img_BG = pygame.transform.scale(Img_BG,(930,WINDOWHEIGHT))
    Black_BG_Full.set_alpha(192)
    audio_bgm_filename = ["Audio/BGM/bgm_01 (2).mp3","Audio/BGM/bgm_02 (2).mp3","Audio/BGM/bgm_03 (2).mp3"]
    audio_se_ko_filename = "Audio/SE/21_ko1.wav"
    audio_se_side_filename = "Audio/SE/sfx_rotatefail.wav"
    audio_se_shoot_filename = "Audio/SE/sfx_rotate.wav"
    audio_se_lockdown_filename = "Audio/SE/sfx_lockdown.wav"
    audio_se_change_filename = "Audio/SE/sfx_hold.wav"
    audio_se_clear_filename = "Audio/SE/sfx_harddrop.wav"
    audio_se_hurryup_filename = "Audio/SE/18_hurryup.wav"

    audio_se_timeup_filename = "Audio/SE/sfx_gameover.wav"

    audio_se_win_filename = "Audio/SE/win.wav"
    audio_se_lose_filename = "Audio/SE/sfx_gameover.wav"
    audio_se_combo_filename_base = "Audio/SE/sfx_combo%d.wav"

    graphics_win_filename = "Graphics/1on1_rank_win.png"
    graphics_lose_filename = "Graphics/1on1_rank_lose.png"
    def __init__(self, network = None, gamemode = 1):
        #player1
        self.BALL_DATA = []
        self.CURRENT_BALL = []
        self.CURRENT_BALL_X = 0.0
        self.CURRENT_BALL_Y = 0.0
        self.CURRENT_BALL_VEC_X = 0.0
        self.CURRENT_BALL_VEC_Y = 0.0
        #player2
        self.PC_time = time.time()
        self.PC_level = 0 #1~4 1最難
        self.BALL_DATA2 = []#x範圍530~930
        self.CURRENT_BALL2= []
        self.CURRENT_BALL_X2 = 0.0#發射點730
        self.CURRENT_BALL_Y2 = 0.0#發射點700
        self.CURRENT_BALL_VEC_X2 = 0.0
        self.CURRENT_BALL_VEC_Y2 = 0.0
        self.BALL_IMG = []
        self.check_data=[[],[]]
        #### 對應對戰模式用
        self.mode = gamemode
        self.MULTIPLAYER_EXWIDE = 60
        self.DAMAGE_LOCAL = 0
        self.DAMAGE_RIVAL = 0
        self.TIMELEFT = 99
        self.BALL_DAMAGE = 0
        self.ComboCount_LOCAL = 0
        self.ComboCount_RIVAL = 0
        self.MaxComboCount_LOCAL = 0
        self.MaxComboCount_RIVAL = 0
        self.Score_LOCAL = 0
        self.Score_RIVAL = 0
        self.KOCOUNT_LOCAL = 0
        self.KOCOUNT_RIVAL = 0
        self.FREEZETIME = False
        self.gametime = time.time()
        self.ballimg_init()


        
        ####球陣列初始化
        for j in range(20):
            k = []
            for i in range(10-j%2):
                k.append(-1)
            self.BALL_DATA.append(k)
            self.BALL_DATA2.append(k.copy())
        
        ####改解析度
        self.NewScreen = pygame.display.set_mode((self.WINDOWWIDTH*2+self.MULTIPLAYER_EXWIDE,self.WINDOWHEIGHT), 0, 32)

        ####外部類別初始化
        ani_base.init(self.WINDOWWIDTH, self.WINDOWHEIGHT)

        ####字型初始化
        self.myfont = pygame.font.SysFont("SimHei", 15)
        self.myfont2 = pygame.font.SysFont("Arial Black", 24)
        self.myfont4 = pygame.font.SysFont("Arial Black", 48)
        self.myfont3 = pygame.font.SysFont("Arial Black", 72)


        ####球初始化
        for i in range(8):
            for j in range(len(self.BALL_DATA[i])):
                self.BALL_DATA[i][j] = randint(0,len(self.BALL_IMG)-1)

            for j in range(len(self.BALL_DATA2[i])):
                self.BALL_DATA2[i][j] = randint(0,len(self.BALL_IMG)-1)

        for j in range(3):
            self.CURRENT_BALL.append(randint(0,len(self.BALL_IMG) -1))
            self.CURRENT_BALL2.append(randint(0,len(self.BALL_IMG) -1))
        ####音效初始化
        try:
            
            pygame.mixer.music.load(self.audio_bgm_filename[randint(0,len(self.audio_bgm_filename)-1)])
            pygame.mixer.music.play(-1)

            self.audio_se_ko = pygame.mixer.Sound(self.audio_se_ko_filename)
            self.audio_se_side = pygame.mixer.Sound(self.audio_se_side_filename)
            self.audio_se_shoot = pygame.mixer.Sound(self.audio_se_shoot_filename)
            self.audio_se_lockdown = pygame.mixer.Sound(self.audio_se_lockdown_filename)
            self.audio_se_change = pygame.mixer.Sound(self.audio_se_change_filename)
            self.audio_se_clear = pygame.mixer.Sound(self.audio_se_clear_filename)
            self.audio_se_hurryup = pygame.mixer.Sound(self.audio_se_hurryup_filename)

            self.audio_se_timeup = pygame.mixer.Sound(self.audio_se_timeup_filename)

            self.audio_se_win = pygame.mixer.Sound(self.audio_se_win_filename)
            self.audio_se_lose = pygame.mixer.Sound(self.audio_se_lose_filename)
    
            self.audio_se_combo = []
            for i in range(20):
                self.audio_se_combo.append(pygame.mixer.Sound((self.audio_se_combo_filename_base % (i+1))))

        except Exception as e:
            print(e)

        ####圖片載入
        self.graphics_win = pygame.image.load(self.graphics_win_filename).convert_alpha()
        self.graphics_lose = pygame.image.load(self.graphics_lose_filename).convert_alpha()
        
        ####連線
        self.network = network
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@PC新增部分@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        
    def PC_think(self):#太強
        for run in range(2):
            for i in range(len(self.BALL_DATA2)-1,-1,-1):#搜尋第1顆球
                for j in range(len(self.BALL_DATA2[i])):
                    if self.BALL_DATA2[i][j] == -1:
                        self.check_data=[[],[]]
                        if(self.check_hit(j,i,self.BALL_DATA2,self.CURRENT_BALL2[0],3)):#判定是否有三顆以上同色球
                            if not(self.PC_check_route(j,i)):continue #確認路徑上的障礙 目標(x,y)
                            n=self.PC_check_impact(j,i)
                            if n==0:continue
                            BALL_DATA_x=j*40+(i%2)*20+530+20
                            BALL_DATA_y=i*40
                            if n==2:BALL_DATA_x+=5
                            elif n==3:BALL_DATA_x-=5
                            #print("PC發射",i,j,n)
                            self.PC_shoot_ball(BALL_DATA_x,BALL_DATA_y)
                            return
            #print("第一顆找不到地方可以放")
            self.CURRENT_BALL2.insert(0, self.CURRENT_BALL2.pop(1))
                    

        for run in range(2):
            for i in range(len(self.BALL_DATA2)-1,-1,-1):
                for j in range(len(self.BALL_DATA2[i])):
                    if self.BALL_DATA2[i][j] == -1:
                        self.check_data=[[],[]]
                        if (self.check_hit(j,i,self.BALL_DATA2,self.CURRENT_BALL2[0],2)):#判定是否有兩顆以上同色球
                            if not(self.PC_check_route(j,i)):continue #確認路徑上的障礙 目標(x,y)
                            n=self.PC_check_impact(j,i)
                            if n==0:continue
                            BALL_DATA_x=j*40+(i%2)*20+530+20
                            BALL_DATA_y=i*40
                            if n==2:BALL_DATA_x+=5
                            elif n==3:BALL_DATA_x-=5
                            #print("PC發射",i,j,n)
                            self.PC_shoot_ball(BALL_DATA_x,BALL_DATA_y)
                            return
            #print("第一顆找不到地方可以放2")
            self.CURRENT_BALL2.insert(0, self.CURRENT_BALL2.pop(1))
        i = randint(0,10)
        j = randint(0,9-i%2)
        BALL_DATA_x=j*40+(i%2)*20+530+20
        BALL_DATA_y=i*40
        #print("PC隨機發射",i,j)
        self.PC_shoot_ball(BALL_DATA_x,BALL_DATA_y)
                       
    def PC_check_route(self,j,i):#確認路徑上有無障礙物
        x1=j*40+(i%2)*20+530+20
        y1=i*40
        
        #y=ax+b
        #斜率a=(y1-y2)/(x1-x2)
        #b=(y1+y2)-(x1+x2)*a/2
        #距離d = (math.abs(a*x-y+b))/math.sqrt(a**2+1)

        x2 = 730
        y2 = 700
        a=10000#防止垂直斜率無限大
        if x1!=x2: a = (y1-y2)/(x1-x2)
        
        b = ((y1+y2)-(x1+x2)*a)/2
        
        
        for y in range(16,i-1,-1):
            for x in range(len(self.BALL_DATA2[y])):
                BALL_DATA_x=x*40+(y%2)*20+530+20
                BALL_DATA_y=y*40
                distance = (abs(a*BALL_DATA_x-BALL_DATA_y+b))/math.sqrt(a**2+1)#(y,x)到軌跡上的垂直距離
                if distance<=self.BALL_SIZE*3/4:#接觸範圍
                    if self.BALL_DATA2[y][x] != -1:
                        return False
        return True
        
    def PC_check_impact(self,j,i):#檢查能否準確的停在瞄準的位置
        x1=j*40+(i%2)*20+530+20
        y1=i*40
        x2 = 730
        y2 = 700
        a=10000#防止垂直斜率無限大
        if x1!=x2: a = (y1-y2)/(x1-x2)

        if a<0 and i>0:#朝右邊發射
            if j+i%2<len(self.BALL_DATA2[i-1]):
                if self.BALL_DATA2[i-1][j+i%2] != -1:
                    #print("1目標右上角有東西可以擋")
                    return 1
            if j-(1-i%2)>=0:
                if self.BALL_DATA2[i-1][j-(1-i%2)] != -1:
                    #print("1目標左上角有東西可以擋")
                    return 3
            if j+1<len(self.BALL_DATA2[i]):    
                if self.BALL_DATA2[i][j+1] !=-1:
                    #print("目標右邊有東西可以擋")
                    return 
        elif a>0 and i>0:#朝左邊發射
            if j-(1-i%2)>=0:
                if self.BALL_DATA2[i-1][j-(1-i%2)] != -1:
                    #print("2目標左上角有東西可以擋")
                    return 1
            if j+i%2<len(self.BALL_DATA2[i-1]):    
                if self.BALL_DATA2[i-1][j+i%2] != -1:
                    #print("2目標右上角有東西可以擋")
                    return 2
            if j-(1-i%2)>=0:
                if self.BALL_DATA2[i][j-1] !=-1:
                    #print("目標左邊有東西可以擋")
                    return 3
        #print("X:",i,j)
        return 0
    def PC_shoot_ball(self,x,y):#電腦發射(已完成)
        SPEED = self.BALL_SPEED + min(10, self.ComboCount_RIVAL)
        dd = self.divto(x - 730,y - 700)
        self.CURRENT_BALL_VEC_X2 = math.sqrt(((x - 730)**2) / dd)* SPEED
        if (x < 730):
            self.CURRENT_BALL_VEC_X2 *= -1
        self.CURRENT_BALL_VEC_Y2 = math.sqrt(((y - 700)**2)  / dd)* SPEED

        if (self.CURRENT_BALL_VEC_Y2 == 0):
            self.CURRENT_BALL_VEC_Y2 = 0.5* SPEED
            
            if (abs(self.CURRENT_BALL_VEC_X2 / self.CURRENT_BALL_VEC_Y2) > 1.6):
            #print("force angle")
                self.CURRENT_BALL_VEC_X2 = 0.8 * SPEED
                if (x < 730):
                    self.CURRENT_BALL_VEC_X2 = -0.8 * SPEED
                self.CURRENT_BALL_VEC_Y2 = 0.5 * SPEED
        self.CURRENT_BALL_X2 = 730 - self.BALL_SIZE/2
        self.CURRENT_BALL_Y2 = 700
        self.CURRENT_BALL2.append(randint(0,len(self.BALL_IMG)-1))
        
        if (pygame.mixer.get_init()):
            self.audio_se_shoot.play()
    
    def PC_ball_judge(self):#PC球運行中處理(已完成)(效能提升)
        self.CURRENT_BALL_X2 += self.CURRENT_BALL_VEC_X2
        self.CURRENT_BALL_Y2 -= self.CURRENT_BALL_VEC_Y2

        ##球接觸判定
        y = int(self.CURRENT_BALL_Y2/40)
        x = int((self.CURRENT_BALL_X2-530-20-y%2*20)/40)

        for i in range(y-2,y+3):
            for j in range(x-2,x+3):
                if i<0 or i>=len(self.BALL_DATA2) or j<0 or j>=len(self.BALL_DATA2[i]):continue
                if(self.BALL_DATA2[i][j]!=-1):#該位置有球
                    BALL_DATA_x=j*40+(i%2)*20+530
                    BALL_DATA_y=i*40
                    if(BALL_DATA_y>self.CURRENT_BALL_Y2):
                        continue
                    rect=math.sqrt((self.CURRENT_BALL_X2+self.CURRENT_BALL_VEC_X2-BALL_DATA_x)**2+(self.CURRENT_BALL_Y2-self.CURRENT_BALL_VEC_Y2-BALL_DATA_y)**2)#距離判定
                    if(rect<=self.BALL_SIZE*3/4):#判定程度
                        #print("碰撞位置:",i,j)
                        self.PC_search_space()
                        if (pygame.mixer.get_init()):
                            self.audio_se_lockdown.play()                        
                        return
  
        ##左右邊界判定
        if (self.CURRENT_BALL_X2 + self.CURRENT_BALL_VEC_X2 > 930 - self.BALL_SIZE/2 or self.CURRENT_BALL_X2 + self.CURRENT_BALL_VEC_X2 < 530-self.BALL_SIZE/2):
            self.CURRENT_BALL_VEC_X2 *= -1
            if (pygame.mixer.get_init()):
                self.audio_se_side.play()
        ##上下邊界判定
        if (self.CURRENT_BALL_Y2 - self.CURRENT_BALL_VEC_Y2 < 0):
            self.PC_search_space()#搜尋最近的空格擺放發射的球
            if (pygame.mixer.get_init()):
                self.audio_se_lockdown.play()

    def PC_search_space(self):#搜尋最近的空格擺放發射的球(已完成)
        #print("PC search")
        self.BALL_DAMAGE = 0
        rect2_min=100
        mx=0
        my=0
        y = int(self.CURRENT_BALL_Y2/40)
        x = int((self.CURRENT_BALL_X2-530-y%2*20)/40)

        for r in range(y-2,y+3):
            for s in range(x-2,x+3):
                if r<0 or r>=len(self.BALL_DATA2) or s<0 or s>=len(self.BALL_DATA2[r]):continue
                if(self.BALL_DATA2[r][s]==-1):#位置為空
                    BALL_DATA_x=(s*40+(r%2)*20)+530
                    BALL_DATA_y=r*40
                    rect2=math.sqrt((self.CURRENT_BALL_X2-BALL_DATA_x)**2+(self.CURRENT_BALL_Y2-BALL_DATA_y)**2)
                    if (rect2_min>rect2):
                        rect2_min=rect2
                        mx=s
                        my=r
                        #print("更新最後擺放位置:",my,mx)
        #print(my,mx)
        #print(self.CURRENT_BALL[0])
        self.BALL_DATA2[my][mx]=self.CURRENT_BALL2[0]
        #print(self.BALL_DATA[my][mx])
        self.check_data=[[],[]]
        if(self.check_hit(mx,my,self.BALL_DATA2,self.CURRENT_BALL2[0],3)):#判定是否有三顆以上同色球
            #print("執行search,搜尋將破壞的球")
            self.search(mx,my,0,self.BALL_DATA2,self.CURRENT_BALL2,2)#搜尋將破壞的球
            self.float_detect(self.BALL_DATA2,2)#進行浮空偵測
        self.CURRENT_BALL2.pop(0)
        self.CURRENT_BALL_VEC_X2 = 0
        self.CURRENT_BALL_VEC_Y2 = 0

        if (self.BALL_DAMAGE > 0):
            self.ComboCount_RIVAL +=1
            ani_combo(self.ComboCount_RIVAL,730,500, 1, -5, 0, 0.25)
            self.Score_RIVAL += self.BALL_DAMAGE*5*self.ComboCount_RIVAL
            #傷害公式 = (球數 + Combo) /9
            self.DAMAGE_BASE = math.floor((self.BALL_DAMAGE + self.ComboCount_RIVAL)/9)
            self.DAMAGE_RIVAL -= self.DAMAGE_BASE
            if (self.DAMAGE_RIVAL < 0):
                self.DAMAGE_LOCAL -= self.DAMAGE_RIVAL
                self.DAMAGE_RIVAL = 0

            if (self.network != None):
                newdata = "BPB,/DAMAGE,/" + str(math.floor(self.DAMAGE_BASE)) + "\n"
                str_data = bytes(newdata, "utf-8")
                self.network.TCP_socket.send(str_data)

            if (pygame.mixer.get_init()):
                self.audio_se_clear.play()

                self.audio_se_combo[min(19, self.ComboCount_RIVAL-1)].play()
        else:
            #self.ComboCount_RIVAL = max(self.ComboCount_RIVAL, self.ComboCount_RIVAL)
            self.ComboCount_RIVAL = 0
        #DAMAGE處理
        if ((self.DAMAGE_RIVAL > 1 and self.ComboCount_RIVAL == 0)):
            while (self.DAMAGE_RIVAL > 1):
                self.DAMAGE_RIVAL = max(self.DAMAGE_RIVAL - 2, 0)
                new_row = []
                for j in range(10):
                    new_row.append(randint(0,len(self.BALL_IMG)-1))

                new_row2 = []
                for j in range(9):
                    new_row2.append(randint(0,len(self.BALL_IMG)-1))
                    
                self.BALL_DATA2[2:(len(self.BALL_DATA2)-1)] = self.BALL_DATA2[0:(len(self.BALL_DATA2)-2)]
                self.BALL_DATA2[0]=new_row
                self.BALL_DATA2[1]=new_row2

        ##向下處理
        if (self.find_lowest_ball2() < 8):
            new_row = []
            for j in range(10):
                new_row.append(randint(0,len(self.BALL_IMG)-1))

            new_row2 = []
            for j in range(9):
                new_row2.append(randint(0,len(self.BALL_IMG)-1))
                    
            self.BALL_DATA2[2:(len(self.BALL_DATA2)-1)] = self.BALL_DATA2[0:(len(self.BALL_DATA2)-2)]
            self.BALL_DATA2[0]=new_row
            self.BALL_DATA2[1]=new_row2
            
        #Will be removed in future
        '''
        if (self.DAMAGE_RIVAL > 1 and self.ComboCount_LOCAL == 0):
            while (self.DAMAGE_RIVAL > 1):
                self.DAMAGE_RIVAL -= 2
                new_row = []
                for j in range(10):
                    new_row.append(randint(0,len(self.BALL_IMG)-1))

                new_row2 = []
                for j in range(9):
                    new_row2.append(randint(0,len(self.BALL_IMG)-1))
                    
                self.BALL_DATA2[2:(len(self.BALL_DATA2)-1)] = self.BALL_DATA2[0:(len(self.BALL_DATA2)-2)]
                self.BALL_DATA2[0]=new_row
                self.BALL_DATA2[1]=new_row2
        '''
        #KO'd JUDGE
        if (self.find_lowest_ball2() > 16):
            self.KOCOUNT_LOCAL += 1
            if (pygame.mixer.get_init()):
                self.audio_se_ko.play()
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

    
    def init_network(self, network):
        self.network = network
        
    def ballimg_init(self):

        for j in range(len(self.BALL_COLOR_BG)):
            new_ball = pygame.Surface((self.BALL_SIZE,self.BALL_SIZE))
            new_ball.set_colorkey((0,0,0))
            pygame.draw.circle(new_ball, self.BALL_COLOR_BG[j], (round(self.BALL_SIZE/2),round(self.BALL_SIZE/2)), round(self.BALL_SIZE/2))
            for i in range(math.floor(self.BALL_SIZE/2)):
                clr = (self.BALL_COLOR_BG[j][0] + (self.BALL_COLOR_FG[j][0] - self.BALL_COLOR_BG[j][0])*i*2/(self.BALL_SIZE)  ,self.BALL_COLOR_BG[j][1] + (self.BALL_COLOR_FG[j][1] - self.BALL_COLOR_BG[j][1])*i*2/(self.BALL_SIZE),self.BALL_COLOR_BG[j][2] + (self.BALL_COLOR_FG[j][2] - self.BALL_COLOR_BG[j][2])*i*2/(self.BALL_SIZE))
                pygame.draw.circle(new_ball, clr, (int(self.BALL_SIZE/2+i/2),int(self.BALL_SIZE/2+i/2)), math.floor(self.BALL_SIZE/2)-i)

            self.BALL_IMG.append(new_ball)

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@程式共用部分@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            
    def float_detect(self,BALL_DATA,player):#浮空偵測(已修改)

        reg_data = copy.deepcopy(BALL_DATA)
        reg_data[0][0] = -1
        for i in range(len(BALL_DATA)):
            self.float_search(reg_data,i,0)
        for i in range(len(reg_data)):
            for j in range(len(reg_data[i])):
                if reg_data[i][j]!=-1:
                    ani_base(self.BALL_IMG[BALL_DATA[i][j]], j*40+(i%2)*20+530*(player-1),i*40, randint(0,2)-1, randint(10,20)*-1 , 0, 1 )
                    self.BALL_DAMAGE +=1
                    BALL_DATA[i][j]=-1
                    
    def float_search(self,reg_data,x,y):#搜尋偵測(已修改)
        if x<0 or y<0 or x>9-y%2: return
        if reg_data[y][x] != -1:
            reg_data[y][x]=-1
            for i in range(-1,2):
                if i==0:
                    self.float_search(reg_data,x-1,y)
                    self.float_search(reg_data,x+1,y)
                else:
                    for j in range(-1+y%2,1+y%2):
                        self.float_search(reg_data,x+j,y+i)
                        
    def Debug_display(self,screen):
        font = pygame.font.SysFont("SimHei", 13)
        for y in range(len(self.BALL_DATA)):
            for x in range(len(self.BALL_DATA[y])):
                text=font.render(str(y)+","+str(x),True,(255,255,255))
                pygame.draw.circle(screen, (255,255,255), (x*40+20+(y%2)*20,y*40+20), 20,1)
                screen.blit(text,(x*40+10+((y)%2)*20,y*40+12))
                pygame.draw.circle(screen, (255,255,255), (x*40+20+(y%2)*20+530,y*40+20), 20,1)
                screen.blit(text,(x*40+10+((y)%2)*20+530,y*40+12))
        
        
               

    def check_hit(self,x,y,BALL_DATA,CURRENT_BALL,n):#搜尋三顆同色球(已修改)
        self.check_data[0].append(x)
        self.check_data[1].append(y)
        #print("data:",self.check_data,y,x)
        if(len(self.check_data[0])>=n):
            return True
        for i in range(y-1,y+2):
            for j in range(x-((y+1)%2),x+(y%2)+1):
                cy=i
                cx=j
                if(i==y and j==x and y%2==0):
                    cx+=1
                elif(i==y and j==x and y%2==1):
                    cx-=1
                if(cy<0 or cx<0 or cy>16 or cx>9-cy%2):continue
                if(BALL_DATA[cy][cx]==CURRENT_BALL):
                    boolean=True
                    for s in range(0,len(self.check_data[0])):
                        if(self.check_data[0][s]==cx and self.check_data[1][s]==cy):
                            boolean=False
                            break
                    if(boolean):
                        if(self.check_hit(cx,cy,BALL_DATA,CURRENT_BALL,n)):
                            return True
                    
        return False


    def search(self,x,y,level,BALL_DATA,CURRENT_BALL,player):#搜尋同色的球,將其破壞(已修改)
 
        level+=1
        for i in range(y-1,y+2):
            for j in range(x-((y+1)%2),x+(y%2)+1):
                cy=i
                cx=j
                if(i==y and j==x and y%2==0):
                    cx+=1
                elif(i==y and j==x and y%2==1):
                    cx-=1
                if(cy<0 or cx<0 or cy>16 or cx>9-cy%2):continue

                if(BALL_DATA[cy][cx]==CURRENT_BALL[0]):
                    mx=2
                    if(j==x-((y+1)%2)):mx=-2
                    #print(cx*40+(cy%2)*20+530*(player-1),cy*40)
                    ani_base(self.BALL_IMG[CURRENT_BALL[0]], cx*40+(cy%2)*20+530*(player-1),cy*40, randint(0,2)-1, randint(10,20)*-1 , 0, 1 ) 
                    BALL_DATA[cy][cx]=-1
                    self.BALL_DAMAGE +=1
                    self.search(cx,cy,level,BALL_DATA,CURRENT_BALL,player)

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    
    def check_empty(self,x,y):
        if (y > 680 or x > 360):
            return True

        if (y < 0):
            return False
        pos_y =  math.floor(y / self.BALL_SIZE)
        pos_x = 0
        if (pos_y % 2 > 0):
            if (x < self.BALL_SIZE / 2 or x > 400 - self.BALL_SIZE / 2):
                return True
            else:
                pos_x = math.floor((x-self.BALL_SIZE/2)/self.BALL_SIZE)
        else:
            pos_x = math.floor(x / self.BALL_SIZE)
        try:
            if (self.BALL_DATA[pos_y][pos_x] != -1):
                return False
        except:
            print("偵錯:",pos_y,pos_x)
        return True

    def find_lowest_ball(self):

        for i in range(len(self.BALL_DATA)):
            j = False
            for k in self.BALL_DATA[i]:
                if (k != -1):
                    j = True
                    break

            if (j == False):
                return i
        return 0
    def find_lowest_ball2(self):
        for i in range(len(self.BALL_DATA2)):
            j = False
            for k in self.BALL_DATA2[i]:
                if (k != -1):
                    j = True
                    break

            if (j == False):
                return i
        return 0
    
    def divto(self,a,b):
        return (abs(a)**2+abs(b)**2)

    def draw_ball(self,screen, color, x, y):
        screen.blit(self.BALL_IMG[color], (x,y))
        
    def shoot_ball(self):

        SPEED = self.BALL_SPEED + min(10, self.ComboCount_LOCAL)
        dd = self.divto(self.cur_x - 200,self.cur_y - 700)
        self.CURRENT_BALL_VEC_X = math.sqrt(((self.cur_x - 200)**2) / dd)* SPEED
        if (self.cur_x < 200):
            self.CURRENT_BALL_VEC_X *= -1
        self.CURRENT_BALL_VEC_Y = math.sqrt(((self.cur_y - 700)**2)  / dd)* SPEED

        if (self.CURRENT_BALL_VEC_Y == 0):
            self.CURRENT_BALL_VEC_Y = 0.5* SPEED
            
        if (abs(self.CURRENT_BALL_VEC_X / self.CURRENT_BALL_VEC_Y) > 2.0):
            #print("force angle")
            self.CURRENT_BALL_VEC_X = 1.0 * SPEED
            if (self.cur_x < 200):
                self.CURRENT_BALL_VEC_X = -1.0 * SPEED
            self.CURRENT_BALL_VEC_Y = 0.5 * SPEED
        self.CURRENT_BALL_X = 200 - self.BALL_SIZE/2
        self.CURRENT_BALL_Y = 700
        self.CURRENT_BALL.append(randint(0,len(self.BALL_IMG)-1))
        if (self.CURRENT_BALL[1] == self.CURRENT_BALL[2] and self.CURRENT_BALL[2] == self.CURRENT_BALL[3]):
            self.CURRENT_BALL[3] = (self.CURRENT_BALL[3] +1)%len(self.BALL_IMG)
        if (pygame.mixer.get_init()):
            self.audio_se_shoot.play()

        if (self.network != None):
            if(self.network.TCP_Connected == True):
                newdata2 = "BPB,/CurrentBall,/"
                for j in range(len(self.CURRENT_BALL)):
                    newdata2 = newdata2 + str(self.CURRENT_BALL[j])
                    if (not j == len(self.CURRENT_BALL) - 1):
                        newdata2 = newdata2 + ","
                    else:
                        newdata2 = newdata2 + "\n"
                str_data2 = bytes(newdata2, "utf-8")
                self.network.TCP_socket.send(str_data2)
                    
    def search_space(self):#搜尋最近的空格擺放發射的球(效能提升)

        self.BALL_DAMAGE = 0
        rect2_min=100
        mx=0
        my=0
        y = int(self.CURRENT_BALL_Y/40)
        x = int((self.CURRENT_BALL_X-y%2*20)/40)
        for r in range(y-2,y+3):
            for s in range(x-2,x+3):
                if r<0 or r>=len(self.BALL_DATA) or s<0 or s>=len(self.BALL_DATA[r]):continue
                if(self.BALL_DATA[r][s]==-1):#位置為空
                    BALL_DATA_x=s*40+(r%2)*20
                    BALL_DATA_y=r*40
                    rect2=math.sqrt((self.CURRENT_BALL_X-BALL_DATA_x)**2+(self.CURRENT_BALL_Y-BALL_DATA_y)**2)
                    if (rect2_min>rect2):
                        rect2_min=rect2
                        mx=s
                        my=r
                        #print("更新最後擺放位置:",my,mx)
        #print(my,mx)
        #print(self.CURRENT_BALL[0])
        self.BALL_DATA[my][mx]=self.CURRENT_BALL[0]
        #print(self.BALL_DATA[my][mx])
        self.check_data=[[],[]]
        if(self.check_hit(mx,my,self.BALL_DATA,self.CURRENT_BALL[0],3)):#判定是否有三顆以上同色球
            #print("執行search,搜尋將破壞的球")
            self.search(mx,my,0,self.BALL_DATA,self.CURRENT_BALL,1)#搜尋將破壞的球
            self.float_detect(self.BALL_DATA,1)#進行浮空偵測
        self.CURRENT_BALL.pop(0)
        self.CURRENT_BALL_VEC_X = 0
        self.CURRENT_BALL_VEC_Y = 0
        
        if (self.BALL_DAMAGE > 0):
            self.ComboCount_LOCAL +=1
            ani_combo(self.ComboCount_LOCAL, self.cur_x, self.cur_y, 1, -5, 0, 0.25)
            self.Score_LOCAL += self.BALL_DAMAGE*5*self.ComboCount_LOCAL
            #傷害公式 = (球數 + Combo) /9
            self.DAMAGE_BASE = math.floor((self.BALL_DAMAGE + self.ComboCount_LOCAL)/9)
            self.DAMAGE_LOCAL -= self.DAMAGE_BASE
            if (self.DAMAGE_LOCAL < 0):
                self.DAMAGE_RIVAL -= self.DAMAGE_LOCAL
                self.DAMAGE_LOCAL = 0

            if (self.network != None):
                newdata = "BPB,/DAMAGE,/" + str(math.floor(self.DAMAGE_BASE)) + "\n"
                str_data = bytes(newdata, "utf-8")
                self.network.TCP_socket.send(str_data)

                newdata = "BPB,/SCORE,/" + str(self.Score_LOCAL) + "\n"
   
                str_data = bytes(newdata, "utf-8")
                self.network.TCP_socket.send(str_data)

                newdata = "BPB,/COMBO,/" + str(self.ComboCount_LOCAL) + "\n"
   
                str_data = bytes(newdata, "utf-8")
                self.network.TCP_socket.send(str_data)
            if (pygame.mixer.get_init()):
                self.audio_se_clear.play()

                self.audio_se_combo[min(19, self.ComboCount_LOCAL-1)].play()
                
        else:
            self.MaxComboCount_LOCAL = max(self.ComboCount_LOCAL, self.MaxComboCount_LOCAL)
            self.ComboCount_LOCAL = 0

        #DAMAGE處理
            
        if ((self.DAMAGE_LOCAL > 1 and self.ComboCount_LOCAL == 0)):
            while (self.DAMAGE_LOCAL > 1):
                self.DAMAGE_LOCAL = max(self.DAMAGE_LOCAL - 2, 0)
                new_row = []
                for j in range(10):
                    new_row.append(randint(0,len(self.BALL_IMG)-1))

                new_row2 = []
                for j in range(9):
                    new_row2.append(randint(0,len(self.BALL_IMG)-1))
                    
                self.BALL_DATA[2:(len(self.BALL_DATA)-1)] = self.BALL_DATA[0:(len(self.BALL_DATA)-2)]
                self.BALL_DATA[0]=new_row
                self.BALL_DATA[1]=new_row2

        ##向下處理
        if (self.find_lowest_ball() < 8):
            new_row = []
            for j in range(10):
                new_row.append(randint(0,len(self.BALL_IMG)-1))

            new_row2 = []
            for j in range(9):
                new_row2.append(randint(0,len(self.BALL_IMG)-1))
                    
            self.BALL_DATA[2:(len(self.BALL_DATA)-1)] = self.BALL_DATA[0:(len(self.BALL_DATA)-2)]
            self.BALL_DATA[0]=new_row
            self.BALL_DATA[1]=new_row2
        #Will be removed in future
        '''
        if (self.DAMAGE_RIVAL > 1 and self.ComboCount_LOCAL == 0):
            while (self.DAMAGE_RIVAL > 1):
                self.DAMAGE_RIVAL -= 2
                new_row = []
                for j in range(10):
                    new_row.append(randint(0,len(self.BALL_IMG)-1))

                new_row2 = []
                for j in range(9):
                    new_row2.append(randint(0,len(self.BALL_IMG)-1))
                    
                self.BALL_DATA2[2:(len(self.BALL_DATA2)-1)] = self.BALL_DATA2[0:(len(self.BALL_DATA2)-2)]
                self.BALL_DATA2[0]=new_row
                self.BALL_DATA2[1]=new_row2
        '''
        #KO'd JUDGE
        if (self.find_lowest_ball() > 16):
            self.KOCOUNT_RIVAL += 1
            if (pygame.mixer.get_init()):
                self.audio_se_ko.play()
            if (not self.network == None):
                if (self.network.TCP_Connected == True):
                    newdata = "BPB,/KO,/" + str(self.KOCOUNT_RIVAL) + "\n"
   
                    str_data = bytes(newdata, "utf-8")
                    self.network.TCP_socket.send(str_data)

    def ball_judge(self):#(效能提升)
        self.CURRENT_BALL_X += self.CURRENT_BALL_VEC_X
        self.CURRENT_BALL_Y -= self.CURRENT_BALL_VEC_Y

        ##球接觸判定
        for i in range(0,len(self.BALL_DATA)-1):
            for j in range(0,len(self.BALL_DATA[i])-(i%2)*1):
                if(self.BALL_DATA[i][j]!=-1):#該位置有球
                    BALL_DATA_x=j*40+(i%2)*20
                    BALL_DATA_y=i*40
                    if(BALL_DATA_y>self.CURRENT_BALL_Y):
                        continue
                    rect=math.sqrt((self.CURRENT_BALL_X+self.CURRENT_BALL_VEC_X-BALL_DATA_x)**2+(self.CURRENT_BALL_Y-self.CURRENT_BALL_VEC_Y-BALL_DATA_y)**2)#距離判定
                    if(rect<=self.BALL_SIZE*3/4):#判定程度
                        #print("碰撞位置:",i,j)
                        self.search_space()
                        if (pygame.mixer.get_init()):
                            self.audio_se_lockdown.play()                        
                        return

        ##左右邊界判定
        if (self.CURRENT_BALL_X + self.CURRENT_BALL_VEC_X > 400 - self.BALL_SIZE/2 or self.CURRENT_BALL_X + self.CURRENT_BALL_VEC_X < -self.BALL_SIZE/2):
            self.CURRENT_BALL_VEC_X *= -1
            if (pygame.mixer.get_init()):
                self.audio_se_side.play()
        ##上下邊界判定
        if (self.CURRENT_BALL_Y - self.CURRENT_BALL_VEC_Y < 0):
            self.search_space()#搜尋最近的空格擺放發射的球
            if (pygame.mixer.get_init()):
                self.audio_se_lockdown.play()
                

    def update(self,screen):
        # 退出事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEMOTION:
                self.cur_x, self.cur_y = event.pos
            elif event.type == KEYDOWN:
                if (event.key == K_SPACE):
                    if (self.CURRENT_BALL_VEC_X == 0 and self.CURRENT_BALL_VEC_Y == 0):
                        self.CURRENT_BALL.insert(0, self.CURRENT_BALL.pop(1))
                        if (pygame.mixer.get_init()):
                            self.audio_se_change.play()
                if (event.key == K_a):
                    self.DAMAGE_LOCAL = min(self.DAMAGE_LOCAL+1, 13)
                if (event.key == K_z):
                    self.DAMAGE_LOCAL = max(self.DAMAGE_LOCAL-1, 0)

            elif event.type == MOUSEBUTTONDOWN:
                self.cur_x, self.cur_y = event.pos
                if (event.button == 1):
                    if (self.FREEZETIME == False):
                        if (self.CURRENT_BALL_VEC_X == 0 and self.CURRENT_BALL_VEC_Y == 0 and self.find_lowest_ball() <= 16):
                            self.shoot_ball()
                elif (event.button == 3):
                    if (self.CURRENT_BALL_VEC_X == 0 and self.CURRENT_BALL_VEC_Y == 0):
                        self.CURRENT_BALL.insert(0, self.CURRENT_BALL.pop(1))
                        if (pygame.mixer.get_init()):
                            self.audio_se_change.play()

            elif event.type == MOUSEBUTTONUP:
                self.cur_x, self.cur_y = event.pos
        

        
        label2 = self.myfont.render('NEXT', 1, (255,255,0))
        label2 = pygame.transform.rotate(label2, -5)
        
        #### BG
        screen.blit(self.Img_BG, (0,0))

        ###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@# PC端處理(已修改)
        if (self.network == None):
            if self.mode==1 and self.FREEZETIME==False and self.find_lowest_ball2() <= 16:
                if (self.CURRENT_BALL_VEC_X2 != 0 or self.CURRENT_BALL_VEC_Y2 != 0):
                    self.PC_ball_judge()
                    self.draw_ball(screen,self.CURRENT_BALL2[0], self.CURRENT_BALL_X2, self.CURRENT_BALL_Y2)
                    
                elif self.PC_time+self.PC_level < time.time():
                    self.PC_time = time.time()
                    self.PC_think()
                
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                
        #### BALL JUDGE
        if (self.CURRENT_BALL_VEC_X != 0 or self.CURRENT_BALL_VEC_Y != 0 and self.FREEZETIME==False):
            self.ball_judge()
            self.draw_ball(screen,self.CURRENT_BALL[0], self.CURRENT_BALL_X, self.CURRENT_BALL_Y)
            
        #### PLAYER BALL
        for i in range(len(self.CURRENT_BALL)):
            if (i != 0 or (self.CURRENT_BALL_VEC_X == 0 and self.CURRENT_BALL_VEC_Y == 0)):
                self.draw_ball(screen,self.CURRENT_BALL[i], 180 + 80 * i, 680)
                
        #### ASSIST LINE 計算
        START_X = 200
        START_Y = 700+self.BALL_SIZE/2
        
        dd = self.divto(self.cur_x - START_X,self.cur_y - 700)
        VEC_BASIC_X = math.sqrt(((self.cur_x - START_X)**2) / dd)
        if (self.cur_x < 200):
            VEC_BASIC_X *= -1
        VEC_BASIC_Y = math.sqrt(((self.cur_y - 700)**2)/ dd)

        #### 角度修正
        if (VEC_BASIC_Y == 0):
            VEC_BASIC_Y = 0.5
            
        if (abs(VEC_BASIC_X / VEC_BASIC_Y) > 2.0):
            VEC_BASIC_X = 1.0
            if (self.cur_x < 200):
                VEC_BASIC_X = -1.0
            VEC_BASIC_Y = 0.5

        if (len(self.CURRENT_BALL) > 0):
            #### ASSIST LINE 繪製
            for i in range(100):
                DIS = 0
                if (VEC_BASIC_X == 0):
                    DIS = self.BALL_SIZE
                else:
                    if (START_X >= 400 - self.BALL_SIZE/2):
                        DIS = math.sqrt(((400-START_X) * VEC_BASIC_Y / VEC_BASIC_X)**2 + (400-START_X)**2)
                    else:
                        DIS = math.sqrt(((START_X) * VEC_BASIC_Y / VEC_BASIC_X)**2 + (START_X)**2)
                        
                if (DIS >= self.BALL_SIZE/2 or (VEC_BASIC_X * (START_X - self.BALL_SIZE/2) < 0)):
                    if (i%2 == 0):
                        pygame.draw.line(screen, self.BALL_COLOR_FG[self.CURRENT_BALL[0]] , (math.floor(START_X),math.floor(START_Y)), (math.floor(START_X + VEC_BASIC_X * self.BALL_SIZE/2), math.floor(START_Y - VEC_BASIC_Y * self.BALL_SIZE/2)), 5)
                    START_X += VEC_BASIC_X * self.BALL_SIZE/2
                    START_Y -= VEC_BASIC_Y * self.BALL_SIZE/2
                    A = 0
                else:
                    if (i%2 == 0):
                        pygame.draw.line(screen, self.BALL_COLOR_FG[self.CURRENT_BALL[0]] , (math.floor(START_X),math.floor(START_Y)), (math.floor(START_X + VEC_BASIC_X * DIS), math.floor(START_Y - VEC_BASIC_Y * DIS)), 5)
                    START_X += VEC_BASIC_X * DIS
                    START_Y -= VEC_BASIC_Y * DIS
                    DIS = self.BALL_SIZE/2 - DIS
                    VEC_BASIC_X*=-1
                    if (i%2 == 0):
                        pygame.draw.line(screen, self.BALL_COLOR_FG[self.CURRENT_BALL[0]] , (math.floor(START_X),math.floor(START_Y)), (math.floor(START_X + VEC_BASIC_X * DIS), math.floor(START_Y - VEC_BASIC_Y * DIS)), 5) 
                    START_X += VEC_BASIC_X * DIS
                    START_Y -= VEC_BASIC_Y * DIS

                if (self.check_empty(START_X,START_Y) == False):
                    break
 
        #### SIDE
        pygame.draw.line(screen, (200,0,200), (0,680), (403, 680), 5)
        pygame.draw.line(screen, (0,200,200), (403,0), (403, self.WINDOWHEIGHT), 5)
        
        #### BALL
        for j in range(len(self.BALL_DATA)):
            for i in range(len(self.BALL_DATA[j])):
                if (self.BALL_DATA[j][i] != -1):
                    self.draw_ball(screen,self.BALL_DATA[j][i], i*self.BALL_SIZE + (j%2)*self.BALL_SIZE/2, j*self.BALL_SIZE)

        if (Debug_Mode):
            Debug_display()
        #### DAMAGE
        for i in range(12):
            if (self.DAMAGE_LOCAL > i):
                pygame.draw.rect(screen,(255,0,0), (410, 666-i*60, 15, 50) ,0)
                pygame.draw.circle(screen, (200,0,0), (420,672-i*60), 4)
            else:
                pygame.draw.rect(screen,(128,128,128), (410, 666-i*60, 15, 50) ,0)
                pygame.draw.circle(screen, (192,192,192), (420,672-i*60), 4)

            
        #For multiplayer
        if (self.mode == 1):
            WIDE2 = self.WINDOWWIDTH*2+self.MULTIPLAYER_EXWIDE


            #### RIVAL BALL
            for i in range(len(self.CURRENT_BALL2)):
                self.draw_ball(screen,self.CURRENT_BALL2[i], WIDE2 - 220 - 80 * i, 680)
                    
            #### 判定線
            pygame.draw.line(screen, (200,0,200), (self.WINDOWWIDTH+self.MULTIPLAYER_EXWIDE+30,680), (WIDE2, 680), 5)
            pygame.draw.line(screen, (0,200,200), (self.WINDOWWIDTH+self.MULTIPLAYER_EXWIDE+30,0), (self.WINDOWWIDTH+self.MULTIPLAYER_EXWIDE+30, self.WINDOWHEIGHT), 5)

            #### BALL
            for j in range(len(self.BALL_DATA2)):
                for i in range(len(self.BALL_DATA2[j])):
                    if (self.BALL_DATA2[j][i] != -1):
                        self.draw_ball(screen, self.BALL_DATA2[j][i], self.WINDOWWIDTH+self.MULTIPLAYER_EXWIDE+i*self.BALL_SIZE+35 + (j%2)*self.BALL_SIZE/2, j*self.BALL_SIZE)
            #### RIVAL DAMAGE
            for i in range(12):
                if (self.DAMAGE_RIVAL > i):
                    pygame.draw.rect(screen,(255,0,0), (WIDE2-425, 666-i*60, 15, 50) ,0)
                    pygame.draw.circle(screen, (200,0,0), (WIDE2-420,672-i*60), 4)
                else:
                    pygame.draw.rect(screen,(128,128,128), (WIDE2-425, 666-i*60, 15, 50) ,0)
                    pygame.draw.circle(screen, (192,192,192), (WIDE2-420,672-i*60), 4)
                
            #剩餘時間
            if (self.FREEZETIME == False):
                screen.blit(self.myfont2.render("TIME", 1, (255,255,0)) , (WIDE2/2-32, 12))
                if (self.TIMELEFT > 15):
                    time_label = self.myfont4.render(str(self.TIMELEFT), 1, (255,255,0))
                else:
                    time_label = self.myfont4.render(str(self.TIMELEFT), 1, (255,0,0))
                screen.blit(time_label, (WIDE2/2-time_label.get_width()/2, 36))

            #分數
            screen.blit(self.myfont2.render("SC", 1, (0,255,255)) , (WIDE2/2-32, 108))
            self.Score_label = self.myfont2.render(str(self.Score_LOCAL), 1, (0,255,255))
            screen.blit(self.Score_label, (WIDE2/2-32, 132))

            #分數
            screen.blit(self.myfont2.render("SC", 1, (255,0,255)) , (WIDE2/2-32, 156))
            self.Score_label = self.myfont2.render(str(self.Score_RIVAL), 1, (255,0,255))
            screen.blit(self.Score_label, (WIDE2/2-32, 180))

            #KO
            screen.blit(self.myfont2.render("K.O.", 1, (0,255,255)) , (WIDE2/2-32, 204))
            self.Score_label = self.myfont2.render(str(self.KOCOUNT_LOCAL), 1, (0,255,255))
            screen.blit(self.Score_label, (WIDE2/2-32, 228))

            #KO
            screen.blit(self.myfont2.render("K.O.", 1, (255,0,255)) , (WIDE2/2-32, 252))
            self.Score_label = self.myfont2.render(str(self.KOCOUNT_RIVAL), 1, (255,0,255))
            screen.blit(self.Score_label, (WIDE2/2-32, 276))

            #DEAD
            
            if (self.find_lowest_ball() > 16):
                screen.blit(self.Black_BG, (0,0))
                label5 = self.myfont3.render('K O', 1, (255,0,0))
                screen.blit(label5, (self.WINDOWWIDTH/2-label5.get_width()/2,self.WINDOWHEIGHT/2-label5.get_height()/2))

            if (self.find_lowest_ball2() > 16):
                screen.blit(self.Black_BG, (self.WINDOWWIDTH+self.MULTIPLAYER_EXWIDE,0))
                label5 = self.myfont3.render('K O', 1, (255,0,0))
                screen.blit(label5, (self.WINDOWWIDTH+self.MULTIPLAYER_EXWIDE+self.WINDOWWIDTH/2-label5.get_width()/2,self.WINDOWHEIGHT/2-label5.get_height()/2))

            if (self.FREEZETIME):
                screen.blit(self.Black_BG_Full, (0,0))

                if (self.TIMELEFT <= 0):
                    if ((self.KOCOUNT_RIVAL > self.KOCOUNT_LOCAL) or (self.KOCOUNT_RIVAL == self.KOCOUNT_LOCAL and self.Score_RIVAL > self.Score_LOCAL)): 
                        L_img = self.graphics_lose
                        R_img = self.graphics_win
                    else:
                        L_img = self.graphics_win
                        R_img = self.graphics_lose

                    screen.blit(L_img, (self.WINDOWWIDTH/2-L_img.get_width()/2,self.WINDOWHEIGHT/2-L_img.get_height()/2))
                    screen.blit(R_img, (self.WINDOWWIDTH+self.MULTIPLAYER_EXWIDE+self.WINDOWWIDTH/2-R_img.get_width()/2,self.WINDOWHEIGHT/2-R_img.get_height()/2))

        #### LABEL
        screen.blit(label2, (360, 650))

        #TIME
        if (self.gametime + 1.0 < time.time()):
            self.gametime = time.time()
            self.TIMELEFT -=1
            if (self.TIMELEFT > 0 and self.FREEZETIME == False):
                if (self.TIMELEFT == 15):
                    if (pygame.mixer.get_init()):
                        self.audio_se_hurryup.play()
            else:
                if (self.FREEZETIME == False):
                    self.FREEZETIME = True
                    self.CURRENT_BALL_VEC_X = 0
                    self.CURRENT_BALL_VEC_Y = 0
                    
                    #self.audio_se_timeup.play()
                    if (pygame.mixer.get_init()):
                        pygame.mixer.music.stop()
                        if ((self.KOCOUNT_RIVAL > self.KOCOUNT_LOCAL) or (self.KOCOUNT_RIVAL == self.KOCOUNT_LOCAL and self.Score_RIVAL > self.Score_LOCAL)): 
                            self.audio_se_lose.play()
                        else:
                            self.audio_se_win.play()

                    ##讀設定檔
                    from System_GameConfig import System_GameConfig as cfg
                    a = cfg()
                    ##存圖
                    if (not cfg.ScreenShot == 0):
                        now = datetime.datetime.now()#time
                        w_time=now.strftime('screenshot/%Y-%m-%d %H-%M-%S.png') #time-str
                        try:
                            if not os.path.exists('screenshot'):
                                os.makedirs('screenshot')
                            pygame.image.save(screen.copy(), w_time)
                        except Exception as e:
                            print("儲存圖片時發生錯誤：")
                            print(e)
                            
                    ##記錄成績
                    from DB import DB
                    db = DB()
                    db.write(a.CurrentName, self.Score_LOCAL, self.MaxComboCount_LOCAL)

                    if (not self.network == None and self.network.TCP_Connected == True):
                        db.write("RIVAL", self.Score_RIVAL, self.MaxComboCount_RIVAL, "Y")
                if (self.TIMELEFT == -5):
                    #扔回去
                    from Scene_Title import Scene_Title
                    return Scene_Changer(Scene_Title(), screen)

            if (not self.network == None):
                if (self.network.TCP_Connected == True):
                    newdata = "BPB,/BallData,/"
                    for i in self.BALL_DATA:
                        for j in range(len(i)):
                            newdata = newdata + str(i[j])
                            if (not j == len(i) - 1):
                                newdata = newdata + ","

                        newdata = newdata + "=/"

                    newdata = newdata + "\n"
                    str_data = bytes(newdata, "utf-8")
                    self.network.TCP_socket.send(str_data)

            ##RESPAWN

            if (self.find_lowest_ball() > 16):
                for i in range(5,len(self.BALL_DATA)):
                    for j in range(len(self.BALL_DATA[i])):
                        self.BALL_DATA[i][j] = -1
            if self.mode==1:
                if (self.find_lowest_ball2() > 16):
                    for i in range(5,len(self.BALL_DATA2)):
                        for j in range(len(self.BALL_DATA2[i])):
                            self.BALL_DATA2[i][j] = -1
        #### 連線更新
        if (not self.network == None):
            self.BALL_DATA2 = self.network.Buffer_Ball_Data
            self.CURRENT_BALL2 = self.network.Buffer_Current_Ball
            self.DAMAGE_RIVAL = 0
            self.DAMAGE_LOCAL += self.network.Buffer_DAMAGE
            self.Score_RIVAL = self.network.Buffer_Score
            
            self.KOCOUNT_LOCAL = self.network.Buffer_KO
            self.ComboCount_RIVAL = self.network.Buffer_Combo
            self.MaxComboCount_RIVAL = max(self.ComboCount_RIVAL, self.MaxComboCount_RIVAL)
            
            if (self.network.Buffer_DAMAGE > 0):
                ani_combo(self.ComboCount_RIVAL,730,500, 1, -5, 0, 0.25)
                
            self.network.flush()
            
            if (self.network.TCP_Connected == False):
                self.FREEZETIME = True
                self.TIMELEFT = 0
        ani_base.update(screen)
