import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []  # initialize the board as an empty list
        # initialize the number of pieces left for both colors
        self.red_left = self.white_left = 12
        # initialize the number of kings for both colors
        self.red_kings = self.white_kings = 0
        self.create_board()  # create the initial game board

    def draw_squares(self, win):
        win.fill(BLACK)  # fill the window with black color
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                # draw a white square at the position of (row*SQUARE_SIZE, col*SQUARE_SIZE) with a size of SQUARE_SIZE
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE,
                                 col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_left * 0.5 - self.red_kings * 0.5)

    def move(self, piece, row, col):
        # move the piece from its current position to the new position
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        # update the piece's position
        piece.move(row, col)

        # check if the piece has reached the opponent's side and should be crowned as king
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])  # append a new row to the board
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):  # determine the color of the square
                    if row < 3:  # add a white piece to the square if it's in the top rows
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:  # add a red piece to the square if it's in the bottom rows
                        self.board[row].append(Piece(row, col, RED))
                    else:  # otherwise, add an empty square
                        self.board[row].append(0)
                else:  # otherwise, add an empty square
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)  # draw the game board
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)  # draw the piece on the square

    def remove(self, pieces):
        for piece in pieces:
            # remove the piece from the board
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1  # decrement the number of red pieces left
                else:
                    self.white_left -= 1  # decrement the number of white pieces left

    def winner(self):
        if self.red_left <= 0:
            return WHITE  # if there are no red pieces left, white wins
        elif self.white_left <= 0:
            return RED  # if there are no white pieces

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(
                row - 1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(
                row - 1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(
                row + 1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(
                row + 1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(
                        r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(
                        r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(
                        r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(
                        r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
