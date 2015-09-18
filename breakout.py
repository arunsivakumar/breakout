import pygame
import random
import math
import sys
from colors import *

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
 
        # Call Sprite constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        
        # Update the position of this object
        self.rect = self.image.get_rect()

class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
 
        # Call Sprite constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Update the position of this object
        self.rect = self.image.get_rect()

# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# block width, height, starting and ending location
block_w = (screen_width / 15) 
block_h = 7
block_x = 0
block_y = 50

# number of rows and columns of brick
rows = 7
columns = 20

# colors from top to bottom of the bricks
colors = [RED,ORANGE,YELLOW,GREEN,BLUE,INDIGO,VIOLET]


# List of sprites
block_list = pygame.sprite.Group()
 
# List of all the sprites
all_sprites_list = pygame.sprite.Group()
paddle_list = pygame.sprite.Group()

### Drawing the blocks


for i in range(rows):
    for j in range(columns):
        # This represents a block
        block = Block(colors[i], block_w, block_h)
 
        # Set location for the block
        block.rect.x = block_x
        block.rect.y = block_y
 
        # Add the block to the list of objects
        block_list.add(block)
        all_sprites_list.add(block)
        block_x = block_x + block_w +1
    block_x = 0
    block_y = block_y + block_h + 1

# Create paddle 
paddle_h = 10
paddle_w = 70

paddle_y = screen_height - paddle_h

paddle = Block(BLUE, paddle_w, paddle_h)
all_sprites_list.add(paddle)
paddle_list.add(paddle)

# Ball details

ball_w = 5
ball_h = 5

ball_change_x = 5
ball_change_y = 3

ball = Ball(BLUE,ball_w,ball_h)
all_sprites_list.add(ball)

ball.rect.x = 200
ball.rect.y = 200

# Loop until the user clicks the close button.

done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

score = 0
brick_hit_count = 0
game_not_done = True

delay = 0


# -------- Main Program Loop -----------
while game_not_done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
 
    # Clear the screen
    screen.fill(WHITE)

    
    # Get the current mouse position. 
    pos = pygame.mouse.get_pos()

    if(delay == 0):
        pygame.time.delay(2000)
        delay = 1
        
    # Fetch the x and y locations
    paddle.rect.x = pos[0]
    paddle.rect.y = paddle_y

    if paddle.rect.x > (screen_width - paddle_w):
       paddle.rect.x = (screen_width - paddle_w)

    # Ball logic
    ball.rect.x += ball_change_x
    ball.rect.y += ball_change_y
    
    if ball.rect.x > (screen_width - ball_w - 1) or ball.rect.x < 0:
        ball_change_x *= -1

    if  ball.rect.y < 0:
        ball_change_y *= -1
    if ball.rect.y > screen_height:
        game_not_done = False
        break

     # check paddle collision
   
    if(pygame.sprite.spritecollide(ball, paddle_list, False)):
        ball_change_y *= -1
  
    # Block collision with ball
    if(pygame.sprite.spritecollide(ball, block_list, True)):
        brick_hit_count += 1
        if (brick_hit_count == (rows * columns)):
           game_not_done = False
           break
        if(brick_hit_count == 15):
            ball_change_x = 6
            ball_change_y = 4
        if(brick_hit_count == 30):
            ball_change_x = 7
            ball_change_y = 5
        if(brick_hit_count == 45):
            ball_change_x = 8
            ball_change_y = 6
        
        ball_change_y *= -1
 
    # Draw all the objects on the screen
    all_sprites_list.draw(screen)
 
    # Screen update
    pygame.display.flip()

   
    # 50 frames per second - game running
    clock.tick(50)
    
while True:   
        basicfont = pygame.font.SysFont(None, 48)
        #check if user wins
        if (brick_hit_count == (rows*columns)):
            text = basicfont.render('You Win!!!', True, (255, 0, 0), (255, 255, 255))
        # check if user loses 
        else:
            text = basicfont.render('Game Over!!!', True, (255, 0, 0), (255, 255, 255))
        textrect = text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery
 
        screen.fill((255, 255, 255))
        screen.blit(text, textrect)
 
        pygame.display.update()
        
        # delay until screen closes
        if(delay == 1):
            pygame.time.delay(3000)
            delay = 2
        pygame.quit()
