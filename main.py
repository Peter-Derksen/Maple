import pygame
import os
import objects
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
star_x = 70 #start coord
star_y = 420
star_vel = 10 #frames to right per update
star_cap = 100 # max number of stars
star_vel_increment = 25
star_cap_increment = 2 
stars_per_x_frames = 1 # stars keep distance lower the closer

#upgrades
index_mob = 0

run = True

#define objects

#lists
stars = []
mobs_active =[]
mobs_list = [objects.mob(10, "darkCornian",mob_x,mob_y), objects.mob(100, "Arkarium",mob_x,mob_y)]
char = objects.player(1,1,1,2,1, player_cord) 

#append objects
stars.append(objects.star(1,star_x, star_y)) 
mobs_active.append(mobs_list[0])


#main draw function
def mainDraw():
    win.blit(bg[0],(0,0))
    char.draw(win)
    for mob in mobs_active:
        if mob.hp <=0 and mob.deadFrame <0:
            mobs_active.pop(mobs_active.index(mob))
            mobs_active.append(mobs_list[index_mob])
            mobs_active[0].regen()
            
        for star in stars:
            if star.x +star_vel > mob.mob_x - mob.width: # darkcornian aanpassen y variabele niet nodig
                mob.hit()
                stars.pop(stars.index(star))
                mob.hitFrame = objects.framesPerAnimation

            if star.x + star_vel < x_pixels:
                star.draw(win)
                star.x = star.x + star_vel
            else:
                stars.pop(stars.index(star))
        mob.draw(win)

    pygame.display.update()

star_frame_count = 0
#main loop
while run:
    keys = pygame.key.get_pressed()
    clock.tick(30)

    for event in pygame.event.get(): #gets events (mouse movement key etc)
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_SPACE]:
        if len(stars) < star_cap and star_frame_count <=0:
            stars.append(objects.star(1,star_x, star_y))
            char.moveCount = char.moveCount+1
            star_frame_count = stars_per_x_frames
        else:
            print(star_frame_count)
            star_frame_count -=1                   
    mainDraw()


#testblock
