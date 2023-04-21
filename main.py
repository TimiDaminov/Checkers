import sys
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax
pygame.init()
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def start_screen():
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("Who will start?", 1, (255, 255, 255))
    rect = text.get_rect()
    rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
    WIN.blit(text, rect)

    # Player button
    player_button = pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(WIN, (0, 255, 0), player_button)
    player_text = font.render("Player", 2, (255, 255, 255))
    WIN.blit(player_text, (player_button.x, player_button.y - 20))

    # CPU button
    cpu_button = pygame.Rect(3 * WIDTH // 4 - 50, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(WIN, (255, 0, 0), cpu_button)
    cpu_text = font.render("CPU", 2, (255, 255, 255))
    WIN.blit(cpu_text, (cpu_button.x, cpu_button.y - 20))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if player_button.collidepoint(mouse_pos):
                    return RED
                elif cpu_button.collidepoint(mouse_pos):
                    return WHITE


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    starting_player = start_screen()
    game.turn = starting_player
    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(
                game.get_board(), 4, starting_player, game)
            game.cpu_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()


main()
