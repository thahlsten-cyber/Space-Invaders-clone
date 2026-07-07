import pygame, sys, random
from game import Game
from spaceship import SpaceShip

class Button:
    def __init__(self, x, y, width, height, text, color, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.callback = callback
        self.font = pygame.font.Font("Font/monogram.ttf", 40)
        self.GREY = (29, 29, 27)
        self.YELLOW = (243, 216, 63)
    def draw(self, surface):
        # Drawing box
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        #Yellow theme
        pygame.draw.rect(surface, (243, 216, 63), self.rect, width=2, border_radius=5)

        # Draw text in center of rect
        text_surface = self.font.render(self.text, False, self.YELLOW)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def event_handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
    
        
class initalizer:
    def __init__(self):
        # Game Structure 
        pygame.init()
        # Using the standerd comp graphics where 0,0 is the top left corner
        self.shop_triggered = False 
        self.SCREEN_WIDTH = 750
        self.SCREEN_HEIGHT = 700
        self.OFFSET = 50

        self.GREY = (29, 29, 27)
        self.YELLOW = (243, 216, 63)

        self.font = pygame.font.Font("Font/monogram.ttf", 40)
        self.level_surface = self.font.render("LEVEL 01", False, self.YELLOW)
        self.game_over_surface = self.font.render("GAME OVER", False, self.YELLOW)
        self.score_text_surface = self.font.render("SCORE", False, self.YELLOW)
        self.highscore_text_surface = self.font.render("HIGH-SCORE", False, self.YELLOW)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH + self.OFFSET, self.SCREEN_HEIGHT + 2*self.OFFSET))
        pygame.display.set_caption("Python Space Invaders")

        self.clock = pygame.time.Clock()

        self.game = Game(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.OFFSET)

        self.SHOOT_LASER = pygame.USEREVENT
        pygame.time.set_timer(self.SHOOT_LASER, 300)

        self.MYSTER_SHIP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MYSTER_SHIP, random.randint(4000, 8000))

        self.shoot_upgrade_price = 500
        self.shoot_upgrade_button = Button(
            x=200, y=250, width=400, height=50,
            text=f"SHOOTING SPEED - {self.shoot_upgrade_price} PTS",
            color=(40,40,40),
            callback=self.buy_shooting_upgrade
            )
    
    def buy_shooting_upgrade(self):
        if self.game.spaceship_group.sprite:
            SpaceShip = self.game.spaceship_group.sprite

            # Check if alrdy maxed
            if SpaceShip.laser_delay == 100:
                return

            # Check if enough score
            if self.game.score >= self.shoot_upgrade_price:
                # Deduct
                self.game.score -= self.shoot_upgrade_price

                SpaceShip.laser_delay -=25

                self.shoot_upgrade_price += 500

                if SpaceShip.laser_delay <= 100:
                    self.shoot_upgrade_button.text = "MAX SPEED REACHED"
                else:
                    self.shoot_upgrade_button.text = f"SHOOTING SPEED - {self.shoot_upgrade_price} PTS" 
            
    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.SHOOT_LASER and self.game.run and not self.shop_triggered:
                self.game.alien_shoot_lasers()

            if event.type == self.MYSTER_SHIP and self.game.run and not self.shop_triggered:
                self.game.create_mystery_ship()
                pygame.time.set_timer(self.MYSTER_SHIP, random.randint(4000, 8000))
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.shop_triggered = not self.shop_triggered 

            self.shoot_upgrade_button.event_handle(event)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r] and self.game.run == False:
                self.game.reset()

            # Handling shop events
            if self.shop_triggered:
                self.shop_event_handle(event)

    def shop_event_handle(self, event):
        pass

    def update(self):
        if not self.shop_triggered and self.game.run == True:
            # All game logic
            self.game.spaceship_group.update()
            self.game.move_aliens()
            self.game.alien_lasers_group.update()
            self.game.mystery_ship_group.update()
            self.game.check_for_colisions()

        else:
            # Background game logic + shop animations
            pass
        
    def draw(self):
        #Drawing 
        self.screen.fill(self.GREY)

        # UI
        pygame.draw.rect(self.screen, self.YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60) 
        pygame.draw.line(self.screen, self.YELLOW, (25, 730), (775, 730), 3)

        if self.game.run:
            self.screen.blit(self.level_surface, (570, 740, 50, 50))
        else:
            self.screen.blit(self.game_over_surface, (570, 740, 50, 50))
        
        x = 50
        for life in range(self.game.lives):
            self.screen.blit(self.game.spaceship_group.sprite.image, (x, 745))
            x += 50

        self.screen.blit(self.score_text_surface, (40, 25, 50, 25))
        self.formatted_score = str(self.game.score).zfill(5)
        self.score_surface = self.font.render(str(self.formatted_score), False, self.YELLOW)
        self.screen.blit(self.score_surface, (40, 50, 50, 50))
        self.screen.blit(self.highscore_text_surface, (550, 15, 50, 15))
        self.formatted_highscore = str(self.game.highscore).zfill(5)
        self.highscore_surface = self.font.render(self.formatted_highscore, False, self.YELLOW)
        self.screen.blit(self.highscore_surface, (625, 40, 50, 50))

        self.game.spaceship_group.draw(self.screen) 
        self.game.spaceship_group.sprite.lasers_group.draw(self.screen)
        for obstacle in self.game.obstacles:
            obstacle.block_group.draw(self.screen)
        self.game.aliens_group.draw(self.screen)
        self.game.alien_lasers_group.draw(self.screen)
        self.game.mystery_ship_group.draw(self.screen)
        if self.shop_triggered:
            self.draw_shop()

        pygame.display.flip()

    def draw_shop(self):
        overlay = pygame.Surface((self.SCREEN_WIDTH + self.OFFSET, self.SCREEN_HEIGHT + 2 * self.OFFSET), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay, (0,0))

        # Container window
        shop_rect = pygame.Rect(150,150,500, 400)
        pygame.draw.rect(self.screen, (40,40,40), shop_rect, 3)
        pygame.draw.rect(self.screen, self.YELLOW, shop_rect, 3)

        # Title overlay
        shop_title = self.font.render("SHOP", False, self.YELLOW)
        self.screen.blit(shop_title, (170, 170))

        self.shoot_upgrade_button.draw(self.screen)

    def run(self):  
        # Game loop 
        while True:
            self.event_handle()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = initalizer()
    game.run()