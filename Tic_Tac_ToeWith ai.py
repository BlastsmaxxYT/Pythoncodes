import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the window size
WIDTH, HEIGHT = 300, 300
WINDOW_SIZE = (WIDTH, HEIGHT)

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set board dimensions
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE

# Create the game window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tic-Tac-Toe")

# Initialize the game board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Variable to keep track of the current player ('X' or 'O')
current_player = 'X'

# Function to draw the game board
def draw_board():
    screen.fill(BLACK)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
            if board[row][col] == 'X':
                pygame.draw.line(screen, RED, (col * CELL_SIZE + 10, row * CELL_SIZE + 10),
                                 ((col + 1) * CELL_SIZE - 10, (row + 1) * CELL_SIZE - 10), 2)
                pygame.draw.line(screen, RED, ((col + 1) * CELL_SIZE - 10, row * CELL_SIZE + 10),
                                 (col * CELL_SIZE + 10, (row + 1) * CELL_SIZE - 10), 2)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, RED, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 10, 2)
    pygame.display.flip()

# Function to check if a player has won
def check_win(player):
    for row in range(BOARD_SIZE):
        if all(board[row][col] == player for col in range(BOARD_SIZE)):
            return True
    for col in range(BOARD_SIZE):
        if all(board[row][col] == player for row in range(BOARD_SIZE)):
            return True
    if all(board[i][i] == player for i in range(BOARD_SIZE)):
        return True
    if all(board[i][BOARD_SIZE - i - 1] == player for i in range(BOARD_SIZE)):
        return True
    return False

# Function to check if the game is a draw
def check_draw():
    return all(board[row][col] != ' ' for row in range(BOARD_SIZE) for col in range(BOARD_SIZE))

# Function to make the AI move
def ai_move():
    best_score = float('-inf')
    best_move = None
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                score = minimax(board, 0, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        row, col = best_move
        board[row][col] = 'O'

# Minimax algorithm implementation
def minimax(board, depth, is_maximizing):
    if check_win('X'):
        return -1
    elif check_win('O'):
        return 1
    elif check_draw():
        return 0
    
    if is_maximizing:
        best_score = float('-inf')
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ' '
                    best_score = min(score, best_score)
        return best_score

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_player == 'X':
                col = event.pos[0] // CELL_SIZE
                row = event.pos[1] // CELL_SIZE
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    current_player = 'O'
                    if not check_win('X') and not check_draw():
                        ai_move()
                        current_player = 'X'
    
    draw_board()
    
    if check_win('X'):
        print("Player X wins!")
        break
    elif check_win('O'):
        print("Player O wins!")
        break
    elif check_draw():
        print("It's a draw!")
        break
