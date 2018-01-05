import pygame
class ani_base:
    Ani_obj = []
    width = 640
    height = 480
    pygame.init()
    font = pygame.font.SysFont("Arial Black", 18)

    def init(w = 640, h = 480):
        ani_base.width, ani_base.height = w, h
    
    def __init__(self, image = None, x = 0, y = 0, vec_x = 0, vec_y = 0, speed_x = 0, speed_y = 0, time = -1):
        #print(self)
        #print(image)
        self.add_anim(image, x, y, vec_x, vec_y, speed_x, speed_y, time)

    def add_textanim(self, text, color = (255,255,255), x = 0, y = 0, vec_x = 0, vec_y = 0, speed_x = 0, speed_y = 0, time = -1):
        label = ani_base.font.render(str(text), 1, color)
        self.add_anim(label, x, y, vec_x, vec_y, speed_x, speed_y, time)
        
    def add_anim(self, image, x, y, vec_x = 0, vec_y = 0, speed_x = 0, speed_y = 0, time = -1):
        self.image = image
        self.x = x
        self.y = y
        self.vec_x = vec_x
        self.vec_y = vec_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.time = time
        if (image != None):
            self.Ani_obj.append(self)
            
    def update(screen):
        for obj in ani_base.Ani_obj:
            #speed
            if (obj.speed_x != 0):
                obj.vec_x += obj.speed_x
                
            if (obj.speed_y != 0):
                obj.vec_y += obj.speed_y

            #move
            if (obj.vec_x != 0):
                obj.x += obj.vec_x
                
            if (obj.vec_y != 0):
                obj.y += obj.vec_y

            #draw
            screen.blit(obj.image, (obj.x, obj.y))
			
	    #kill
            if (obj.time != -1):
                if (obj.time <= 0):
                    ani_base.Ani_obj.remove(obj) 
                else:
                    obj.time -= 1
            else:
                if (obj.y > ani_base.height):
                    ani_base.Ani_obj.remove(obj)
