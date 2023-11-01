import numpy as np
import random
import pygame
import pygame_menu
import math
import sys
from random import randrange

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 7
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)


class Connect4:

    def __init__(self, depth=1):
        self.depth = depth
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))

    def print_board(self):
        print(np.flip(self.board, 0))

    def reset(self):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))

    @staticmethod
    def drop_piece(board, row, col, piece):
        board[row][col] = piece

    @staticmethod
    def is_valid_location(board, col):
        if col is None:
            return False
        return board[ROW_COUNT - 1][col] == 0

    @staticmethod
    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if Connect4.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    @staticmethod
    def is_terminal_node(board):
        return Connect4.winning_move(board, PLAYER_PIECE) or Connect4.winning_move(board, AI_PIECE) or len(
            Connect4.get_valid_locations(board)) == 0

    @staticmethod
    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    @staticmethod
    def winning_move(board, piece):
        for c in range(COLUMN_COUNT - 1):
            for r in range(ROW_COUNT - 1):
                if board[c, r] == piece and board[c + 1, r] == piece and board[c, r + 1] == piece and board[c + 1, r + 1] == piece:
                    return True
        return False

    @staticmethod
    def evaluate_window(window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        if window.count(piece) == 4:
            score += 200
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 1

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    @staticmethod
    def score_position(board, piece):
        score = 0

        for c in range(COLUMN_COUNT - 2):
            for r in range(ROW_COUNT - 1):
                window = list()
                window.append(board[c, r])
                window.append(board[c + 1, r])
                window.append(board[c, r + 1])
                window.append(board[c + 1, r + 1])
                score += Connect4.evaluate_window(window, piece)

        return score

    @staticmethod
    def minimax(board, depth, alpha, beta, maximizing_player):
        valid_locations = Connect4.get_valid_locations(board)
        is_terminal = Connect4.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if Connect4.winning_move(board, AI_PIECE):
                    return None, 100000000000000
                elif Connect4.winning_move(board, PLAYER_PIECE):
                    return None, -10000000000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, Connect4.score_position(board, AI_PIECE)
        if maximizing_player:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = Connect4.get_next_open_row(board, col)
                b_copy = board.copy()
                Connect4.drop_piece(b_copy, row, col, AI_PIECE)
                new_score = Connect4.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = Connect4.get_next_open_row(board, col)
                b_copy = board.copy()
                Connect4.drop_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = Connect4.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value


game = Connect4()
player_name = "Seth"
starting_player = PLAYER
screen = pygame.display.set_mode(size)

board_colors = [
    ('Random', (-1, -1, -1)),

    ('Tan', (230, 219, 172)),
    ('Beige', (238, 220, 154)),
    ('Macaroon', (248, 224, 118)),
    ('Hazel Wood', (248, 224, 118)),

    ('Granola', (214, 184, 90)),
    ('Oat', (223, 201, 138)),
    ('Egg Nog', (250, 226, 156)),
    ('Fawn', (200, 169, 81)),

    ('Sugar Cookie', (243, 234, 175)),
    ('Sand', (216, 184, 99)),
    ('Sepia', (248, 224, 118)),
    ('Latte', (231, 194, 125)),

    ('Oyster', (220, 215, 160)),
    ('Biscotti', (227, 197, 101)),
    ('Parmesean', (253, 233, 146)),
    ('Hazelnut', (189, 165, 93)),

    ('Sandcastle', (218, 193, 124)),
    ('Buttermilk', (253, 239, 178)),
    ('Sand Dollar', (237, 232, 186)),
    ('Shortbread', (251, 231, 144)),
]

board_color = board_colors[randrange(1, len(board_colors)-1)]


def draw_board(board):

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, board_color[1], (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, BLUE, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def set_difficulty(value, difficulty):
    game.depth = difficulty


def set_starting_player(value, new_starting_player):
    global starting_player
    starting_player = new_starting_player


def set_player_name(new_name):
    global player_name
    player_name = new_name


def change_background_color(selected_value, color, **kwargs):
    global board_color
    value_tuple, index = selected_value
    if color == (-1, -1, -1):
        board_color = board_colors[randrange(1, len(board_colors) - 1)]
        color = board_color[1]
    widget: 'pygame_menu.widgets.Selector' = kwargs.get('widget')
    widget.update_font({'selected_color': color})
    widget.get_selection_effect().color = color


def start_the_game():

    game.print_board()

    game_over = False

    draw_board(game.board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = starting_player

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if game.is_valid_location(game.board, col):
                        row = game.get_next_open_row(game.board, col)
                        game.drop_piece(game.board, row, col, PLAYER_PIECE)

                        if game.winning_move(game.board, PLAYER_PIECE):
                            label = myfont.render(player_name + " wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        game.print_board()
                        draw_board(game.board)

        # # Ask for Player 2 Input
        if turn == AI and not game_over:

            col, minimax_score = game.minimax(game.board, game.depth, -math.inf, math.inf, True)

            if game.is_valid_location(game.board, col):
                # pygame.time.wait(500)
                row = game.get_next_open_row(game.board, col)
                game.drop_piece(game.board, row, col, AI_PIECE)

                if game.winning_move(game.board, AI_PIECE):
                    label = myfont.render("Player 2 wins!!", 1, BLUE)
                    screen.blit(label, (40, 10))
                    game_over = True

                game.print_board()
                draw_board(game.board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)
            game.reset()


pygame.init()


menu = pygame_menu.Menu('Connect 4 (In a square)', 500, 400, theme=pygame_menu.themes.THEME_DARK)
menu.add.text_input('Name :', default=player_name, onchange=set_player_name)
menu.add.selector('Difficulty :',
                  [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)],
                  default=0,
                  onchange=set_difficulty)
menu.add.selector('Starting Player :',
                  [(player_name, PLAYER), ("Player 2", AI)],
                  onchange=set_starting_player)
selector = menu.add.selector(
    title='Board color:\t',
    items=board_colors,
    onreturn=change_background_color,
    onchange=change_background_color
)
selector.add_self_to_kwargs()

menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)


