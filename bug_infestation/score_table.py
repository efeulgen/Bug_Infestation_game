import pygame
import sys

pygame.init()

screen_size = 1280, 720
width, height = screen_size
screen = pygame.display.set_mode(screen_size)
bg_img = pygame.image.load("assets/deep_space_bg_1280x720.png")
clock = pygame.time.Clock()

back_img = pygame.image.load("assets/back.png")
back_rect = back_img.get_rect(center=(width/2 - 100, height/2 + 300))

table_rect = pygame.Rect(width/2 - 150, height/2 - 250, 300, 500)

score_table_font = pygame.font.Font("fonts/LazenbyCompSmooth.ttf", 20)
score_table_text_list = []
score_table_rect_list = []
first_line_y_pos = height/2

with open("score_table.txt", "r") as score_table:
    for line in score_table:
        score_table_text_list.append(score_table_font.render(line.rstrip(), True, (255, 255, 255)))

x = 0
for i in score_table_text_list:
    score_table_rect_list.append(i.get_rect(center=(width/2, first_line_y_pos + x)))
    x += 50


def show_score_table():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    running = False

        screen.blit(bg_img, (0, 0))
        pygame.draw.rect(screen, (44, 91, 138), table_rect)
        for index in range(5):
            screen.blit(score_table_text_list[index], score_table_rect_list[index])

        screen.blit(back_img, back_rect)

        pygame.display.update()
        clock.tick(120)
