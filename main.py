import pygame, sys
import math
from spaceship import SpaceShip

# Game Structure 
pygame.init
# Using the standerd comp graphics where 0,0 is the top left corner
screen_width = 750
screen_height = 700

GREY = (29, 29, 27)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python Space Invaders")

clock = pygame.time.Clock()

spaceship = SpaceShip(screen_width, screen_height)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Updating
    spaceship_group.update()

    #Drawing 
    screen.fill(GREY)
    spaceship_group.draw(screen)
    spaceship_group.sprite.lasers_group.draw(screen)

    pygame.display.update()
    clock.tick(60) # Makes the clock run 60 times a second Delta Time -ish 
