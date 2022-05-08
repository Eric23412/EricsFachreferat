import pygame
import math
import random

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((960,540))
done = False
clock = pygame.time.Clock()





hitwall = False
spawn = False



class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,typenumber):
        super().__init__()
        self.type = ['Graphics/Enemy0.bmp','Graphics/Enemy1.bmp','Graphics/Enemy2.bmp']
        self.scoredrop = [100,250,500]
        self.scoredrop = self.scoredrop[typenumber]
        self.image = pygame.image.load(self.type[typenumber]).convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.k = 1
        self.deathsound = pygame.mixer.Sound("Sounds/hitHurt.wav")

    def Move(self):        
        global hitwall
        global playerhealth
        self.rect.x += self.k*10        
        if self.rect.right > 960 or self.rect.left < 0:  
            hitwall = True
        if self.rect.y > 540: playerhealth -= 1
    

    def Hit(self):
        global score
        global playerhealth
        global bombammo
        if pygame.sprite.spritecollide(self,bullets,True) or pygame.sprite.spritecollide(self,bombs,False):
            if bombs.__len__() == 1: bombs.sprite.exploded = True
            score += self.scoredrop
            if random.randint(0,10000)>9925: 
                if random.randint(0,1) == 1: playerhealth += 1
                else: bombammo += 1
            self.deathsound.play()
            self.kill()
        
    def update(self):
        self.Hit()



class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,i):
        super().__init__()
        self.image = pygame.image.load('Graphics/Planets.bmp').convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.direction = i

    def update(self):
        self.rect.y -= 5*self.direction
        if self.rect.y < 0 or self.rect.y > 540:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.Bombimage = pygame.image.load('Graphics/Planets1.bmp').convert_alpha()
        self.Explosionimage = pygame.image.load('Graphics/Explosion.bmp').convert_alpha()
        self.sound = pygame.mixer.Sound("Sounds/explosion.wav")
        self.states = [self.Bombimage, self.Explosionimage]
        self.image = self.states[0]
        self.rect = self.image.get_rect(center=(x,y))
        self.exploded = False
        self.starttime = 0
        self.Test = False
    

    def Main(self):
        if not self.exploded:
            self.rect.y -= 5
            self.starttime = pygame.time.get_ticks()
        else:
            time = pygame.time.get_ticks() - self.starttime
            if time > 2000:
                self.kill()
        if self.rect.y < 0:
            self.kill()


    def Explode(self):
        global score
        if self.exploded == True and self.Test == False:
            self.sound.play(0)
            self.image = self.states[1]
            self.rect = self.image.get_rect(center=(self.rect.centerx,self.rect.centery))
            self.Test = True


    def update(self):
        self.Main()
        self.Explode()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Graphics/Player.bmp').convert_alpha()
        self.rect = self.image.get_rect(topleft=(480,450))

    def Inputs(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] and self.rect.right < 960: self.rect.x += 10
        if pressed[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= 10
        if pressed[pygame.K_w]: self.rect.y -=10

    def update(self):
        self.Inputs()


background = pygame.image.load("Graphics/Background.bmp")
TextFont = pygame.font.Font("Fonts/BAUHS93.OTF", 25)
shootsound = pygame.mixer.Sound("Sounds/Shoot.wav")
playmusic = True
gameover = False
gamestarted = False
playerhealth = 3
weapon = 0
Relod = 1
RelodSpeed = 1
score = 0
StartTime = pygame.time.get_ticks()
tickspeed = 1

HiScore = open("Save/Hi-Score.txt","a")
HiScoreName = ["A","A","A"]
Underscore = [450,462,474]
namepos = 0
f = 0

bombammo = 5
selectedweapon = [pygame.image.load('Graphics/Planets1.bmp').convert_alpha(),pygame.image.load('Graphics/Planets.bmp').convert_alpha()]

bombs = pygame.sprite.GroupSingle()
bullets = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
enemys = pygame.sprite.Group()

def restart(): 
    player.empty()
    bullets.empty()
    enemys.empty()
    player.add(Player())
    x = 0
    for i in range(0,5):
        for u in range(1,13):
            enemys.add(Enemy((u*70),(250-50*i),math.floor(x)))
        x += 0.5
    
restart()



while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if gameover == True:
                if event.key == pygame.K_UP: f = 1
                if event.key == pygame.K_DOWN: f= -1
                if f != 0: 
                    HiScoreName[namepos] = chr(ord(HiScoreName[namepos])+f)
                    if ord(HiScoreName[namepos]) > 90: HiScoreName[namepos] = chr(65)
                    elif ord(HiScoreName[namepos]) < 65: HiScoreName[namepos] = chr(90)
                    f = 0
                if event.key == pygame.K_LEFT: 
                    if namepos != 0: namepos -= 1
                    else: namepos = 2
                if event.key == pygame.K_RIGHT:
                    if namepos != 2: namepos += 1
                    else: namepos = 0
                if event.key == pygame.K_RETURN: 
                    HiScore.write(''.join(HiScoreName) + ": " + str(score) + chr(13))
                    done = True

            if event.key == pygame.K_RETURN and not gameover: gamestarted = True

            if event.key == pygame.K_UP and weapon < 1: weapon +=1
            if event.key == pygame.K_DOWN and weapon > 0: weapon -=1
    
    screen.blit(background,(0,0))

    if gamestarted:

        if pygame.time.get_ticks() - StartTime > 1280/tickspeed:
            
            for sprite in enemys:
                try:
                    sprite.Move()
                except: 1==1
            if random.randint(1,10000)>6500:
                i = random.randint(0,enemys.__len__())
                z = 0
                for sprite in enemys:
                    if z == i:
                        shootsound.play(0)
                        enemys.add(Bullet(sprite.rect.centerx,sprite.rect.centery,-1))
                    z+=1
            
            if enemys.__len__() > 44: tickspeed = 1
            elif enemys.__len__() > 33: tickspeed = 1.5
            elif enemys.__len__() > 22: tickspeed = 2.5
            elif enemys.__len__() > 11: tickspeed = 4
            elif enemys.__len__() > 1: tickspeed = 5
            StartTime = pygame.time.get_ticks()


        


        if hitwall == True:
            for sprite in enemys:
                try:
                    sprite.k = -sprite.k
                    sprite.rect.centery += 25
                    sprite.rect.x += sprite.k*10
                except: 1==1
                hitwall = False
        if pygame.sprite.spritecollide(player.sprite, enemys, True):
            pygame.mixer.Sound("Sounds/PlayerHit.wav").play()
            playerhealth -= 1
        if enemys.__len__() == 0:
            score += 500
            gamestarted = False
            restart()
    
        pressed = pygame.key.get_pressed()

        if weapon == 0: RelodSpeed = 2.75
        elif weapon == 1: RelodSpeed = 0.5
        if pressed[pygame.K_SPACE] and Relod >= 1:
            shootsound.play(0)
            if weapon == 0: 
                bullets.add(Bullet(player.sprite.rect.centerx,player.sprite.rect.centery,1))
                Relod = 0
            elif weapon == 1 and bombammo > 0:
                Relod = 0
                bombammo -= 1
                bombs.add(Bomb(player.sprite.rect.centerx,player.sprite.rect.centery))
        if Relod < 1:
            Relod += 0.01*RelodSpeed
            pygame.draw.rect(screen,(255,255,255),pygame.Rect(player.sprite.rect.x, player.sprite.rect.y+45, Relod*40, 5))
        

        
        if playerhealth <= 0:
            gamestarted = False
            gameover = True
        
        else:
            player.update()
            enemys.update()
            bullets.update()
            bombs.update()
        

        pygame.draw.rect(screen,(255,255,255),pygame.Rect(895,460,60,60))
        screen.blit(selectedweapon[weapon-1],selectedweapon[weapon-1].get_rect(center=(925,490)))
        if weapon == 1: screen.blit(TextFont.render(str(bombammo),True,(0,0,0)),  (900,500))
        screen.blit(TextFont.render("Your Lifes: " + str(playerhealth),True,(255,255,255)),  (5,500))
        screen.blit(TextFont.render("Score: " + str(score),True,(255,255,255)),  (5,20))
        bombs.draw(screen)
        player.draw(screen)
        bullets.draw(screen)
        
        enemys.draw(screen)
        

    else:
        starttext = TextFont.render("Press Enter to Continue",True,(255,255,255))

        screen.blit(starttext,starttext.get_rect(center=(480,300)))
    
    if gameover == True:
        scoretext = TextFont.render("Final Score: " + str(score),True,(255,255,255))
        gameovertext = TextFont.render("Game Over enter your name and save your HiScore",True,(255,255,255))

        screen.blit(scoretext,scoretext.get_rect(center=(480,200)))
        screen.blit(gameovertext,gameovertext.get_rect(center=(480,250)))
        screen.blit(TextFont.render(''.join(HiScoreName),True,(255,255,255)),(450,265))
        screen.blit(TextFont.render("_",True,(255,255,255)),(Underscore[namepos],270))


    pygame.display.flip()
    clock.tick(60)

pygame.display.quit()
pygame.quit()
