import pygame
from sys import exit
from snake import Snake
from food import Food
from constant import *

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        

    def draw(self):
        self.snake.draw()
        self.food.draw()
    
    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.food_collision()
            self.border_collision()

    def food_collision(self):
        if self.snake.body[-1] == self.food.position:
            self.food.position = self.food.generate_pos(self.snake.body)
            self.snake.grow = True
            self.score += 1
    
    def border_collision(self):
        if self.snake.body[-1][0] == NB_CELL or self.snake.body[-1][0] == -1:
            self.game_over()
        if self.snake.body[-1][1] == NB_CELL or self.snake.body[-1][1] == -1:
            self.game_over()
        
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0

    def run(self):
        title_font = pygame.font.Font(None, 60)
        score_font = pygame.font.Font(None, 40)
        while True:
            for event in pygame.event.get():
                if event.type == SNAKE_UPDATE:
                    self.update()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if self.state == "STOPPED":
                        self.state = "RUNNING"

            self.snake.key_input()
            screen.fill(GREEN)
            pygame.draw.rect(screen, DARK_GREEN,(OFFSET-5, OFFSET-5, CELL_SIZE*NB_CELL+10, CELL_SIZE*NB_CELL+10),5) # Border
            title_surf = title_font.render("Retro Snake", True, DARK_GREEN)
            screen.blit(title_surf, (OFFSET - 5,20))
            score_surf = title_font.render(f"Score : {self.score}", True, DARK_GREEN)
            screen.blit(score_surf, (OFFSET - 5, OFFSET + CELL_SIZE * NB_CELL + 10))
            self.draw()

            pygame.display.update()
            clock.tick(60)

    