import pygame
from constant import *

class Snake:
    def __init__(self):
        self.body = [(4,12), (5,12), (6,12)]
        self.direction = (1,0)
        self.grow = False
    
    def draw(self):
        for body_part in self.body:
            body_part_rect = pygame.Rect(OFFSET + CELL_SIZE*body_part[0], OFFSET + CELL_SIZE*body_part[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, DARK_GREEN, body_part_rect, 0, 7)
    
    def update(self):
        self.body.append((self.body[-1][0] + self.direction[0], self.body[-1][1] + self.direction[1]))
        if self.grow:
            self.grow = False
        else:
            self.body = self.body[1:]
            
    
    def key_input(self):
        keys = pygame.key.get_pressed()
        move_song = pygame.mixer.Sound("3_snake/sounds/music_move.mp3")
        move_song.set_volume(0.5)
        if keys[pygame.K_DOWN] and self.direction != (0,-1):
            self.direction = (0,1)
            move_song.play()
        if keys[pygame.K_UP] and self.direction != (0,1):
            self.direction = (0,-1)
            move_song.play()
        if keys[pygame.K_LEFT] and self.direction != (1,0):
            self.direction = (-1,0)
            move_song.play()
        if keys[pygame.K_RIGHT] and self.direction != (-1,0):
            self.direction = (1,0)
            move_song.play()
        
        
    
    def reset(self):
        self.body = [(4,12), (5,12), (6,12)]
        self.direction = (1,0)