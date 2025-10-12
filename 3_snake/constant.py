import pygame

CELL_SIZE = 30
NB_CELL = 25
GREEN = (173,202,96)
DARK_GREEN = (43, 51, 24)

OFFSET = 75


screen = pygame.display.set_mode((2*OFFSET + NB_CELL*CELL_SIZE, 2*OFFSET + NB_CELL*CELL_SIZE))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)