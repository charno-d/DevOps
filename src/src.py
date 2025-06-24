import pygame
import math
import random
import time
pygame.init()

screen_width,screen_height=1408,704
screen=pygame.display.set_mode((screen_width,screen_height))
block_size=64
images=[]
for x in [2,4,8,16,32,64]:
    image=pygame.transform.scale(pygame.image.load('pic/block%d.jpg'%x),(block_size,block_size))
    images.append(image)
back_image=pygame.transform.scale(pygame.image.load('pic/back.jpg'),(block_size,block_size))

class MoveState:
    FREE=0
    MOVE=1
    STAY=2

class Block:
    def calc_degree(self,ori,tar):
        dx=tar[0]-ori[0]
        dy=tar[1]-ori[1]
        if dx==0 and dy==0:
            return math.atan2(1,0)
        return math.atan2(dy,dx)

    def __init__(self,pos,target_pos):
        self.level=random.randint(0,2)
        self.image=images[self.level]
        self.rect=self.image.get_rect(center=pos)
        self.speed=[0.2,-0.6]
        self.acc=[0,0.0008]

        self.move_state=MoveState.FREE
    
        rad=self.calc_degree(pos,target_pos)
        self.speed[0]+=0.8*math.cos(rad)
        self.speed[1]+=0.8*math.sin(rad)
        self.pos=pos

    def level_up(self):
        if self.level<5:
            self.level+=1
            self.image=images[self.level]
            return True
        return False
    def update(self):
        if self.move_state==MoveState.FREE:
            self.speed[0]+=self.acc[0]*delta_time
            self.speed[1]+=self.acc[1]*delta_time
            self.pos[0]+=self.speed[0]*delta_time
            self.pos[1]+=self.speed[1]*delta_time
            self.rect.center=self.pos
        elif self.move_state==MoveState.MOVE:
            self.pos[0]+=(self.target_pos[0]-self.pos[0])/5
            self.pos[1]+=(self.target_pos[1]-self.pos[1])/5
            if abs(self.target_pos[0]-self.pos[0])<1 and abs(self.target_pos-self.pos[1])<1:
                self.pos=self.target_pos
                self.move_state=MoveState.STAY
            self.rect.center=self.pos
        
    def set_move_state(self,move_state,grid_pos=None):
        self.move_state=move_state
        self.grid_pos=grid_pos
        if grid_pos:
            target_x=grid_pos[1]*block_size+block_size//2+screen_width//2
            target_y=grid_pos[0]*block_si+block_size//2
    def is_horizontal_collision(self,received):
        dx=min(self.rect.right,received.rect.right)-max(self.rect.left,received.rect.left)
        dy=min(self.rect.bottom,received.rect.bottom)-max(self.rect.top,received.rect.top)
        return dx<=dy
    


active_blocks=[]
received_blocks=[]
back_blocks={}

for i in range (screen_height//block_size):
    for j in range(screen_width//block_size):
        rect=pygame.Rect(screen_width//2+j*block_size,i*block_size,block_size,block_size)
        back_blocks[(i,j)]=rect

running=True
delta_time=0
clock=pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            mouse_pos=pygame.mouse.get_pos()
            active_blocks.append(Block([0,screen_height-block_size],mouse_pos))
    screen.fill((0,0,0))
    for(i,j),rect in back_blocks.items():
        screen.blit(back_image,rect)
    to_receive=[]
    for block in active_blocks[:]:
        block.update()
        #boundary check
        if block.rect.right>screen_width:
            block.speed[0]=-abs(block.speed[0])
        if block.rect.left<0:
            block.speed[0]=abs(block.speed[0])
        if block.rect.top<0 :
            block.speed[1]=abs(block.speed[1])
        if block.rect.bottom>screen_height:
            block.speed=[0,0]
            block.acc=[0,0]
            block.active=False
            to_receive.append(block)    


    for block in to_receive:
        if block in active_blocks:
            active_blocks.remove(block)
            received_blocks.append(block)
    



    for block in active_blocks:
        screen.blit(block.image,block.rect)
    for block in received_blocks:
        screen.blit(block.image,block.rect)
    

    delta_time=clock.tick(1000)
    pygame.display.flip()

pygame.quit()