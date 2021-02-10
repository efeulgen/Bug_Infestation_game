import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))


class GameText:
    score_value = 0
    score_font = pygame.font.Font("fonts/LazenbyCompSmooth.ttf", 32)
    score_text_x = 10
    score_text_y = 10

    def show_score(self):
        score_text = self.score_font.render('Score: ' + str(self.score_value), True, (255, 255, 255))
        screen.blit(score_text, (self.score_text_x, self.score_text_y))

    def gameover(self):
        game_over_img = pygame.image.load("assets/game_over.png")
        game_over_rect = game_over_img.get_rect(center=(640, 360))
        screen.blit(game_over_img, game_over_rect)
        final_score_font = pygame.font.Font("fonts/LazenbyCompSmooth.ttf", 40)
        final_score_text = final_score_font.render(f"You have killed {self.score_value} bugs.", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(640, 550))
        screen.blit(final_score_text, final_score_rect)

    def playagain(self):
        playagain_font = pygame.font.Font("fonts/LazenbyCompSmooth.ttf", 40)
        playagain_text = playagain_font.render("Play Again? : (P)LAY/ (Q)UIT", True, (255, 255, 255) )
        playagain_rect = playagain_text.get_rect(center=(640, 650))
        screen.blit(playagain_text, playagain_rect)
