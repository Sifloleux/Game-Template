import time
import pygame
from pygame.locals import *
import random
import os.path
import math

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 710
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60
SHOOTING_SPEED = 6
SPEED = [0, 0]
BLOCK_MOVEMENT = 30

starting_point = [SCREEN_WIDTH/2,SCREEN_HEIGHT-60]
draw_line = 0
x = [SCREEN_WIDTH/2,SCREEN_HEIGHT-60]
y=[float('nan'),float('nan')]
mouse_draging = False
shoot = 0
num_of_balls = 1

game_map = [[0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],]


def loadImage(name, useColorKey=False):
    fullname = os.path.join("data",name)
    image = pygame.image.load(fullname)  
    image = image.convert() 
    if useColorKey is True:
        colorkey = image.get_at((0,0)) 
        image.set_colorkey(colorkey,RLEACCEL) 
    return image

def get_speed(starting_point,pointer_point):
    hypotenuse = math.sqrt((abs(pointer_point[1]-starting_point[1]))**2 + \
                           (abs(pointer_point[0]-starting_point[0]))**2)
        
    if starting_point[0] > pointer_point[0]:
        speed = [(pointer_point[0]-starting_point[0])/hypotenuse \
                 ,-(starting_point[1]-pointer_point[1])/hypotenuse]
            
    elif starting_point[0] < pointer_point[0]:
         speed = [(pointer_point[0]-starting_point[0])/hypotenuse \
                 ,-(starting_point[1]-pointer_point[1])/hypotenuse]     
    else:
        speed=[0,1]
    return speed


def add_ball(mouse_position, SHOOTING_SPEED,starting_point):
    speed = get_speed(starting_point,mouse_position)
    ball1 = Ball(RED,20,20,[SHOOTING_SPEED*speed[0],SHOOTING_SPEED*speed[1]])
    ball1.rect.x = starting_point[0] - 10
    ball1.rect.y = starting_point[1] - 10
    all_balls_list.add(ball1)
    all_balls_list.draw(screen)
    pygame.display.flip()




#def add_block_line()


    
class Ball(pygame.sprite.Sprite):

    
    def __init__(self, color, width, height,velocity):
        super().__init__()
        self.velocity = velocity
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])        
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.kill()

class Block(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height,hp):
        super().__init__()
        self.hp = hp
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, SCREEN_WIDTH/10, SCREEN_WIDTH/10])        
        self.rect = self.image.get_rect()
        #self.rect.bottom.
    
    def update(self):
        self.rect.y += BLOCK_MOVEMENT
        if self.hp <=0:
             self.kill()
             
             
class Line(pygame.sprite.Sprite):
     def __init__(self, color, width, height,hp):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height],3)        
        self.rect = self.image.get_rect()
        #self.rect.bottom.
    
     def update(self):
         self.rect.y += BLOCK_MOVEMENT
         if self.hp <=0:
             self.kill()
             
             
             
             
#----------------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
mouse_draging = False
all_balls_list = pygame.sprite.Group()
all_blocks_list = pygame.sprite.Group()
all_vertical_list = pygame.sprite.Group()
all_horizontal_list = pygame.sprite.Group()
 

carryOn = True

block = Block(WHITE,50,50,1)
block.rect.x = 300
block.rect.y = 100
all_blocks_list.add(block)

clock = pygame.time.Clock()
 

while carryOn:
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
              carryOn = False 
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: 
                     carryOn=False

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and shoot ==1:
                mouse_x, mouse_y = event.pos 
                mouse_draging = False
                y[0] = y[0]
                y[1] = y[1]
                draw_line = 0
                for i in range(num_of_balls):
                    print(mouse_x, mouse_y)
                    add_ball([mouse_x, mouse_y],SHOOTING_SPEED,starting_point)
                shoot= 0 
                
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                mouse_draging = False
                y[0] = y[0]
                y[1] = y[1]
                draw_line = 0 
                shoot = 0
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_draging = True
            mouse_x, mouse_y = event.pos             
            draw_line = 1
            shoot = 1
            all_balls_list.draw(screen)  
            pygame.display.flip()
                                   
        elif event.type == pygame.MOUSEMOTION:
            if mouse_draging:
                mouse_x, mouse_y = event.pos
                y[0] = mouse_x
                y[1] = mouse_y
                draw_line = 1
 

    all_balls_list.update()
 

    for obj in all_balls_list:
        if obj.rect.x>=SCREEN_WIDTH:
            obj.velocity[0] = -obj.velocity[0]
        if obj.rect.x<=0:
            obj.velocity[0] = -obj.velocity[0]
        if obj.rect.y>SCREEN_HEIGHT:
            obj.velocity[1] = -obj.velocity[1]
        if obj.rect.y<0:
            obj.velocity[1] = -obj.velocity[1] 

    
    for hit in pygame.sprite.groupcollide(all_balls_list,all_blocks_list,0,0):
        hit.velocity[0] = - hit.velocity[0]
        hit.velocity[1] = - hit.velocity[1]
        
    for hit in pygame.sprite.groupcollide(all_blocks_list,all_balls_list,0,0):
        hit.hp = hit.hp -1
        if hit.hp <=0:
            hit.kill()
        print(hit.hp)
    
    screen.fill(BLACK)
    

    all_balls_list.draw(screen) 
    all_blocks_list.draw(screen) 
    pygame.draw.circle(screen, RED, [x[0],x[1]],5)
    #if not all_balls_list:

    if draw_line == 1:
        pygame.draw.line(screen, (200,200,200), starting_point,[mouse_x, mouse_y])
    pygame.draw.line(screen,WHITE,[0,655],[SCREEN_WIDTH,655],2)
    pygame.display.flip()

    clock.tick(60)
 

pygame.quit()