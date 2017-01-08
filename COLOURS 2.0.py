import pygame
from pygame.locals import *
pygame.init()

import random

#SPRITES
class Ball(pygame.sprite.Sprite):
    '''A class that is a Sprite object and models a ball with properties for its colour scheme, its current colour, its image, its rect position, and its speed in the y direction.'''
    
    def __init__(self, num_colours, word_colours, back_speed, key_speed, x_position, y_position):
        '''Create a Ball that is a Sprite with a colour scheme, a y speed, and a x and y position.'''
        pygame.sprite.Sprite.__init__(self)
        
        #both a word and num colour is kept to determine collisions between walls and ball (they use different types of surfaces)
        self.word_colours = word_colours
        self.num_colours = num_colours
        
        col = random.choice(self.word_colours)
        self.image = pygame.image.load("{}.png".format(col)).convert()
        
        #parallel lists concept used to find rgb values of a word colour
        self.num_colour = self.num_colours[self.word_colours.index(col)]
        self.word_colour = col
        
        self.rect = self.image.get_rect()
        self.rect.center = (x_position, y_position)
        
        self.image.set_colorkey((255, 255, 255))
        
        self.key_speed = key_speed
        self.back_speed = back_speed
    
    def change_colour(self):
        '''B.set_colour()
        Change this Ball's colour to any colour in the colour scheme.'''
        current_colour = self.word_colours.index(self.word_colour)
        new_colours = self.word_colours[:current_colour]+self.word_colours[current_colour+1:]
        
        #randomly choose a new colour and change self's rgb value and word colour
        self.word_colour = random.choice(new_colours)
        self.num_colour = self.num_colours[self.word_colours.index(self.word_colour)]
        self.image = pygame.image.load("{}.png".format(self.word_colour)).convert()  

    def update(self, x_moving, x_direction, y_moving, y_direction):
        '''B.update(bool, int, bool, int)
        Update this Ball so it is moving when the arguement(moving) is True.'''
        
        #direction will be determined if up or down arrow key is pressed
        if y_moving == True:
            self.rect.move_ip(0, self.key_speed*y_direction)
        if x_moving == True:
            self.rect.move_ip(self.key_speed*x_direction, 0)  
        else:
            self.rect.move_ip(self.back_speed*-1, 0)

class Wall(pygame.sprite.Sprite):
    '''A class that is a Sprite and models a segment of a Wall with properties for its colour, x and y speed, x and y position.'''
    
    def __init__(self, word_colour,num_colour, x_speed, y_speed, x_position, y_position):
        '''Create a Wall that is a Sprite with a colour, x/y speed, and x/y position.'''
        pygame.sprite.Sprite.__init__(self)
        
        self.num_colour = num_colour
        self.word_colour = word_colour
        self.image = pygame.Surface((20, 105)).convert()
        self.image.fill(self.num_colour)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x_position, y_position)
        
        self.x_speed = x_speed
        self.y_speed = y_speed  

    def inc_speed(self):
        '''W.inc_speed()
        Increase this Wall's speed by one pixel.'''
        self.y_speed += 1
    
    def update(self):
        '''W.update()
        Update this Wall's position so that it is moved to the beginning if it goes off the screen.'''
        
        #x_speed must be negative because the wall is moving to the left
        self.rect.move_ip(self.x_speed*-1, self.y_speed)
        
        #change its positions if it goes off the screen
        if self.rect.right <= 0:
            self.rect.left = screen.get_width()+250
        elif self.rect.top >= screen.get_height():
            self.rect.bottom = 0

class Obstacle(pygame.sprite.Sprite):
    '''A class that is a Sprite and models a game Obstacle with properties for its x/y speed, and y position.'''
    
    def __init__(self, x_speed, x_position, y_position):
        '''Create an Obstacle that is a Sprite with x speed, and x/y positions.'''
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((20, 20)).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (x_position, y_position)
        self.x_speed = x_speed         
    
    def change_position(self):
        '''O.change_pos()
        Change this Obstacle's position.'''
        x_pos = self.rect.center[0] + screen.get_width() + 20
        y_pos = random.randrange(20, screen.get_height()-20)
        self.rect.center = (x_pos, y_pos)
  
    def update(self):
        '''O.update()
        Update this Obstacle so that it moves.'''
        self.rect.move_ip(self.x_speed*-1, 0)
    
class Star(Obstacle):
    '''A class that is an Obstacle and models a Star(points) with properties for its x speed, and x/y position.'''
    
    def __init__(self, x_speed, x_position, y_position):
        '''Create a Star that is an Obstacle with x speed, and x/y positions.'''
        Obstacle.__init__(self, x_speed, x_position, y_position)
        
        self.image = pygame.image.load("star.png").convert()
        self.image.set_colorkey((255, 255, 255))
   
class Bomb(Obstacle):
    '''A class that is an Obstacle and models a Bomb with properties for its x speed, and x/y position.'''
    
    def __init__(self, x_speed, x_position, y_position):
        '''Create a Bomb that is an Obstacle with x speed, and x/y positions but a different image.'''
        Obstacle.__init__(self, x_speed, x_position, y_position)
        
        self.image = pygame.image.load("bomb.png").convert()
        self.image.set_colorkey((255, 255, 255))

class Font(pygame.sprite.Sprite):
    '''A class that is a Sprite object and models any font that will occur during the game.'''
    
    def __init__(self, colour, text, pos, size):
        '''Create a Font Sprite with rect coordinate(pos), size of the font, and the text.'''
        pygame.sprite.Sprite.__init__(self) 
        self.text = text
        self.size = size 
        self.colour = colour
        
        self.my_font = pygame.font.SysFont("impact", self.size)
        self.image = self.my_font.render("{}".format(self.text), True, self.colour)
        
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    def update(self, update, text):
        '''F.update(str)
        Update this font's text.'''
        
        #true when font of score is being updated every cycle, but false when a font must be constant
        if update == True:
            self.text = text
            self.image = self.my_font.render("{}".format(self.text), True, self.colour)

#OTHER CLASSES
class Score(object):
    '''A class that models a user's Score and has properties for the current score and username.'''
    
    def __init__(self, score, file):
        '''Create a Score with a current score and filename.'''
        self.__score = score
        self.__file = file

    def increase(self):
        '''S.score_increase()
        Increase this Score's score.'''
        self.__score += 1

    def get_score(self):
        '''S.get_score() --> int
        Return this Score's score property.'''
        return int(self.__score)

    def best(self):
        '''S.best() --> list
        Store the current score in self.__file, and then return text stating whether self.__score is greater than any score stored in self.__file'''
        lines = []
        out = []
        in_file = open(self.__file)
        
        for line in in_file:
            lines.append(int(line.strip("\n")))

        if self.__score > max(lines):
            out.append("Congratulations")
            out.append("New Best Score")
            out.append("{}".format(self.__score))
        else:
            out.append("Better Luck Next Time")
            out.append("Current Best Score")
            out.append("{}".format(max(lines)))

        in_file.close()  
        
        out_file = open(self.__file, "w")
        out_file.write("{}\n".format(self.__score))
        
        #rewrite file to add new score
        for n in lines:
            out_file.write("{}\n".format(n))
        out_file.close() 
        
        return out
    
    def __str__(self):
        '''S.__str__() or str(S) --> str
        Return the string version of this Score in the format "self.__score"'''
        return "{}".format(self.__score)    

#SCREEN SETUP
size = (600, 300)
screen = pygame.display.set_mode(size)
background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))
screen.blit(background, (0, 0))  

#SOUNDS
bomb = pygame.mixer.Sound("bomb.wav")
bomb.set_volume(1.0)

new_score = pygame.mixer.Sound("yay.wav")
new_score.set_volume(1.0)

bad_score = pygame.mixer.Sound("sad male.wav")
bad_score.set_volume(1.0)

ting = pygame.mixer.Sound("ting.wav")
ting.set_volume(1.0)

#VARIABLES
clock = pygame.time.Clock()
keep_going = True
quit = False

#SPRITES FOR LOOP 1
#star group
stars = []

for x in range(0, 5):
    for y in range(0, 10):
        stars.append(Star(0, 30+(y*60), 30+(60*x)))
star_group_1 = pygame.sprite.Group(stars)

#font group
fonts = []
start_font = Font((255, 181, 197),"START", (screen.get_width()//2, (screen.get_height()//2)+60), 70)
fonts.append(Font((221, 160, 221), "COLOURS!", (screen.get_width()//2, (screen.get_height()//2)-60), 80))
fonts.append(start_font)
font_group = pygame.sprite.Group(fonts)

#GAME LOOP 1
while keep_going:
    clock.tick(30)
    
    pygame.display.set_caption("COLOURS: Press start to begin!")
    
    #to clear stars that collide with the words (to be able to read it clearly)
    pygame.sprite.groupcollide(star_group_1, font_group, True, False)
    
    #EVENT HANDLING
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            keep_going = False
            quit = True
            
        elif ev.type == MOUSEBUTTONDOWN:
            x = ev.pos[0]
            y = ev.pos[1]
            if start_font.rect.collidepoint(x, y) == True:
                keep_going = False
        
        elif ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                keep_going = False
    
    #CLEAR/UPDATE/DRAW
    #the following is done to ONLY clear the screen if the game loop finishes and not re-update/draw
    star_group_1.clear(screen, background)
    font_group.clear(screen, background)
    
    if keep_going != False:
        star_group_1.update()
        font_group.update(False, " ")
        star_group_1.draw(screen)   
        font_group.draw(screen) 
    
    pygame.display.flip()   

#VARIABLES
if quit != True:
    keep_going = True

#ball starts with no motion    
y_moving = False
y_direction = 1
x_moving = False
x_direction = 1

#counter variable explained further down in the game loop
counter = -1
points = 0

#SPRITES
#both are kept track of in order to detect collisions between ball and wall
word_colours = ["pink", "purple", "blue", "green"]
num_colours = [(255, 181, 197), (221, 160, 221), (135, 206, 235), (193, 255, 193)]

#ball group
ball = Ball(num_colours, word_colours, 1, 5, 50, screen.get_height()//2)
ball_group = pygame.sprite.Group(ball)

#wall group
walls = []
x_pos = 50

for n in range(0, 7):
    num = random.randrange(0, 4)
    y_pos = random.randrange(0, -50, -1)
    x_pos += 125
    for n in range(0, 4):
        walls.append(Wall(word_colours[num], num_colours[num], 1, 2, x_pos, y_pos))
        y_pos += 100
        
        num += 1
        if num == 4:
            num = 0
wall_group = pygame.sprite.Group(walls)

#star/bomb groups
stars = []
bombs = []
x_pos = 110
for n in range(0, 5):
    x_pos += 125
    y_pos_1 = random.randrange(15, screen.get_height()-15)
    stars.append(Star(1, x_pos, y_pos_1))
    
    y_pos_2 = random.randrange(15, screen.get_height()-15)
    
    #to ensure that a bomb wont be placed in same position as star
    if y_pos_1 == y_pos_2 or y_pos_1 >= y_pos_2 + 20 and y_pos_1 <= y_pos_2 - 20:
        y_pos_2 += 30
        
    bombs.append(Bomb(1, x_pos, y_pos_2))    

star_group_2 = pygame.sprite.Group(stars)
bomb_group = pygame.sprite.Group(bombs)

#score class
score = Score(0, "userdata.txt")

#font group
fonts = []
fonts.append(Font((0, 0, 0), score, (525, 250), 80))
font_group = pygame.sprite.Group(fonts)

#GAME LOOP 2
while keep_going:
    clock.tick(30)
    
    pygame.display.set_caption("POINTS: {}".format(score))
    
    #BORDER TEST
    if ball.rect.bottom > screen.get_height() or ball.rect.top < 0 or ball.rect.left < 0 or ball.rect.right > screen.get_width() :
        keep_going = False
    
    #WALL COLLISIONS
    w_collisions = pygame.sprite.spritecollide(ball, wall_group, False)
    if len(w_collisions) != 0:
        counter = 5

    for n in w_collisions:
        if n.num_colour != ball.num_colour:
            keep_going = False
    
    #to delay the change of colour (if changed right away the ball collides with the "incorrect" colour)
    if counter == 0:
        ball.change_colour()
        counter = -1
    elif counter > 0:
        counter -= 1
    
    #STAR COLLISIONS
    #instead of killing the stars off this moves them to a new position to go through the game screen again (^ see change_position() methods ^)
    list_points = pygame.sprite.spritecollide(ball, star_group_2, False)
    for n in list_points:
        n.change_position()
        score.increase()
        ting.play()
        
        #to increase difficulty every 10 points earned (uses inc_speed() methods)
        if score.get_score()%10  == 0:
            for n in wall_group:
                n.inc_speed()            
    
    #to move any left over stars/bombs that moved off the screen back to the other side of the screen (^ see change_position() methods ^)
    #used instead of update() because of stars that collide with ball, they are moved but dont go off the screen
    for n in star_group_2:
        if n.rect.right <= 0:
            n.change_position()
    for n in bomb_group:
        if n.rect.right <= 0:
            n.change_position()    

    #BOMB COLLISIONS
    bomb_list = pygame.sprite.spritecollide(ball, bomb_group, False)
    if (len(bomb_list)) > 0:
        bomb.play()
        keep_going = False
        

    #EVENT HANDLING
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            keep_going = False
    
    #KEY EVENTS
    keys = pygame.key.get_pressed()
    
    #event handling of motion in the x-axis
    if keys[K_LEFT]:
        x_moving = True
        x_direction = -1   
    elif keys[K_RIGHT]:
        x_moving = True
        x_direction = 1
    else:
        x_moving = False
    
    #event handling of motion in the y-axis    
    if keys[K_UP]:
        y_moving = True
        y_direction = -1    
    elif keys[K_DOWN]:
        y_moving = True
        y_direction = 1    
    else:
        y_moving = False
    
    #CLEAR/UPDATE/DRAW
    star_group_2.clear(screen, background)
    bomb_group.clear(screen, background)
    ball_group.clear(screen, background)        
    wall_group.clear(screen, background)
    font_group.clear(screen, background)
    
    if keep_going != False:
        star_group_2.update()
        bomb_group.update()
        ball_group.update(x_moving, x_direction, y_moving, y_direction)
        wall_group.update()
        font_group.update(True, score)
        star_group_2.draw(screen) 
        bomb_group.draw(screen)
        ball_group.draw(screen)
        wall_group.draw(screen) 
        font_group.draw(screen)
    
    pygame.display.flip()   

#to store the current score and to determine if it is the best score only if the user plays
best = score.best() 

#VARIABLES
#if user quits from begininng
if quit != True:   
    keep_going = True

#FONTS
fonts = []

fonts.append(Font((255, 181, 197), "GAME OVER!", (screen.get_width()//2, (screen.get_height()//2)-65), 70))
fonts.append(Font((221, 160, 221), "{}".format(best[0]), (screen.get_width()//2, (screen.get_height()//2)-10), 40))
fonts.append(Font((255, 181, 197), "{}".format(best[1]), (screen.get_width()//2, (screen.get_height()//2)+30), 30))
fonts.append(Font((221, 160, 221), "{}".format(best[2]), (screen.get_width()//2, (screen.get_height()//2)+75), 55))

font_group = pygame.sprite.Group(fonts)

#SOUNDS
if best[0] == "Congratulations":
    new_score.play()
else:
    bad_score.play()

#GAME LOOP 3
while keep_going:
    clock.tick(30)
    
    pygame.display.set_caption("COLOURS!")
    
    #to clear stars that collide with the words (to be able to read it clearly)
    pygame.sprite.groupcollide(star_group_1, font_group, True, False)
    
    #EVENT HANDLING
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            keep_going = False
    
    #CLEAR/UPDATE/DRAW
    star_group_1.clear(screen, background)        
    font_group.clear(screen, background)
    star_group_1.update()
    font_group.update(False, " ")
    star_group_1.draw(screen)
    font_group.draw(screen)
    pygame.display.flip()   