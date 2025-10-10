import pygame
from sys import exit
from random import randint

# Initialize pygame
pygame.init()
pygame.display.set_caption('Square Catcher')

# Screen size
screen = pygame.display.set_mode((800, 400))

# Player setup
player = pygame.Surface((50, 50))                      # create a red square
player_rect = player.get_rect(midtop=(400, 200))       # start position
player_speed = 400                                     # pixels per second
player.fill('Red')
clock = pygame.time.Clock()

# Falling objects
falling_obj = []            # list of falling objects (pygame.Rect)
obj_speed = 150             # pixels per second
spawn_timer = 0             # timer for spawning objects
spawn_interval = 1000       # interval in ms (1s between spawns)

# Score and lives
score = 0
life = 3
text_font = pygame.font.Font(None, 25)

# Game states
game_active = False
game_over = False

# Text setup
text_intro = pygame.font.Font(None, 80)
text_intro_enter = pygame.font.Font(None, 25)
text_game_over = pygame.font.Font(None, 50)

# Temporary loss messages ("-2" when an object hits the ground)
# Each element = [Surface, [x, y], timer_in_frames]
loss_messages = []

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Restart when game over and press R
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset game variables
                score = 0
                life = 3
                falling_obj.clear()
                loss_messages.clear()
                player_rect.midtop = (400, 200)
                game_over = False
                game_active = True

    # Delta time (in seconds)
    dt = clock.tick(60) / 1000

    keys = pygame.key.get_pressed()

    # Player movement only if game is active
    if game_active:
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed * dt
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed * dt
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed * dt
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed * dt

    # Start the game with SPACE from intro screen
    if keys[pygame.K_SPACE] and not game_active and not game_over:
        game_active = True

    # Keep the player inside the screen
    if player_rect.bottom >= 400:
        player_rect.bottom = 400
    if player_rect.top <= 0:
        player_rect.top = 0
    if player_rect.right >= 800:
        player_rect.right = 800
    if player_rect.left <= 0:
        player_rect.left = 0
    
    if game_active:
        # Spawn new falling objects
        spawn_timer += dt * 1000
        if spawn_timer > spawn_interval:
            spawn_timer = 0
            new_obj = pygame.Rect(randint(0, 750), -50, 50, 50)
            falling_obj.append(new_obj)

        # Update objects
        new_falling = []
        for obj in falling_obj:
            obj.y += obj_speed * dt
            if player_rect.colliderect(obj):
                score += 5   # caught object → +5 points
            elif obj.top >= 400:
                life -= 1
                score -= 2
                # Create a temporary "-2" message
                loss_point_text = text_font.render("-2", True, 'Red')
                pos = [randint(100, 700), randint(50, 350)]  # random position
                loss_messages.append([loss_point_text, pos, 60])  # ~1 second visible
                if life <= 0:
                    game_active = False
                    game_over = True
            else:
                new_falling.append(obj)

        falling_obj = new_falling

        # --- Drawing ---
        screen.fill('White')

        # Player
        screen.blit(player, player_rect)

        # Falling objects
        for obj in falling_obj:
            pygame.draw.ellipse(screen, 'Green', obj)

        # Score and lives
        score_text = text_font.render(f"Score: {score}", False, 'Black')
        screen.blit(score_text, (10, 10))
        life_text = text_font.render(f"Lives: {life}", False, 'Black')
        screen.blit(life_text, (650, 10))

        # Temporary loss messages ("-2")
        for msg in loss_messages[:]:   # iterate over a copy
            surf, pos, timer = msg
            screen.blit(surf, pos)     # draw the message
            msg[2] -= 1                # decrease timer
            if msg[2] <= 0:
                loss_messages.remove(msg)  # remove expired messages

    elif game_over:
        # Game over screen
        screen.fill((50, 50, 50))
        game_over_text = text_game_over.render("GAME OVER", True, 'Red')
        screen.blit(game_over_text, (270, 120))
        score_text = text_font.render(f"Score: {score}", False, 'White')
        screen.blit(score_text, (350, 200))
        restart_text = text_intro_enter.render("Press R to restart", True, 'White')
        screen.blit(restart_text, (300, 300))

    else:
        # Intro screen
        screen.fill((94, 129, 162))
        intro_text_1 = text_intro.render("SQUARE CATCHER", False, 'Red')
        screen.blit(intro_text_1, (150, 100))
        intro_text_2 = text_intro_enter.render("Press SPACE to start", True, 'Red')
        screen.blit(intro_text_2, (300, 300))
        
    # Update display
    pygame.display.update()
