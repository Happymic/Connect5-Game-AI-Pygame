import numpy as np
import random
import math
import pygame

# Set the chess board size here!
ROW_COUNT = 11
COLUMN_COUNT = 11

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_SIZE = 600
SQUARE_SIZE = WINDOW_SIZE // COLUMN_COUNT
RADIUS = SQUARE_SIZE // 2 - 5

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, (0, 0, 255), (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, (0, 0, 0), (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, (255, 0, 0), (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, (255, 255, 0), (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
    pygame.display.update()
def is_winner(board, piece):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 4):
            if all(board[r][c + i] == piece for i in range(5)):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 4):
            if all(board[r + i][c] == piece for i in range(5)):
                return True

    for r in range(ROW_COUNT - 4):
        for c in range(COLUMN_COUNT - 4):
            if all(board[r + i][c + i] == piece for i in range(5)):
                return True

    for r in range(4, ROW_COUNT):
        for c in range(COLUMN_COUNT - 4):
            if all(board[r - i][c + i] == piece for i in range(5)):
                return True

    return False


def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 5:
        score += 100
    elif window.count(piece) == 4 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 3 and window.count(EMPTY) == 2:
        score += 5

    if window.count(opponent_piece) == 4 and window.count(EMPTY) == 1:
        score -= 90

    return score


def score_position(board, piece):
    score = 0


    for r in range(ROW_COUNT):
        row_array = list(board[r, :])
        for c in range(COLUMN_COUNT - 4):
            window = row_array[c:c + 5]
            score += evaluate_window(window, piece)


    for c in range(COLUMN_COUNT):
        col_array = list(board[:, c])
        for r in range(ROW_COUNT - 4):
            window = col_array[r:r + 5]
            score += evaluate_window(window, piece)


    for r in range(ROW_COUNT - 4):
        for c in range(COLUMN_COUNT - 4):
            window = [board[r + i][c + i] for i in range(5)]
            score += evaluate_window(window, piece)


    for r in range(4, ROW_COUNT):
        for c in range(COLUMN_COUNT - 4):
            window = [board[r - i][c + i] for i in range(5)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return is_winner(board, PLAYER_PIECE) or is_winner(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if is_winner(board, AI_PIECE):
                return None, 100000000000
            elif is_winner(board, PLAYER_PIECE):
                return None, -100000000000
            else:
                return None, 0
        else:
            return None, score_position(board, AI_PIECE)

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


pygame.init()


screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

pygame.display.set_caption("Connect5V1")


board = create_board()


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, (0, 0, 255), (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, (0, 0, 0), (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, (255, 0, 0), (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, (255, 255, 0), (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
    pygame.display.update()


running = True
player_turn = random.choice([True, False])  # Random Start
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not running:
            break

        if player_turn:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                col = mouseX // SQUARE_SIZE

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if is_winner(board, PLAYER_PIECE):
                        print("Player win")
                        running = False

                    player_turn = False

        else:
            col, minimax_score = minimax(board, 3, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if is_winner(board, AI_PIECE):
                    print("AI Win")
                    running = False

                player_turn = True

        draw_board(board)
pygame.quit()
