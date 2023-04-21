
from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)


def minimax(position, depth, max_player, game):
    # Base case: if the maximum depth is reached or a winner is found
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position

    # If it's the max player's turn
    if max_player:
        # Set the max evaluation to negative infinity and the best move to None
        maxEval = float('-inf')
        best_move = None
        # Get all possible moves for the current player
        for move in get_all_moves(position, WHITE, game):
            # Recursively evaluate the move and set the evaluation to the max evaluation
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            # If the current evaluation is the maximum, set the best move to the current move
            if maxEval == evaluation:
                best_move = move

        # Return the maximum evaluation and the best move
        return maxEval, best_move
    else:
        # If it's the min player's turn
        # Set the min evaluation to positive infinity and the best move to None
        minEval = float('inf')
        best_move = None
        # Get all possible moves for the current player
        for move in get_all_moves(position, RED, game):
            # Recursively evaluate the move and set the evaluation to the min evaluation
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            # If the current evaluation is the minimum, set the best move to the current move
            if minEval == evaluation:
                best_move = move

        # Return the minimum evaluation and the best move
        return minEval, best_move


# Function to simulate a move on the board
def simulate_move(piece, move, board, game, skip):
    # Move the piece on the board
    board.move(piece, move[0], move[1])
    # If there is a skip move, remove the skipped piece
    if skip:
        board.remove(skip)

    # Return the updated board
    return board


# Function to get all possible moves for a player
def get_all_moves(board, color, game):
    moves = []

    # For each piece of the player's color
    for piece in board.get_all_pieces(color):
        # Get all valid moves for the piece
        valid_moves = board.get_valid_moves(piece)
        # For each valid move and the corresponding skipped piece
        for move, skip in valid_moves.items():
            # Draw the valid moves on the board
            draw_moves(game, board, piece)
            # Create a copy of the board and piece to simulate the move
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            # Simulate the move on the temporary board
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            # Add the updated board to the list of possible moves
            moves.append(new_board)

    # Return the list of possible moves
    return moves


# Function to draw the valid moves of a piece on the board
def draw_moves(game, board, piece):

    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(100)
