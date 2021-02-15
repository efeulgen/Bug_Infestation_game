import pygame
import random
from pygame import mixer
from game_texts import GameText
import start_menu

pygame.init()
clock = pygame.time.Clock()

# screen
screen_size = 1280, 720
width, height = screen_size
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Space Bug Infestation by @fff")
bg_img = pygame.image.load("assets/deep_space_bg_1280x720.png")

# background music
mixer.music.load("sounds&musics/game_loop_1.mp3")
mixer.music.play(-1)

# player
player_img = pygame.image.load("assets/Astro-K-47.png")
player_rect = player_img.get_rect(center=(50, 280))
player_x_speed = 0
player_y_speed = 0

# enemy
enemy_img = pygame.image.load("assets/space_bug.png")
enemy_rects = []

enemy_speeds = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_rects.append(enemy_img.get_rect(center=(random.randint(400, 735), random.randint(50, 150))))
    enemy_speeds.append([random.choice([4, 3, -3, -4]), random.choice([4, 3, -3, -4])])

# bullet
bullet_img = pygame.image.load('assets/bullet_has.png')
bullet_rects = []
bullet_speed = 12

# blood splash
splash_img = pygame.image.load("assets/splash-2.png")
splash_rect = splash_img.get_rect(center=(0, 0))

game_text = GameText()

start_menu.play_start()

running = True
hit = False
hit_cool_down = 0
game_over = False
game_over_sound_played = False
enemies_added = False
play_again = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play_again = True

            if event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_DOWN:
                player_y_speed = 7

            if event.key == pygame.K_UP:
                player_y_speed = -7

            if event.key == pygame.K_RIGHT:
                player_x_speed = 7

            if event.key == pygame.K_LEFT:
                player_x_speed = -7

            if event.key == pygame.K_SPACE:
                if len(bullet_rects) <= 3:
                    bullet_rects.append(bullet_img.get_rect(center=(player_rect.centerx + 70, player_rect.centery + 10)))

            if event.key == pygame.K_q and game_over is True:
                running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_y_speed = 0
                player_x_speed = 0

    if game_over is False:
        # screen and score
        screen.blit(bg_img, (0, 0))
        game_text.show_score()

        # player blit/ movement/ bound checking
        player_rect.x += player_x_speed
        player_rect.y += player_y_speed
        screen.blit(player_img, player_rect)

        if player_rect.top <= 0:
            player_rect.top = 0
        if player_rect.bottom >= 720:
            player_rect.bottom = 720
        if player_rect.right >= 250:
            player_rect.right = 250
        if player_rect.left <= 0:
            player_rect.left = 0

        # enemy movement&bound checking
        for i in range(num_of_enemies):
            if not 0 <= enemy_rects[i].x <= 1216:
                enemy_speeds[i][0] *= -1

            if not 0 <= enemy_rects[i].y <= 656:
                enemy_speeds[i][1] *= -1

            enemy_rects[i].x += enemy_speeds[i][0]
            enemy_rects[i].y += enemy_speeds[i][1]
            screen.blit(enemy_img, enemy_rects[i])

        # shooting/ bullet bound checking/ collision
        for bullet_rect in bullet_rects:
            screen.blit(bullet_img, bullet_rect)
            bullet_rect.x += bullet_speed
            if bullet_rect.x >= 1290:
                bullet_rects.remove(bullet_rect)
            for index, bug_rect in enumerate(enemy_rects):
                if bullet_rect.colliderect(bug_rect):
                    game_text.score_value += 1
                    enemy_rects.remove(bug_rect)
                    enemy_speeds.remove(enemy_speeds[index])
                    num_of_enemies -= 1
                    bullet_rects.remove(bullet_rect)

                    # sounds
                    smash_sound = mixer.Sound("sounds&musics/smash.wav")
                    smash_sound.play()

                    scream_sound = mixer.Sound("sounds&musics/scream.wav")
                    scream_sound.play()

                    # regenerate
                    enemy_rects.append(enemy_img.get_rect(center=(random.randint(400, 735), random.randint(50, 150))))
                    enemy_speeds.append([random.choice([4, 3, -3, -4]), random.choice([4, 3, -3, -4])])
                    num_of_enemies += 1

                    # splash coors
                    hit = True
                    hit_cool_down = 0
                    splash_rect = splash_img.get_rect(center=(bug_rect.centerx, bug_rect.centery))

        # splash
        if hit_cool_down <= 20 and hit:
            screen.blit(splash_img, splash_rect)
            hit_cool_down += 1
        else:
            hit_cool_down = 0
            hit = False

        # difficulty up
        if game_text.score_value >= 10 and enemies_added is not True:
            num_of_enemies = 9
            for i in range(3):
                enemy_rects.append(enemy_img.get_rect(center=(random.randint(400, 735), random.randint(50, 150))))
                enemy_speeds.append([random.choice([4, 3, -3, -4]), random.choice([4, 3, -3, -4])])
            enemies_added = True

        # game over
        for bug in enemy_rects:
            if player_rect.colliderect(bug):
                game_over = True

    if play_again:
        for i in range(num_of_enemies):
            enemy_rects.append(enemy_img.get_rect(center=(random.randint(400, 735), random.randint(50, 150))))
            enemy_speeds.append([random.choice([4, 3, -3, -4]), random.choice([4, 3, -3, -4])])

        game_text.score_value = 0
        game_over = False
        play_again = False

    if game_over:
        game_text.gameover()
        game_text.playagain()

        enemy_rects.clear()
        enemy_speeds.clear()

        score_text = f"Score: {game_text.score_value}\n"
        score_index = 0

        with open("score_table.txt", "r") as file:
            file_content = file.readlines()
            for line in file_content:
                if int(game_text.score_value) == int(line[-3:-1]):
                    score_index = -1
                    break
                elif int(game_text.score_value) > int(line[-3:-1]):
                    score_index = file_content.index(line)
                    break
                else:
                    score_index = len(file_content)

        if not score_index == -1:
            file_content.insert(score_index, score_text)
        file_text = "".join(file_content)
        with open("score_table.txt", "w") as file:
            file.write(file_text)

        if game_over_sound_played is False:
            game_over_sound = mixer.Sound("sounds&musics/game_over_1.wav")
            game_over_sound.play()

        game_over_sound_played = True

    # clock and update
    pygame.display.update()
    clock.tick(120)

pygame.quit()
