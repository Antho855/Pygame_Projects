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
            self.tail_collision()

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
    
    def tail_collision(self):
        if self.snake.body[-1] in self.snake.body[:-1]:
            self.game_over()
        
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0

    def reset_game(self):
        self.snake.reset()
        self.food.position = self.food.generate_pos(self.snake.body)
        self.score = 0
        self.state = "RUNNING"
        pygame.time.set_timer(SNAKE_UPDATE, 200)


    # Relancer le timer s'il a été stoppé
    pygame.time.set_timer(SNAKE_UPDATE, 150)

    def intro_message(self):
        title_font = pygame.font.Font(None, 80)
        instruction_font = pygame.font.Font(None, 30)
        screen.fill(GREEN)
        title_text = title_font.render("RETRO SNAKE", False, DARK_GREEN)
        instruction_text = instruction_font.render("Press SPACE to start", False, DARK_GREEN)
        screen.blit(title_text, (2*OFFSET,NB_CELL//2 *CELL_SIZE))
        screen.blit(instruction_text, (2*OFFSET, OFFSET + NB_CELL//2 *CELL_SIZE))
        pygame.display.update()

    def run(self):
        title_font = pygame.font.Font(None, 60)
        score_font = pygame.font.Font(None, 40)
        game_active = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == SNAKE_UPDATE:
                    self.update()
                if event.type == pygame.KEYDOWN:
                    self.state = "RUNNING"

            keys = pygame.key.get_pressed()
            # Start the game with SPACE from intro screen
            if keys[pygame.K_SPACE] and not game_active:
                game_active = True

            if game_active:
                self.snake.key_input()
                screen.fill(GREEN)

                # Bordure
                pygame.draw.rect(screen, DARK_GREEN, (OFFSET-5, OFFSET-5, CELL_SIZE*NB_CELL+10, CELL_SIZE*NB_CELL+10), 5)

                # Titres
                title_surf = title_font.render("Retro Snake", True, DARK_GREEN)
                screen.blit(title_surf, (OFFSET - 5, 20))
                score_surf = score_font.render(f"Score : {self.score}", True, DARK_GREEN)
                screen.blit(score_surf, (OFFSET - 5, OFFSET + CELL_SIZE * NB_CELL + 10))

                self.draw()

                pygame.display.update()
                clock.tick(60)
            
            else:
                self.intro_message()
            pygame.display.update()

    