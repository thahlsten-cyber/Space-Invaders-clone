import pygame 
from lazar import Lazar

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, offset):
        super().__init__() # Initializes our SS sprite by taking the Sprite (parent class) 's own init
        self.offset = offset
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("Graphics/spaceship.png")
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, screen_height))
        self.speed = 6
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 300
        self.laser_sound = pygame.mixer.Sound("Sounds/laser.ogg")

    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Lazar(self.rect.center, 5, self.screen_height)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks() # Sets laser time at the time it was fired saving that tick in the variable
            self.laser_sound.play()
            
    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    def constrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < self.offset:
            self.rect.left = self.offset

    def recharge_laser(self):
        if not self.laser_ready: # if laser is false saves current time and then checks if the dif of current time to time init fired is over delay time
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
        self.lasers_group.empty()
