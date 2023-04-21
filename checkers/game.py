import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        # Draw the board and valid moves on the window
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        # Update the window
        pygame.display.update()

    def _init(self):
        # Initialize variables
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        # Get the winner of the game
        return self.board.winner()

    def reset(self):
        # Reset the game
        self._init()

    def select(self, row, col):
        if self.selected:
            # If a piece is already selected, try to move it to the new location
            result = self._move(row, col)
            if not result:
                # If the move was invalid, deselect the piece and select the new one
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            # If the piece is of the current player's color, select it and get its valid moves
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # If a piece is selected and the move is valid, move the piece
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                # If a piece was skipped during the move, remove it from the board
                self.board.remove(skipped)
            # Change the turn to the other player
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        # Draw circles on the valid move positions
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, RED, (col * SQUARE_SIZE +
                               SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        # Reset the valid moves and change the turn to the other player
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def cpu_move(self, board):
        self.board = board
        self.change_turn()
