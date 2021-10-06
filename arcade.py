import pygame, random

from pygame.constants import HAT_RIGHT

pygame.init()

WINDOW_WIDTH = 928
WINDOW_HEIGHT = 793
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chirp")

FPS = 60
clock = pygame.time.Clock()

PLAYER_STARTING_LIVES = 3
PLAYER_STARTING_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_SEED_VELOCITY = 3
SEED_ACCELERATION = .25
BUFFER_DISTANCE = -50

score = 0
seed_points = 0
seeds_eaten = 0

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_STARTING_VELOCITY

boost_level = STARTING_BOOST_LEVEL

seed_velocity = STARTING_SEED_VELOCITY

ORANGE = (246, 170, 54)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

font = pygame.font.SysFont("Centaur", 32)

points_text = font.render("Points: " + str(seed_points), True, ORANGE)
points_rect = points_text.get_rect()
points_rect.topleft = (10, 10)

score_text = font.render("Score: " + str(score), True, ORANGE)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 50)

title_text = font.render("Chirp", True, ORANGE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

eaten_text = font.render("Seeds eaten: " + str(seeds_eaten), True, ORANGE)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = WINDOW_WIDTH//2
eaten_rect.y = 50

lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH-10, 10)

boost_text = font.render("Boost: " + str(boost_level), True, ORANGE)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOW_WIDTH-10, 50)

gameover_text = font.render("FINAL SCORE: " + str(score), True, RED)
gameover_rect = gameover_text.get_rect()
gameover_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play again", True, WHITE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)

hit = pygame.mixer.Sound("hit.wav")
miss = pygame.mixer.Sound("miss.wav")
pygame.mixer.music.load("ambience.wav")

player_image_right = pygame.image.load("birdright.png")
player_image_left = pygame.image.load("birdleft.png")
player_image = player_image_right
player_rect = player_image.get_rect()
player_rect.centerx = WINDOW_WIDTH//2
player_rect.bottom = WINDOW_HEIGHT

cherry_image = pygame.image.load("cherry.png")
cherry_rect = cherry_image.get_rect()
cherry_rect.topleft = (random.randint(0, WINDOW_WIDTH-48), BUFFER_DISTANCE)

background_image = pygame.image.load("Background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

running = True
pygame.mixer.music.play(-1, 0.0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_rect.left > 0:
        player_rect.x -= player_velocity
        player_image = player_image_left
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_rect.right < (WINDOW_WIDTH):
        player_rect.x += player_velocity
        player_image = player_image_right
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.top > 100:
        player_rect.y -= player_velocity
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += player_velocity
    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = PLAYER_BOOST_VELOCITY
        boost_level -= 1
    else:
        player_velocity = PLAYER_STARTING_VELOCITY
        if boost_level < 100:
            boost_level += .4

    cherry_rect.y += seed_velocity
    seed_points = int(seed_velocity*(WINDOW_HEIGHT - cherry_rect.y + 100))

    if cherry_rect.y > WINDOW_HEIGHT:
        miss.play()
        player_lives -= 1
        cherry_rect.topleft = (random.randint(0, WINDOW_WIDTH-48), BUFFER_DISTANCE)
        seed_velocity = STARTING_SEED_VELOCITY

    if player_rect.colliderect(cherry_rect):
        score += seed_points
        seeds_eaten += 1
        hit.play()
        cherry_rect.topleft = (random.randint(0, WINDOW_WIDTH-48), BUFFER_DISTANCE)
        seed_velocity += SEED_ACCELERATION
        boost_level += 10
        if boost_level > STARTING_BOOST_LEVEL:
            boost_level = STARTING_BOOST_LEVEL

    points_text = font.render("Points: " + str(seed_points), True, ORANGE)
    score_text = font.render("Score: " + str(score), True, ORANGE)
    eaten_text = font.render("Seeds eaten: " + str(seeds_eaten), True, ORANGE)
    lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
    boost_text = font.render("Boost: " + str(int(boost_level)), True, ORANGE)

    if player_lives == 0:
        gameover_text = font.render("FINAL SCORE: " + str(score), True, RED)
        display_surface.blit(gameover_text, gameover_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    score = 0
                    seeds_eaten = 0
                    player_lives = PLAYER_STARTING_LIVES
                    boost_level = STARTING_BOOST_LEVEL
                    seed_velocity = STARTING_SEED_VELOCITY
                    player_rect.centerx = WINDOW_WIDTH//2
                    player_rect.bottom = WINDOW_HEIGHT
                    pygame.mixer.music.play()
                    is_paused = False
    

    display_surface.blit(background_image, background_rect)

    display_surface.blit(points_text, points_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(eaten_text, eaten_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(boost_text, boost_rect)
    pygame.draw.line(display_surface, ORANGE, (0, 100), (WINDOW_WIDTH, 100), 3)

    display_surface.blit(player_image, player_rect)
    display_surface.blit(cherry_image, cherry_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()