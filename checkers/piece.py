from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame


class Piece:
    PADDING = 15  # Padding around the piece inside the square
    OUTLINE = 2  # Thickness of the outline of the piece

    def __init__(self, row, col, color):
        self.row = row  # Row index of the piece
        self.col = col  # Column index of the piece
        self.color = color  # Color of the piece
        self.king = False  # Whether the piece is a king or not
        self.x = 0  # x-coordinate of the center of the piece
        self.y = 0  # y-coordinate of the center of the piece
        self.calc_pos()  # Calculate the position of the piece on the board

    def calc_pos(self):
        # Calculate the position of the center of the piece on the board
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True  # Set the piece to be a king

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING  # Calculate the radius of the piece
        # Draw the outline of the piece
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        # Draw the piece
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            # If the piece is a king, draw a crown on top of it
            win.blit(CROWN, (self.x - CROWN.get_width() //
                     2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row  # Update the row index of the piece
        self.col = col  # Update the column index of the piece
        self.calc_pos()  # Recalculate the position of the piece on the board

    def __repr__(self):
        # Return the color of the piece as a string representation
        return str(self.color)
