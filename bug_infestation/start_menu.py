import pygame
import sys
import score_table

pygame.init()

screen_size = 1280, 720
width, height = screen_size
screen = pygame.display.set_mode(screen_size)
bg_img = pygame.image.load("assets/deep_space_bg_1280x720.png")
clock = pygame.time.Clock()

opening_img = pygame.image.load("assets/opening.png")
opening_rect = opening_img.get_rect(center=(width/2, height/2))

play_img = pygame.image.load("assets/play.png")
play_rect = play_img.get_rect(center=(width/2 - 200, height/2 + 250))

high_scores_img = pygame.image.load("assets/high_scores.png")
high_scores_rect = high_scores_img.get_rect(center=(width/2 + 200, height/2 + 250))


def play_start():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    running = False

                if high_scores_rect.collidepoint(event.pos):
                    score_table.show_score_table()

        screen.blit(bg_img, (0, 0))
        screen.blit(opening_img, opening_rect)
        screen.blit(play_img, play_rect)
        screen.blit(high_scores_img, high_scores_rect)

        pygame.display.update()
        clock.tick(120)
