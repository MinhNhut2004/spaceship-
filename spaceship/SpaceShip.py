import pygame , sys 
import random
from pygame.locals import *
from pygame import mixer
pygame.init()
mixer.init()

#CONS
exit = True
fps=60
frame_count=0
SCREENH = 900
SCREENW = 800
SPEED=8
gameover=0
SPEEDANEMY=0.5
COOLDOWN_BULLET = 500 
COOLDOWN_BULLET_ENEMY=1000
LAST_SHOT_ENEMY = pygame.time.get_ticks()
#COLOR
RED = (255,0,0)
#IMAGE
BG = pygame.transform.scale(pygame.image.load(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\IMAGE\bg.jpg'),(900,800))
Ship_img = pygame.transform.scale(pygame.image.load(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\IMAGE\ship.jpg'),(100,100))
icon=pygame.image.load(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\IMAGE\bullet.jpg')
bullet_img =pygame.transform.scale(pygame.image.load(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\IMAGE\bullet.jpg'),(50,50))
bulletenemy_img =pygame.transform.scale(pygame.image.load(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\IMAGE\bulletenemy.jpg'),(50,50))
boom_img =pygame.image.load(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\IMAGE\boom.jpg')



WINDOWN = pygame.display.set_mode((SCREENH, SCREENW))
pygame.display.set_caption("SpaceShip")
pygame.display.set_icon(icon)

allSprite=pygame.sprite.Group()
ship_group=pygame.sprite.Group()
enemy_group=pygame.sprite.Group() 
enemybullet_group=pygame.sprite.Group()
explosion_group=pygame.sprite.Group()
bullet_group=pygame.sprite.Group()
#SOUND
bullet_sound=mixer.Sound(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\SOUND\bullet_sound.mp3')
fx=mixer.Sound(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\SOUND\fx.mp3')
def draw ():
    WINDOWN.blit(BG,(0,0))


#   CLASS
class Spaceship (pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image= Ship_img
        self.rect = self.image.get_rect()
        self.rect.center=[x,y]
        self.time_last_shot = pygame.time.get_ticks()
        self.health_start = 3
        self.health_remaining = 3
    def update(self):
        gameover=0
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > -70 :
            self.rect.x -=SPEED
        elif keys[pygame.K_d] and self.rect.x < SCREENW +70:
            self.rect.x +=SPEED
        elif keys[pygame.K_w] and self.rect.y > -100:
            self.rect.y -=SPEED
        elif keys[pygame.K_s] and self.rect.y < (SCREENH - self.rect.height - 100):
            self.rect.y +=SPEED

        pygame.draw.rect(WINDOWN, RED, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(WINDOWN, RED, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        if self.health_remaining <=0:
                fx.set_volume(0.05)
                fx.play()
                explosion = Explosion(self.rect.centerx, self.rect.centery)
                explosion_group.add(explosion)
                allSprite.add(explosion_group)
                self.kill()
                gameover=-1

        if keys[pygame.K_SPACE] :
            bullet_sound.set_volume(0.05)
            bullet_sound.play()
            self.shootbullet()
        return gameover
        
    def shootbullet (self):
        current_time = pygame.time.get_ticks()
        if (current_time-self.time_last_shot) > COOLDOWN_BULLET :
            bullet=Bullet(self.rect.centerx,self.rect.top)
            bullet_group.add(bullet)
            allSprite.add(bullet_group)
            self.time_last_shot=current_time
           
    

class Bullet (pygame.sprite.Sprite):
    def __init__(self, x,y) :
        super().__init__()
        self.image=bullet_img
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.speed_y = -5
    def update(self):
        self.rect.y +=self.speed_y
        if self.rect.bottom < 0 :
            self.kill()
        if pygame.sprite.spritecollide(self,enemy_group, False, pygame.sprite.collide_mask):
            self.kill()
            fx.set_volume(0.05)
            fx.play()
			#reduce spaceship health
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(explosion)
            allSprite.add(explosion_group)
            exit=False
           
class Enemy (pygame.sprite.Sprite):
    def __init__(self, x , y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\IMAGE\enemy'+ str(random.randint(1,4))+ '.png'),(130,130))
        self.rect=self.image.get_rect()
        self.rect.center = [x,y]
        self.movex =1 
        self.movey =1 
        self.countx =0
        self.county =0
    def update(self):
        self.rect.centerx += self.movex
        self.rect.centery += self.movey
        self.countx+=1
        self.county+=1
        if self.countx > 20 :
            self.movex*=-1
            self.countx *=self.movex
        if self.county >= (SCREENH / 3 +100):
            self.movey *= -1
            self.county*= self.movey
        if pygame.sprite.spritecollide(self,bullet_group, False, pygame.sprite.collide_mask):
            self.kill()
            fx.set_volume(0.05)
            fx.play()
			#reduce spaceship health
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(explosion)
            allSprite.add(explosion_group)
        if check_collision_between_groups(enemy_group,ship_group) :
            self.kill()
            fx.set_volume(0.05)
            fx.play()
			#reduce spaceship health
            ship.health_remaining=ship.health_remaining -1
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(explosion)
            allSprite.add(explosion_group)
        if self.rect.bottom < 0 or self.rect.top > SCREENH or self.rect.right < 0 or self.rect.left > SCREENW:
            self.kill()

def check_collision_between_groups(group1, group2):


    for sprite1 in group1:
        for sprite2 in group2:
            
            if sprite1.rect.colliderect(sprite2.rect):
               
                if sprite1.rect.bottom > sprite2.rect.top and sprite1.rect.top < sprite2.rect.top:
                    return True
               
                elif sprite1.rect.top < sprite2.rect.bottom and sprite1.rect.bottom > sprite2.rect.bottom:
                    return True
             
                elif sprite1.rect.right > sprite2.rect.left and sprite1.rect.left < sprite2.rect.left:
                    return True
             
                elif sprite1.rect.left < sprite2.rect.right and sprite1.rect.right > sprite2.rect.right:
                    return True
                return True
    return False

class Bulletofenemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=bulletenemy_img
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.speed_y = 7
    def update(self):
        self.rect.centery += self.speed_y
        if self.rect.bottom > SCREENH :
            self.kill()
       
        self.mask = pygame.mask.from_surface(self.image)

        if pygame.sprite.spritecollide(self, ship_group, False, pygame.sprite.collide_mask):
            self.kill()
            fx.set_volume(0.05)
            fx.play()
            ship.health_remaining=ship.health_remaining -1   
			#reduce spaceship health
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(explosion)
            allSprite.add(explosion_group)
            


class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\IMAGE\boom.jpg')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		
        

	def update(self):
            self.kill()




def createnemy():
    
    for enemy in range(5,8): 
            number=random.randint(1,9) 
            enemy = Enemy(100 + number * 100, 0)
            enemy_group.add(enemy)
            allSprite.add(enemy_group)
    


#
createnemy()
ship=Spaceship(500,500)
ship_group.add(ship)
allSprite.add(ship_group)


olock=pygame.time.Clock()
mixer.music.load(r'C:\Users\tuhin\Desktop\WorkSpace\python\pygame\game1\SOUND\music.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)
while exit:
    
    olock.tick(fps)
    timenow=pygame.time.get_ticks()
    
    if (timenow - LAST_SHOT_ENEMY) > COOLDOWN_BULLET_ENEMY:
        attack = random.choice(enemy_group.sprites())
        bulletofenemy = Bulletofenemy(attack.rect.centerx, attack.rect.bottom)
        enemybullet_group.add(bulletofenemy)
        allSprite.add(enemybullet_group)
        LAST_SHOT_ENEMY = timenow

   
    if gameover==0:
        frame_count+=1
        if (frame_count % 200) == 0: 
            createnemy()
        allSprite.update()
        draw()
        allSprite.draw(WINDOWN)    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
pygame.quit()