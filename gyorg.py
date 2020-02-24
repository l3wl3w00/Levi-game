#########################################################################################################################################################################
# Program name: game
# Creation date: 2020. 02. 17.
# Author: Györgydeák Levente
#########################################################################################################################################################################

import pygame
import random
import math

#########################################################################################################################################################################
# global parameters
#########################################################################################################################################################################
pygame.init()
win_width = 1280
win_height = 720
win = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("First Game")
walkRight = pygame.image.load('rajz_jobb.png')
walkLeft = pygame.image.load('rajz_bal.png')
walkUp = pygame.image.load('rajz_fel.png')
walkDown = pygame.image.load('rajz_le.png')
balfel = pygame.image.load("bal_fel.png")
jobbfel = pygame.image.load("jobb_fel.png")
jobble = pygame.image.load("jobb_le.png")
balle = pygame.image.load("bal_le.png")
hatter = pygame.image.load('hatter2.png')
green = [walkLeft,walkRight,walkUp,walkDown,jobbfel,jobble,balfel,balle]
red = [pygame.image.load('badguy_left.png'),pygame.image.load('badguy_right.png'),\
    pygame.image.load('badguy_up.png'),pygame.image.load('badguy_down.png'),\
    pygame.image.load('badguy_upright.png'),pygame.image.load('badguy_downright.png'),\
    pygame.image.load('badguy_upleft.png'),pygame.image.load('badguy_downleft.png')]
blue = [pygame.image.load('blue_left.png'),pygame.image.load('blue_right.png'),\
    pygame.image.load('blue_up.png'),pygame.image.load('blue_down.png'),\
    pygame.image.load('blue_upright.png'),pygame.image.load('blue_downright.png'),\
    pygame.image.load('blue_upleft.png'),pygame.image.load('blue_downleft.png')]
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 30, True)
stunfont = pygame.font.SysFont('arial', 12)
heal = pygame.image.load('heal.png')
#########################################################################################################################################################################
#class player
#########################################################################################################################################################################
class player():
    """self, x, y, r, maxhp, Type,vel = 2 """
    def __init__(self, x, y, r, maxhp, Type,vel = 2 ):
        self.x = x
        self.y = y
        self.r = r
        self.vel = vel
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.lastMove = "up"
        self.maxhp = maxhp
        self.hp = maxhp
        self.Type = Type
        self.collisionDirection = ""
        self.hitbox = (self.x+self.r + 4, self.y + self.r+5)
        self.hitboxr = self.r
        self.isStunned = False

    def drawHitbox(self):
        if self.Type == red:
            self.hitbox = (self.x+self.r , self.y + self.r)
            self.hitboxr = self.r
        pygame.draw.circle(win,(255,0,0),(self.hitbox[0], self.hitbox[1]), self.hitboxr, 2)

    def draw(self,win):
        ########## balra mozog ###########################################
        if self.left and not self.up and not self.down:
            self.up = False
            self.down = False
            win.blit(self.Type[0],(self.x,self.y))
            self.lastMove = "left"

        ########## jobbra mozog ###########################################
        elif self.right and not self.up and not self.down:
            self.up = False
            self.down = False
            win.blit(self.Type[1],(self.x,self.y))
            self.lastMove = "right"

        ########## fel mozog ###########################################
        elif self.up and not self.left and not self.right:
            self.left = False
            self.right = False
            win.blit(self.Type[2],(self.x,self.y))
            self.lastMove = "up"

        ########## le mozog ###########################################
        elif self.down and not self.left and not self.right:
            self.left = False
            self.right = False
            win.blit(self.Type[3],(self.x,self.y))
            self.lastMove = "down"

        ########## jobb fel mozog ###########################################
        elif self.up and self.right:
            win.blit(self.Type[4],(self.x,self.y))
            self.lastMove = "upright"
            if not keyPressed(pygame.K_UP):
                self.up = False
            if not keyPressed(pygame.K_RIGHT):
                self.right = False

        ########## jobb le mozog ###########################################
        elif self.down and self.right:
            self.lastMove = "downright"
            win.blit(self.Type[5],(self.x,self.y))
            if not keyPressed(pygame.K_DOWN):
                self.down = False
            if not keyPressed(pygame.K_RIGHT):
                self.right = False
        
        ########## bal fel mozog ###########################################
        elif self.up and self.left:
            self.lastMove = "upleft"
            win.blit(self.Type[6],(self.x,self.y))
            if not keyPressed(pygame.K_UP):
                self.up = False
            if not keyPressed(pygame.K_LEFT):
                self.left = False

        ########## bal le mozog ###########################################
        elif self.down and self.left:
            self.lastMove = "downleft"
            win.blit(self.Type[7],(self.x,self.y))
            if not keyPressed(pygame.K_LEFT):
                self.left = False
            if not keyPressed(pygame.K_DOWN):
                self.down = False
        ########## áll ###########################################
        else:
            if self.lastMove == "left":
                win.blit(self.Type[0],(self.x,self.y))
            elif self.lastMove == "right":
                win.blit(self.Type[1],(self.x,self.y))
            elif self.lastMove == "up":
                win.blit(self.Type[2],(self.x,self.y))
            elif self.lastMove == "down":
                win.blit(self.Type[3],(self.x,self.y))
            elif self.lastMove == "downleft":
                win.blit(self.Type[7],(self.x,self.y))
            elif self.lastMove == "downright":
                win.blit(self.Type[5],(self.x,self.y))
            elif self.lastMove == "upright":
                win.blit(self.Type[4],(self.x,self.y))
            elif self.lastMove == "upleft":
                win.blit(self.Type[6],(self.x,self.y))
    
    def drawHpBar(self):
        hppercent = self.hp/self.maxhp
        if self.Type != red:
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0] - self.hitboxr, self.hitbox[1] - (self.hitboxr+30),100,20))
            pygame.draw.rect(win,(0,255,0),(self.hitbox[0] - self.hitboxr, self.hitbox[1] - (self.hitboxr+30),round(hppercent*100),20))
            pygame.draw.rect(win,(0,0,0),(self.hitbox[0] - self.hitboxr, self.hitbox[1] - (self.hitboxr+30),100,20),2)
        else:
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0]+7 - self.hitboxr, self.hitbox[1] - (self.hitboxr+30),50,10))
            pygame.draw.rect(win,(0,255,0),(self.hitbox[0]+7 - self.hitboxr, self.hitbox[1] - (self.hitboxr+30),round(hppercent*50),10))
            pygame.draw.rect(win,(0,0,0),(self.hitbox[0]+7 - self.hitboxr, self.hitbox[1] - (self.hitboxr+30),50,10),1)

    def writeStuntext(self, stuntext):
        if self.Type != red:
            win.blit(stuntext,(self.hitbox[0] - self.hitboxr,self.hitbox[1] - (self.hitboxr+30) - 20))
        else:
            win.blit(stuntext,(self.hitbox[0]+7 - self.hitboxr,self.hitbox[1] - (self.hitboxr+30) - 20))

    def moveUp(self):
        if self.y  > 0:
            self.y -= self.vel
            self.up = True
            self.down = False
        self.hitbox = (self.x+self.r + 3, self.y + self.r+3)
            
    def moveDown(self):
        if self.y  < win_height - 2*self.r:   
            self.y += self.vel
            self.down = True
            self.up = False
        self.hitbox = (self.x+self.r + 3, self.y + self.r+3)
            
    def moveLeft(self):
        if self.x  > 0:
            self.x -= self.vel
            self.left = True
            self.right = False
        self.hitbox = (self.x+self.r + 3, self.y + self.r+3)

    def moveRight(self):
        if self.x  < win_width - 2*self.r:
            self.x += self.vel
            self.left = False
            self.right = True
        self.hitbox = (self.x+self.r + 3, self.y + self.r+3)
    
    def shoot(self,listToAppendTo, radius,dmg, color = (255,0,0),stunduration = 20, velp = 15,stun = False):
        """listToAppendTo, radius, dmg"""
        if len(listToAppendTo) < 100:
            listToAppendTo.append(projectile(round(self.x + self.r),round(self.y + self.r),radius,color,self.lastMove,dmg,self,stunDuration = stunduration,vel = velp, isStun = stun))
    
    def die(self, listToRemoveFrom):
        listToRemoveFrom.pop(listToRemoveFrom.index(self))
        del self

    def collideWith(self, target):
        distance = math.hypot(self.hitbox[0] - target.hitbox[0],self.hitbox[1] - target.hitbox[1])

        if  distance <= self.hitboxr + target.hitboxr:#(self.x > target.x + target.r*2 or self.x + self.r *2 < target.x) or (self.y > target.y + target.r*2  or self.y + self.r *2 < target.y):
            print("collision")
            return True
        else:
            return False
            
    def moveTowardsTarget(self,target):
        if not self.collideWith(target):
            if target.x > self.x and self.x + self.vel <= target.x:
                self.moveRight()
            if target.x < self.x and self.x + self.vel >= target.x:
                self.moveLeft()
            if target.y > self.y and self.y + self.vel <= target.y:
                self.moveDown()
            if target.y < self.y and self.y + self.vel >= target.y:
                self.moveUp()     
    
    def bounceBack(self,value, lastMove):
        if lastMove == "left":
            self.x += value
        if lastMove == "right":
            self.x -= value
        if lastMove == "down":
            self.y -= value
        if lastMove == "up":
            self.y += value
        if lastMove == "upleft":
            self.x += int(value/math.sqrt(2))
            self.y += int(value/math.sqrt(2))
        if lastMove == "downleft":
            self.x += int(value/math.sqrt(2))
            self.y -= int(value/math.sqrt(2))
        if lastMove == "upright":
            self.x -= int(value/math.sqrt(2))
            self.y += int(value/math.sqrt(2))
        if lastMove == "downright":
            self.x -= int(value/math.sqrt(2))
            self.y -= int(value/math.sqrt(2))
        self.hitbox = (self.x+self.r + 3, self.y + self.r+3)

    def loseHp(self, value):
        self.hp -= value

    def getUnStunned(self):
        self.isStunned = False

    def getStunned(self):
        self.isStunned = True
#########################################################################################################################################################################
#class projectile
#########################################################################################################################################################################
class projectile():
    """ self,x,y,r,color,facing, dmg, shooter, stun = False, vel = 15 """
    def __init__(self,x,y,r,color,facing, dmg, shooter, isStun = False, vel = 15, stunDuration = 20):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vel = vel
        self.facing = facing
        self.dmg = dmg
        self.shooter = shooter
        self.isStun = isStun
        self.stunDuration = stunDuration
    
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)

    def move(self, listToRemoveFrom):
        if self.facing == "left":
            if self.x < win_width and self.x > 0: 
                self.x -= self.vel

            else:
                listToRemoveFrom.pop(listToRemoveFrom.index(self))

        elif self.facing == "right":
            if self.x < win_width and self.x > 0:
                self.x += self.vel
            else:
                listToRemoveFrom.pop(listToRemoveFrom.index(self))
            
        elif self.facing == "up":
            if self.y < win_height and self.y > 0:
                self.y -= self.vel
            else:
                listToRemoveFrom.pop(listToRemoveFrom.index(self))

        elif self.facing == "down":
            if self.y < win_height and self.y > 0:
                self.y += self.vel
            else:
                listToRemoveFrom.pop(listToRemoveFrom.index(self))

        elif self.facing == "downright":
            if self.y < win_height and self.y > 0 and self.x < win_width and self.x > 0:
                self.y += int(self.vel/math.sqrt(2))
                self.x += int(self.vel/math.sqrt(2))
            else:
                listToRemoveFrom.pop(listToRemoveFrom.index(self))

        elif self.facing == "downleft":
            if self.y < win_height and self.y > 0 and self.x < win_width and self.x > 0:
                self.y += int(self.vel/math.sqrt(2))
                self.x -= int(self.vel/math.sqrt(2))
            else:
                listToRemoveFrom.pop(listToRemoveFrom.index(self))

        elif self.facing == "upright":
            if self.y < win_height and self.y > 0 and self.x < win_width and self.x > 0:
                self.y -= int(self.vel/math.sqrt(2))
                self.x += int(self.vel/math.sqrt(2))
            else:
                listToRemoveFrom.pop(listToRemoveFrom.index(self))

        elif self.facing == "upleft":
            if self.y < win_height and self.y > 0 and self.x < win_width and self.x > 0:
                self.y -= int(self.vel/math.sqrt(2))
                self.x -= int(self.vel/math.sqrt(2))
            else:
                listToRemoveFrom.pop(listToRemoveFrom.index(self))
    
    def collide(self,target):
        distance = math.hypot(self.x - target.hitbox[0],self.y - target.hitbox[1])
        return distance <= self.r + target.hitboxr 

#########################################################################################################################################################################
# függvények
#########################################################################################################################################################################
def respawn(character, charlist, vel, hp, charType):
    """respawns the object specified by the character argument"""
    randomx = random.randint(0,win_width)
    randomy = random.randint(0,win_height)
    character = player(randomx,randomy,40,hp,charType,vel)
    while isInObj(randomx, randomy, char):
        randomx = random.randint(0,win_width)
        randomy = random.randint(0,win_height)
        character = player(randomx,randomy,40,hp,charType,vel)
    charlist.append(character)

def redrawGameWindow():
    text = font.render("Kills: " + str(score), 1, (255,255,255))
    stuntext = stunfont.render("STUNNED", 1, (255,255,255))
    win.blit(hatter,(0,0))
    win.blit(text,(1100,10))
    for bullet in bullets:
        bullet.draw(win)
    char.draw(win)
    for enemy in enemies:
        enemy.draw(win)
        enemy.drawHpBar()
        if enemy.isStunned:
            enemy.writeStuntext(stuntext)
            
    char.drawHpBar()
    pygame.display.update()

def keyPressed(inputKey):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[inputKey]:
        return True
    else:
        return False

def isInObj(randomx,randomy,whereNotToSpawn):
    if randomx > whereNotToSpawn.x + whereNotToSpawn.r*2+100 or randomy > whereNotToSpawn.y + whereNotToSpawn.r*2+100 or randomx < whereNotToSpawn.x-100 or randomy < whereNotToSpawn.y-100:
        return False
    else:
        return True

#########################################################################################################################################################################
# game init
#########################################################################################################################################################################
run = True
char = player(300,300,50,Type = green,maxhp = 10, vel = 8)
enemy = player(50,50,40,Type = red,maxhp = 10,vel = 2)
enemies = []
bullets = []
enemies.append(enemy)
enemycount = 0
bulletcount = 0
shootcd = 0
fps = 40
score = 0
collisiondmg = 1
stuncd = 0

#########################################################################################################################################################################
# main loop
#########################################################################################################################################################################
while run:
    
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bulletcount += 1
            if bulletcount%5 == 0:
                char.shoot(bullets, 10, 5,stun = True)
            else:
                char.shoot(bullets,5, 3)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                char.shoot(bullets,100,500,velp = 30,)
            if event.key == pygame.K_SPACE:
                bulletcount += 1
                if bulletcount%5 == 0:
                    char.shoot(bullets,10,5,stun = True)
                else:
                    char.shoot(bullets,6,3)
    for bullet in bullets:
        bullet.move(bullets)
        enemycount = 0
        for enemy in enemies:
            if bullet.shooter == char:
                if bullet.collide(enemy) and enemycount == 0:
                    if bullet.isStun:
                        bullets.pop(bullets.index(bullet))
                        enemy.loseHp(bullet.dmg)
                        enemy.getStunned()
                        stunduration = bullet.stunDuration
                        stuncd = 0
                        enemycount += 1
                    else:
                        bullets.pop(bullets.index(bullet))
                        enemy.loseHp(bullet.dmg)
                        enemycount += 1
            elif bullet.shooter == enemy:
                if bullet.collide(char) and enemycount == 0:
                    bullets.pop(bullets.index(bullet))
                    char.loseHp(bullet.dmg)

    ###   mozgások   #################################################################################################
    if keyPressed(pygame.K_LEFT) and not char.collideWith(enemy):
        char.moveLeft()
        if keyPressed(pygame.K_UP):
            char.moveUp()
        elif keyPressed(pygame.K_DOWN):
            char.moveDown()

    elif keyPressed(pygame.K_RIGHT) and not char.collideWith(enemy):
        char.moveRight()
        if keyPressed(pygame.K_UP):
            char.moveUp()
        elif keyPressed(pygame.K_DOWN):
            char.moveDown()

    elif keyPressed(pygame.K_UP) and not char.collideWith(enemy):
        char.moveUp()
        if keyPressed(pygame.K_LEFT):
            char.moveLeft()
        elif keyPressed(pygame.K_RIGHT):
            char.moveRight()

    elif keyPressed(pygame.K_DOWN) and not char.collideWith(enemy):
        char.moveDown()
        if keyPressed(pygame.K_LEFT):
            char.moveLeft()
        elif keyPressed(pygame.K_RIGHT):
            char.moveRight()

    else:
        left = False
        right = False
        down = False
        up = False
    ###   mozgások vége   ################################################################################################

    for enemy in enemies:
        if not enemy.isStunned:
            enemy.moveTowardsTarget(char)
            shootcd += 1
            if shootcd%(fps*2) == 0:
                enemy.shoot(bullets,5,1, (0,0,0))
        
        else:
            stuncd += 1
            if stuncd >= stunduration:
                enemy.getUnStunned()
                stuncd = 0
            
        if enemy.collideWith(char):
            enemy.bounceBack(30,enemy.lastMove)
            if char.lastMove == "left" and enemy.lastMove == "right":
                char.bounceBack(20,"left")
            if char.lastMove == "right" and enemy.lastMove == "left":
                char.bounceBack(20,"right")
            if char.lastMove == "up" and enemy.lastMove == "down":
                char.bounceBack(20,"up")
            if char.lastMove == "down" and enemy.lastMove == "up":
                char.bounceBack(20,"down")
            if char.lastMove == "downright" and enemy.lastMove == "upleft":
                char.bounceBack(20,"downright")
            if char.lastMove == "downleft" and enemy.lastMove == "upright":
                char.bounceBack(20,"downleft")
            if char.lastMove == "upright" and enemy.lastMove == "downleft":
                char.bounceBack(20,"upright")
            if char.lastMove == "upleft" and enemy.lastMove == "downright":
                char.bounceBack(20,"upleft")
            char.loseHp(collisiondmg)
            enemy.loseHp(collisiondmg)
    
    for enemy in enemies:
        if enemy.hp < 1:
            enemy.die(enemies)
            score += 1
    
    if len(enemies) < 1:
        if score == 1:
            respawn(enemy,enemies,3,250,red)
        else:
            respawn(enemy,enemies,2,10,red)

    if char.hp < 1:
        del char
        print("Meghaltál!")
        break
    redrawGameWindow()

pygame.quit()
