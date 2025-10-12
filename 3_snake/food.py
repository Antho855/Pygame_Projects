import pygame
from constant import *
from random import randint

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_pos(snake_body)
    
    def draw(self):
        food_rect = pygame.Rect(OFFSET + CELL_SIZE*self.position[0], OFFSET + CELL_SIZE*self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, DARK_GREEN, food_rect)

    def generate_pos(self, snake_body):
        pos = (randint(0, NB_CELL-1), randint(0, NB_CELL-1))
        while pos in snake_body:
            pos = self.generate_pos()
        return pos