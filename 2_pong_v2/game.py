import pygame
from ball import Ball
from sys import exit
from player import Player
from random import choice

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1000, 500

        # Screen setup & clock
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('THE PONG')
        self.clock = pygame.time.Clock()

        # Players setup
        self.player_1 = Player(pygame.K_UP, pygame.K_DOWN, 950, self.height // 2)
        self.player_2 = Player(pygame.K_z, pygame.K_s, 50, self.height // 2)

        # Ball setup
        self.ball = Ball(self.width // 2, self.height // 2)
        
        # Active bonuses
        self.active_bonus = []

    def reset(self, full_reset=True):

        # Reset players
        self.player_1.reset(y=self.height // 2, life_reset=full_reset)
        self.player_2.reset(y=self.height // 2, life_reset=full_reset)

        # Reset ball
        self.ball.reset(self.width // 2, self.height // 2)

        # Return game state
        return {
            "game_active": True,
            "game_over": False,
            "restart": True
        }
    
    def intro_message(self):
        title_font = pygame.font.Font(None, 80)
        instruction_font = pygame.font.Font(None, 30)
        self.screen.fill('Black')
        title_text = title_font.render("THE PONG", False, 'White')
        instruction_text = instruction_font.render("Press SPACE to start", False, 'White')
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, self.height // 3))
        self.screen.blit(instruction_text, (self.width // 2 - instruction_text.get_width() // 2, self.height // 2))
        pygame.display.update()
    
    def game_over_message(self):
        title_font = pygame.font.Font(None, 80)
        instruction_font = pygame.font.Font(None, 30)
        self.screen.fill('Black')
        if self.player_1.lives == 0:
            winner_text = title_font.render("Player 2 Wins!", False, 'White')
        else:
            winner_text = title_font.render("Player 1 Wins!", False, 'White')

        restart_text = instruction_font.render("Press R to Restart or Q to Quit", False, 'White')
        self.screen.blit(winner_text, (self.width // 2 - winner_text.get_width() // 2, self.height // 3))
        self.screen.blit(restart_text, (self.width // 2 - restart_text.get_width() // 2, self.height // 2))
        pygame.display.update()
    
    
    def run(self):
        running = True
        game_active = False
        game_over = False
        restart = False
        message_timer = ["3", "2", "1", "GO!"]
        bonus = {
            "BIG BALL": (pygame.Surface((50, 50)), "Red"),
            "SMALL BALL": (pygame.Surface((30, 30)), "Dark Orange"),
            "SPEED UP": (pygame.Surface((20, 20)), "Yellow"),
            "SLOW DOWN": (pygame.Surface((40, 40)), "Blue"),
            "LIFE +1": (pygame.Surface((10, 10)), "Purple"),
            "BIG PADDLE": (pygame.Surface((40, 40)), "White"),
            "SMALL PADDLE": (pygame.Surface((20,20)), "Pink")}

        # Fonts
        title_font = pygame.font.Font(None, 80)

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # --- Start screen ---
            if not game_active and not game_over:
                self.intro_message()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    states = self.reset(full_reset=True)
                    game_active, game_over, restart = states.values()

            # --- Main game loop ---
            elif game_active and not game_over:
                if restart:
                    for i in range(4):
                        self.screen.fill('Black')
                        countdown_text = title_font.render(message_timer[i], False, 'White')
                        self.screen.blit(countdown_text, (self.width // 2 - countdown_text.get_width() // 2, self.height // 2 - countdown_text.get_height() // 2))
                        pygame.display.update()
                        pygame.time.delay(1000)
                    restart = False

                self.screen.fill('Black')

                # Update + draw players
                self.player_1.update(self.screen)
                self.player_2.update(self.screen)

                # Update + draw ball
                self.ball.update(self.screen)

                # Display lives
                self.player_1.display_lives(self.screen, (self.width - 250, 20))
                self.player_2.display_lives(self.screen, (50, 20))

                # Collisions avec les raquettes
                if self.ball.rect.colliderect(self.player_1.rect):
                    if self.ball.speed_x > 0 and self.ball.rect.right >= self.player_1.rect.left:
                        self.ball.rect.right = self.player_1.rect.left
                        self.ball.speed_x *= -1
                        self.ball.increase_speed(1.05)

                if self.ball.rect.colliderect(self.player_2.rect):
                    if self.ball.speed_x < 0 and self.ball.rect.left <= self.player_2.rect.right:
                        self.ball.rect.left = self.player_2.rect.right
                        self.ball.speed_x *= -1
                        self.ball.increase_speed(1.05)

                # Handle scoring
                if self.ball.rect.left <= 0:
                    self.player_2.lives -= 1
                    states = self.reset(full_reset=False)
                    restart = states["restart"]

                elif self.ball.rect.right >= self.width:
                    self.player_1.lives -= 1
                    states = self.reset(full_reset=False)
                    restart = states["restart"]

                # Handle bonus spawn
                if choice(range(0, 300)) == 1:
                    effect = choice(list(bonus.keys()))
                    bonus_surf, color = bonus[effect]
                    bonus_surf.fill(color)
                    bonus_rect = bonus_surf.get_rect(center=(choice(range(100, self.width - 100)), choice(range(50, self.height - 50))))
                    # Bonus attributes
                    self.active_bonus.append({
                        "effect": effect,
                        "surf": bonus_surf,
                        "rect": bonus_rect,
                        "spawn_time": pygame.time.get_ticks(),
                        "duration": 7000  # Duration (ms)
                    })


                current_time = pygame.time.get_ticks()
                for bonus_item in self.active_bonus[:]:  # Iterate over a copy of the list
                    if current_time - bonus_item["spawn_time"] <= bonus_item["duration"]:
                        # Draw bonus
                        self.screen.blit(bonus_item["surf"], bonus_item["rect"])

                        # Collision ball + bonus
                        if self.ball.rect.colliderect(bonus_item["rect"]):
                            effect = bonus_item["effect"]
                            if effect in ["BIG BALL", "SMALL BALL"]:
                                self.ball.bonus_size(effect)
                            elif effect == "SPEED UP":
                                self.ball.increase_speed(1.2)
                            elif effect == "SLOW DOWN":
                                self.ball.increase_speed(0.8)
                            elif effect == "LIFE +1":
                                if self.ball.speed_x > 0:
                                    self.player_1.bonus_life()
                                else:
                                    self.player_2.bonus_life()
                            elif effect == "BIG PADDLE":
                                if self.ball.speed_x < 0:
                                    self.player_1.bonus_size(effect)
                                else:
                                    self.player_2.bonus_size(effect)
                            elif effect == "SMALL PADDLE":
                                if self.ball.speed_x > 0:
                                    self.player_1.bonus_size(effect)
                                else:
                                    self.player_2.bonus_size(effect)

                            # Delete bonus after collection
                            self.active_bonus.remove(bonus_item)
                    else:
                        # Bonus  Apparition Expired
                        self.active_bonus.remove(bonus_item)

                if getattr(self.ball, "bonus_active", False):
                    if pygame.time.get_ticks() - self.ball.bonus_start_time > self.ball.bonus_duration:
                        # Reset ball size
                        self.ball.radius = self.ball.normal_radius
                        self.ball.surface = pygame.Surface((self.ball.radius * 2, self.ball.radius * 2), pygame.SRCALPHA)
                        pygame.draw.circle(self.ball.surface, "Dark Red", (self.ball.radius, self.ball.radius), self.ball.radius)
                        self.ball.rect = self.ball.surface.get_rect(center=self.ball.rect.center)
                        self.ball.bonus_active = False

                for player in [self.player_1, self.player_2]:
                    if getattr(player, "bonus_active", False):
                        if pygame.time.get_ticks() - player.bonus_start_time > player.bonus_duration:
                            # Reset player size
                            player.width_rect = player.normal_height
                            player.surface = pygame.Surface((20, player.width_rect))
                            player.surface.fill("White")
                            player.rect = player.surface.get_rect(center=player.rect.center)
                            player.bonus_active = False

                # End game condition
                if self.player_1.lives <= 0 or self.player_2.lives <= 0:
                    game_active = False
                    game_over = True

                pygame.display.update()
                self.clock.tick(60)

            # --- Game over screen ---
            elif game_over:
                self.game_over_message()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    states = self.reset(full_reset=True)
                    game_active, game_over, restart = states.values()
                elif keys[pygame.K_q]:
                    running = False

        pygame.quit()
        exit()

