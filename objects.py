import pygame
import os
from random import randint

framesPerAnimation = 4

class player(object):
    def __init__(self, hp, mp, exp, level, dmg, player_cord):
        self.hp = hp
        self.mp = mp
        self.exp = exp
        self.level = level
        self.dmg = dmg
        self.moveCount = 360
        self.player_cord = player_cord
        lvl = "level" + str(self.level)
        self.movement =  [pygame.image.load('eqp\\'+ lvl +'\swingO1_0.png'),pygame.image.load('eqp\\'+ lvl +'\swingO1_1.png'),pygame.image.load('eqp\\'+ lvl +'\swingO1_2.png'),pygame.image.load('eqp\\'+ lvl +'\swingO1_3.png'),
                pygame.image.load('eqp\\'+ lvl +'\swingO2_0.png'),pygame.image.load('eqp\\'+ lvl +'\swingO2_1.png'),pygame.image.load('eqp\\'+ lvl +'\swingO2_2.png'),pygame.image.load('eqp\\'+ lvl +'\swingO2_3.png'),
                pygame.image.load('eqp\\'+ lvl +'\swingO3_0.png'),pygame.image.load('eqp\\'+ lvl +'\swingO3_1.png'),pygame.image.load('eqp\\'+ lvl +'\swingO3_2.png'),pygame.image.load('eqp\\'+ lvl +'\swingO3_3.png')]

    def draw(self, win):
        if self.moveCount+1 > 12 :
            self.moveCount = 0
        else:
            win.blit(self.movement[self.moveCount], self.player_cord )


class mob(object):
    def __init__(self, hp, name, mob_x , mob_y ):
        #input attributes
        self.spawn_hp = hp
        self.hp= hp
        self.exp = hp/10 #exp form bedenken
        self.mesos = hp/1000 #mesos form bedenken
        self.name = name
        self.mob_x = mob_x
        self.mob_y = mob_y
        self.mob_cord = (mob_x,mob_y)

        #load all movement images

        #number of frames
        self.Number_Frames_stand = len(os.listdir('mob\\' + self.name + '\\stand'))
        self.Number_Frames_die = len(os.listdir('mob\\' + self.name + '\\die'))
        self.Number_Frames_hit =  len(os.listdir('mob\\' + self.name + '\\hit'))

        #define image array
        self.image_die = []
        self.image_hit = []
        self.image_stand = []

        #fill all  image arrays
        for i in range(0,self.Number_Frames_stand):
            self.image_stand.append(pygame.image.load('mob\\' + self.name + '\\stand\stand_' + str(i) + ".png"))
        for i in range(0,self.Number_Frames_die):
            self.image_die.append(pygame.image.load('mob\\' + self.name + '\\die\die1_' + str(i) + ".png"))
        for i in range(0, self.Number_Frames_hit):
            self.image_hit.append(pygame.image.load('mob\\' + self.name + '\\hit\hit1_' + str(i) + ".png"))

        #excess attributes
        self.deadFrame = 0
        self.standFrame = 0
        self.hitFrame = 0
        self.width = self.image_stand[0].get_width()
        self.height = self.image_stand[0].get_height()
        self.hitbox = [self.mob_x-self.width,self.mob_y-self.height,self.width, self.height]

    def draw(self, win):
        #draw hit box
        pygame.draw.rect(win, (255,0,0) ,self.hitbox,1)

        #draw correct frame
        if self.hitFrame>0 and self.hp>0:
            win.blit(self.image_hit[0], (self.mob_x-self.image_hit[0].get_width(), self.mob_y-self.image_hit[0].get_height()))
            self.hitFrame -=1

        elif self.hp<=0:
            win.blit(self.image_die[self.deadFrame//framesPerAnimation], (self.mob_x-self.image_die[0].get_width(), self.mob_y-self.image_die[0].get_height()))
            if self.deadFrame + 1 < (self.Number_Frames_die) *framesPerAnimation :
                self.deadFrame += 1
                print("dying")
            else:
                self.deadFrame = -1
                print("dead")
        else:
            if self.standFrame+1 > self.Number_Frames_stand * framesPerAnimation:
                self.standFrame =0
            win.blit(self.image_stand[self.standFrame//framesPerAnimation], (self.mob_x-self.image_stand[0].get_width(), self.mob_y-self.image_stand[0].get_height()))
            self.standFrame += 1

    def hit(self):
        self.hitFrame = framesPerAnimation
        self.hp -=1
        print("hit")

    def regen(self):
        self.hp = self.spawn_hp
        self.deadFrame = 0
        self.standFrame = 0
        self.hitFrame = 0

class star(object):
    def __init__(self, lvl, star_x, star_y):
        self.lvl = lvl
        self.multi = 1 + (0.5*lvl*lvl)
        self.rotation = 0
        self.star = pygame.image.load('star\star' + str(0)+'.png')
        self.x = star_x
        self.y = star_y

    def draw(self, win):
        increments = randint(1,40)
        if self.y%2 == 0:
            self.y += 3
        else:
            self.y -= 3  
        
        if self.rotation - 360/increments < 0:
            self.rotation = 360
        rotated_star = pygame.transform.rotate(self.star, self.rotation)
        self.rotation -= int(360/increments)
        win.blit(rotated_star, (self.x, self.y))
