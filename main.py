#Importing modules

import pygame,  sys
from pygame.locals import *
pygame.init()

#Defining the window

window_height=600 
window_width=1200

blue = (0,0,255)
black = (0,0,0)
white = (255, 255, 255)

fps = 25
level = 0
addnewflamerate = 20


addnewbuildingrate=50

mainClock = pygame.time.Clock()
#creating canvas
Canvas = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Subway Surfers')



#defining the required function
#class for the monster
class dragon:

    global firerect, imagerect, Canvas
    up = False
    down = True
    velocity = 15
    
    def __init__(self):
        self.image = load_image('g1.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.right = window_width
        self.imagerect.top = window_height/2

    def update(self):
        
        if (self.imagerect.top < cactusrect.bottom):
            self.up = False
            self.down = True

        if (self.imagerect.bottom > firerect.top):
            self.up = True
            self.down = False
            
        if (self.down):
            self.imagerect.bottom += self.velocity

        if (self.up):
            self.imagerect.top -= self.velocity

        Canvas.blit(self.image, self.imagerect)

    def return_height(self):

        h = self.imagerect.top
        return h

#class for the monster throwing objects
class flames:
    flamespeed = 10

    def __init__(self):
        self.image = load_image('mini-ghosts.png')
        self.imagerect = self.image.get_rect()
        self.height = Dragon.return_height() + 30
        self.surface = pygame.transform.scale(self.image, (30,30))
        self.imagerect = pygame.Rect(window_width - 106, self.height, 30, 30)

    def update(self):
            self.imagerect.left -= self.flamespeed

    def collision(self):
        if self.imagerect.left == 0:
            return True
        else:
            return False

#class for the player
class witch:
    global moveup, movedown, gravity, cactusrect, firerect
    speed = 10
    downspeed = 20

    def __init__(self):
        self.image = load_image('witch.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.topleft = (50,window_height/2)
        self.score = 0
        
    def keep_score(self):
        self.score=mainClock.tick(fps)   
        
    def update(self):
        
        if (moveup and (self.imagerect.top > cactusrect.bottom)):
            self.imagerect.top -= self.speed
            
            
        if (movedown and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.downspeed
            
            
        if (gravity and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.speed


#function to end the program
def terminate():
    pygame.quit()
    sys.exit()

def waitforkey():
    #function to wait for user to start
    while True :                                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:     #function to terminate if the user presses the escape key
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return
def ghosthit(playerrect, flames):      #function to check if the ghost has hit the player or not
    for f in flame_list:
        if playerrect.colliderect(f.imagerect):
            return True
        return False

def drawtext(text, font, surface, x, y):        #function to display text on the screen
    textobj = font.render(text, 1, white)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

def check_level(score):                     #function to check the level of the player
    global window_height, level, cactusrect, firerect
    if score in range(0,10):
        firerect.top = 550
        cactusrect.bottom = 50
        level = 1
    elif score in range(10, 30):
        firerect.top = 550 
        cactusrect.bottom = 100
        level = 2
    elif score in range(30,50):
        level = 3
        firerect.top = 550
        cactusrect.bottom = 150
    elif score in range(50,4000):
        level = 4
        firerect.top = 550 
        cactusrect.bottom = 200

def load_image(imagename):
    return pygame.image.load(imagename)

space = pygame.transform.scale(load_image('firey-road.png') ,(window_width,window_height))


#setting up font and sounds and images

font = pygame.font.SysFont(None, 48)
scorefont = pygame.font.SysFont(None, 30)

fireimage = load_image('fire_bricks_upside_down.png')
firerect = fireimage.get_rect()


cactusimage = load_image('fire_bricks.png')
cactusrect = cactusimage.get_rect()

startimage = load_image('start.png')
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width/2
startimagerect.centery = window_height/2

endimage = load_image('end.png')
endimagerect = startimage.get_rect()
endimagerect.centerx = window_width/2
endimagerect.centery = window_height/2

pygame.mixer.music.load('Ratsasan-Piano-BGM.wav')
gameover = pygame.mixer.Sound('Theme Halloween.mp3')
death = pygame.mixer.Sound('Scream.mp3')

#getting to the start screen

drawtext('subway surfers', font, Canvas,(window_width/3), (window_height/3))
Canvas.blit(startimage, startimagerect)

pygame.display.update()
waitforkey()

#start of the main code

topscore = 0
Dragon = dragon()

#creating rect for crate
crate = pygame.image.load('Building.png')
crate = pygame.transform.rotozoom(crate,0,0.8)
crate_x = 700
crate_speed = 6

while True:
    health=3
    flame_list = []
    player = witch()
    moveup = movedown = gravity = False
    flameaddcounter = 0

    gameover.stop()
    pygame.mixer.music.play(-1,0.0)

    bgx = 0
    print("outer while")

    while True:     #the main game loop
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            #code to move the player UP and DOWN
            if event.type == KEYDOWN:
                
                if event.key == K_UP:
                    movedown = False
                    moveup = True
                    gravity = False

                if event.key == K_DOWN:
                    movedown = True
                    moveup = False
                    gravity = False

            if event.type == KEYUP:

                if event.key == K_UP:
                    moveup = False
                    gravity = True
                if event.key == K_DOWN:
                    movedown = False
                    gravity = True
                    
                if event.key == K_ESCAPE:
                    terminate()

        flameaddcounter += 1
        
        
        check_level(player.score)
        
        if flameaddcounter == addnewflamerate:

            player.score += 1
            flameaddcounter = 0
            newflame = flames()
            flame_list.append(newflame)

        
        
        for f in flame_list:
            flames.update(f)

        for f in flame_list:
            if f.imagerect.left <= 0:
                flame_list.remove(f)

        player.update()
        Dragon.update()
        

        # Canvas.fill(black)
        Canvas.blit(space,(bgx-window_width,0))
        Canvas.blit(space,(bgx,0))
        Canvas.blit(space,(bgx+window_width,0))
        
        bgx = bgx - 4
        if bgx <= (-window_width):
            bgx = 0
        
        Canvas.blit(fireimage, firerect)
        Canvas.blit(cactusimage, cactusrect)
        Canvas.blit(player.image, player.imagerect)
        Canvas.blit(Dragon.image, Dragon.imagerect)
        
        c_rect = Canvas.blit(crate,(crate_x,350))
        crate_x -= crate_speed
        if crate_x < -50:
            crate_x = 1400
            
        if player.imagerect.colliderect(c_rect):
            death.play()
            death.fadeout(3000)
            pygame.mixer.music.play(-1,0.0)
            health -= 1
            if player.score > topscore:
                topscore = player.score
            if(health == 0):
                crate_x = 700
                flame_list = []
                flameaddcounter=0
                break
            crate_x = 700
            flame_list = []
            flameaddcounter=0
            continue
                        
        #code to display text while the player is playing
        drawtext('Score : %s | Top score : %s | Level : %s | Lives : %s' %(player.score, topscore, level, health), scorefont, Canvas, 350, cactusrect.bottom + 10)
        
        for f in flame_list:
            Canvas.blit(f.surface, f.imagerect)

               
        #code to modify the health after the player is hit by the ghost
        if ghosthit(player.imagerect, flame_list):
            death.play()
            death.fadeout(3000)
            pygame.mixer.music.play(-1,0.0)
            health -= 1
            if player.score > topscore:
                topscore = player.score
                
            if(health == 0):
                crate_x = 700
                flame_list = []
                flameaddcounter=0
                break
            crate_x = 700
            flame_list = []
            flameaddcounter=0


        pygame.display.update()
    

        mainClock.tick(fps)
    
    pygame.mixer.music.stop()
    gameover.play()
    #code to take player to the end screen and display top score
    Canvas.blit(endimage, endimagerect)
    drawtext('Top score : %s' %( topscore), scorefont, Canvas, 1000, cactusrect.bottom + 4)

    pygame.display.update()
    waitforkey()
        