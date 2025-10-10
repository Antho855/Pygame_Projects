import pygame
from random import choice

class Ball:
    def __init__(self, x, y):
        self.radius = 15
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, "Dark red", (self.radius, self.radius), self.radius)

        # Initial position
        self.rect = self.surface.get_rect(center=(x, y))

        # Base speed
        self.base_speed_x = 5
        self.base_speed_y = 3

        # Initial speed
        self.speed_x = 4 * choice([-1, 1])
        self.speed_y = 3 * choice([-1, 1])

    def update(self, surface):
        # Ball movement
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce on top and bottom
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = -self.speed_y
        elif self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.speed_y = -self.speed_y

        # Draw the ball
        surface.blit(self.surface, self.rect)
    
    def increase_speed(self, factor=1.1):
        # Increase ball speed by a factor
        self.speed_x *= factor
        self.speed_y *= factor

    def reset(self, x, y):
        # Reset ball position and speed
        self.rect.center = (x, y)
        self.radius = 15
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, "Dark red", (self.radius, self.radius), self.radius)
        self.rect = self.surface.get_rect(center=self.rect.center)
        self.speed_x = self.base_speed_x
        self.speed_y = self.base_speed_y
        self.speed_x *= -1 
        self.speed_y *= choice([-1, 1])
    
    def bonus_size(self, effect):
        # Base size
        normal_radius = 15  

        if effect == "BIG BALL":
            new_radius = 25
        elif effect == "SMALL BALL":
            new_radius = 8

        # Apply the bonus
        self.radius = new_radius
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, "Dark Red", (self.radius, self.radius), self.radius)
        self.rect = self.surface.get_rect(center=self.rect.center)

        # Save bonus state
        self.bonus_active = True
        self.bonus_start_time = pygame.time.get_ticks()
        self.bonus_duration = 5000  # 5 seconds
        self.normal_radius = normal_radius
