import pygame
import os
from random import randint
#links: https://maples.im/#
#setup / size / title
pygame.init()

x_pixels = 1000
y_pixels = 500
win = pygame.display.set_mode((x_pixels, y_pixels))

pygame.display.set_caption("Maple Shooter by me") #window title
clock = pygame.time.Clock()
throwspeed = 1
bg = [pygame.image.load('bg\magatia.png')]

#player var
player_cord_x= 50
player_cord_y= 395
player_cord= (player_cord_x,player_cord_y)

#mob var
mob_x = 950
mob_y = 460
mob_cord = (mob_x, mob_y)
global mob_index
mob_index=0

#star var
start_star_x = 70
start_star_y = 420
star_vel = 50
star_cap = 10
star_vel_increment = 25
star_cap_increment = 2

#upgrades
index_mob = 0



class player(object):
    lvl = "level" + str(1)
    movement = [pygame.image.load('level1\swingO1_0.png'),pygame.image.load('level1\swingO1_1.png'),pygame.image.load('level1\swingO1_2.png'),pygame.image.load('level1\swingO1_3.png'),
                pygame.image.load('level1\swingO2_0.png'),pygame.image.load('level1\swingO2_1.png'),pygame.image.load('level1\swingO2_2.png'),pygame.image.load('level1\swingO2_3.png'),
                pygame.image.load('level1\swingO3_0.png'),pygame.image.load('level1\swingO3_1.png'),pygame.image.load('level1\swingO3_2.png'),pygame.image.load('level1\swingO3_3.png')]

    def __init__(self, hp, mp, exp, level, dmg):
        self.hp = hp
        self.mp = mp
        self.exp = exp
        self.level = level
        self.dmg = dmg
        self.moveCount = 360

    def draw(self, win):
        if self.moveCount+1 > 12 :
            self.moveCount = 0
        else:
            win.blit(self.movement[self.moveCount], player_cord )


class star(object):
    def __init__(self, lvl):
        self.lvl = lvl
        self.multi = 1 + (0.5*lvl*lvl)
        self.rotation = 0
        self.star = pygame.image.load('star1\\' + 'Subi_0.png')
        self.x = start_star_x


    def draw(self, win):
        increments = randint(1,40)
        if self.rotation - 360/increments < 0:
            self.rotation = 360
        rotated_star = pygame.transform.rotate(self.star, self.rotation)
        self.rotation -= int(360/increments)
        win.blit(rotated_star, (self.x, start_star_y))

def increment_mob():
    global index_mob
    index_mob +=1


class mob(object):
    def __init__(self, hp, name):
        #input attributes
        self.hp= hp
        self.exp = hp/10 #exp form bedenken
        self.mesos = hp/1000 #mesos form bedenken
        self.name = name

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
        self.hitbox = [mob_x-self.width,mob_y-self.height,self.width, self.height]

    def draw(self, win):
        #draw hit box
        pygame.draw.rect(win, (255,0,0) ,self.hitbox,1)

        #draw correct frame
        if self.hitFrame>0 and self.hp>0:
            win.blit(self.image_hit[0], (mob_x-self.image_hit[0].get_width(), mob_y-self.image_hit[0].get_height()))
            self.hitFrame -=1

        elif self.hp<=0:
            win.blit(self.image_die[self.deadFrame//3], (mob_x-self.image_die[0].get_width(), mob_y-self.image_die[0].get_height()))
            if self.deadFrame +1 < (self.Number_Frames_die) *3 :
                self.deadFrame += 1
            else:
                self.deadFrame = -1

        else:
            if self.standFrame+1 > self.Number_Frames_stand * 3:
                self.standFrame =0
            win.blit(self.image_stand[self.standFrame//3], (mob_x-self.image_stand[0].get_width(), mob_y-self.image_stand[0].get_height()))
            self.standFrame += 1

    def hit(self):
        self.hitFrame = 3
        self.hp -=1
        print("hit")



run = True

#define objects
stars = []
stars.append(star(1))
char = player(1,1,1,1,1)

mobs_list =[mob(10, "darkCornian"), mob(100, "Arkarium")]
mobs_active =[]
mobs_active.append(mobs_list[0])


#main draw function
def mainDraw():
    win.blit(bg[0],(0,0))
    char.draw(win)
    for mob in mobs_active:
        if mob.hp <=0 and mob.deadFrame <0:
            mobs_active.pop(mobs_active.index(mob))
            mobs_active.append(mobs_list[index_mob])
            increment_mob()
            
        for star in stars:
            if star.x +star_vel > mob_x- mob.hitbox[1]: # darkcornian aanpassen y variabele niet nodig
                mob.hit()
                stars.pop(stars.index(star))
                mob.hitFrame = 3

            if star.x + star_vel < x_pixels:
                star.draw(win)
                star.x = star.x + star_vel
            else:
                stars.pop(stars.index(star))
        mob.draw(win)

    pygame.display.update()


#main loop
while run:
    keys = pygame.key.get_pressed()
    clock.tick(throwspeed*12)

    for event in pygame.event.get(): #gets events (mouse movement key etc)
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_SPACE]:
        if len(stars) < star_cap:
            stars.append(star(1))
            char.moveCount = char.moveCount+1
    mainDraw()


#testblock
