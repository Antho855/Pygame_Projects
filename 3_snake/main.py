import pygame
from sys import exit
from random import randint

pygame.init()

CELL_SIZE = 30
NB_CELL = 25
GREEN = (173,202,96)
DARK_GREEN = (43, 51, 24)

OFFSET = 75


title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)


screen = pygame.display.set_mode((2*OFFSET + NB_CELL*CELL_SIZE, 2*OFFSET + NB_CELL*CELL_SIZE))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

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
        if keys[pygame.K_DOWN] and self.direction != (0,-1):
            self.direction = (0,1)
        if keys[pygame.K_UP] and self.direction != (0,1):
            self.direction = (0,-1)
        if keys[pygame.K_LEFT] and self.direction != (1,0):
            self.direction = (-1,0)
        if keys[pygame.K_RIGHT] and self.direction != (-1,0):
            self.direction = (1,0)
    
    def reset(self):
        self.body = [(4,12), (5,12), (6,12)]
        self.direction = (1,0)
    
    

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
    

game = Game()

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"

    game.snake.key_input()
    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GREEN,(OFFSET-5, OFFSET-5, CELL_SIZE*NB_CELL-10, CELL_SIZE*NB_CELL-10),5)
    title_surf = title_font.render("Retro Snake", True, DARK_GREEN)
    screen.blit(title_surf, (OFFSET - 5,20))
    score_surf = title_font.render(str(game.score), True, DARK_GREEN)
    screen.blit(score_surf, (OFFSET - 5, OFFSET + CELL_SIZE * NB_CELL + 10))
    game.draw()

    pygame.display.update()
    clock.tick(60)