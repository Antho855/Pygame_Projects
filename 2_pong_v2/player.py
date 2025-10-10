import pygame

class Player:
    def __init__(self, up, down, x, y=250):
        self.width_rect = 100  # hauteur de la raquette
        self.surface = pygame.Surface((20, self.width_rect))  # largeur, hauteur
        self.surface.fill("White")

        # Initial position
        self.rect = self.surface.get_rect(center=(x, y))

        # Controles
        self.keys = [up, down]
        self.speed = 6

        # Lives
        self.lives = 3

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < 500:  # Screen height
            self.rect.y += self.speed

    def key_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[self.keys[0]]:
            self.move_up()
        if pressed[self.keys[1]]:
            self.move_down()

    def update(self, surface):
        # Handle input
        self.key_input()
        # Draw the player
        surface.blit(self.surface, self.rect)
    
    def reset(self, life_reset, y=250):
        self.rect.centery = y
        if life_reset:
            self.lives = 3
        self.width_rect = 100
        self.surface = pygame.Surface((20, self.width_rect))
        self.surface.fill("White")
        self.rect = self.surface.get_rect(center=self.rect.center)
    
    def display_lives(self, surface, position):
        font = pygame.font.Font(None, 36)
        life_text = font.render(f"Lives: {self.lives}", True, 'White')
        surface.blit(life_text, position)
    
    def bonus_size(self, effect):
        # Base size
        normal_height = 100  

        if effect == "BIG PADDLE":
            new_height = 150
        elif effect == "SMALL PADDLE":
            new_height = 70

        # Apply the bonus
        self.surface = pygame.Surface((20, new_height))
        self.surface.fill("White")
        self.rect = self.surface.get_rect(center=self.rect.center)

        # Save bonus state
        self.bonus_active = True
        self.bonus_start_time = pygame.time.get_ticks()
        self.bonus_duration = 5000  # 5 secondes
        self.normal_height = normal_height

    
    def bonus_life(self):
        self.lives += 1
        pygame.display.update()
