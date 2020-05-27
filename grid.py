from math import inf as infinity
from random import choice
import platform
import pygame
import time
import os
from os import system
import sys
from sys import exit
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,100'
pink = [255, 192, 203]
screen = pygame.display.set_mode((600, 600))
screen.fill(pink)
pygame.display.update()
pygame.display.set_caption('TicTacToe')
pygame.display.flip()

X_sign = pygame.image.load(os.path.join('X.png'))
O_sign = pygame.image.load(os.path.join('O.png'))

COMP = +1
HUMAN = -1

board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):  # stan aktualnej planszy
    if wins(state, HUMAN):  # zwraca +1 jesli wygrywa COMP
        score = -1  # zwraca -1 jesli wygyrwa HUMAN
    elif wins(state, COMP):  # zwraca 0 jesli jest remis
        score = +1
    else:
        score = 0

    return score


def wins(state, player):
    # funkcja sprawdza mozliwosc wygranej przez danego gracza
    # mozliwosci:
    # trzy wiersze [X X X] lub [O O O]
    # trzy kolumny [X X X] lub [O O O]
    # dwa diagonale [X X X] lub [O O O]
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    # kazda wolna komorka bedzie dodana do listy komorek
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    # ruch na planszy jesli koordynaty sa dostepne
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    # funkcja dzieki ktorej sztuczna inteligencja wykonuje najlepszy mozliwy ruch
    # depth - indeks w drzewie, przyjmuje [0,9]
    # funkcja zwraca liste z najlepszym wierszem, najlepsza kolumna, najlepszym wynikiem
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max v
        else:
            if score[2] < best[2]:
                best = score  # min v

    return best


def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):  # renderuje plansze do konsoli

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def get_mouse():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if pos[1] < 200:
                        return (pos[0] // 200) + 1
                    if 200 <= pos[1] <= 400:
                        return (pos[0] // 200) + 4
                    if pos[1] > 400:
                        return (pos[0] // 200) + 7


def ai_turn(c_choice, h_choice):
    # jest uzywana funkcja minimax jesli depth<9
    # jezeli nie, zostaje wybrany losowy koordynat
    # c_choice - wybor komputera
    # h_choice - wybor gracza

    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Komputer rusza [{c_choice}]')

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)

    screen.fill((0, 0, 0))
    draw(screen, board, c_choice, h_choice)
    pygame.display.flip()


def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Twoj ruch [{h_choice}]')

    screen.fill((255, 192, 203))
    draw(screen, board, c_choice, h_choice)
    pygame.display.flip()

    while move < 1 or move > 9:
        try:
            move = int(get_mouse())
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Zly ruch!')
                move = -1
        except(EOFError, KeyboardInterrupt):
            print('Zegnam')
            exit()
        except(KeyError, ValueError):
            print('Zly wybor!')


def draw(screen, state, c_choice, h_choice):
    grid_lines = [
        ((0, 200), (600, 200)),
        ((0, 400), (600, 400)),
        ((200, 0), (200, 600)),
        ((400, 0), (400, 600))
    ]

    for line in grid_lines:
        pygame.draw.line(screen, (255, 255, 255), line[0], line[1], 2)

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }

    i = 0
    j = 0

    for row in state:
        for cell in row:
            symbol = chars[cell]
            if symbol == 'X':
                screen.blit(X_sign, (i * 200, j * 200))
            elif symbol == 'O':
                screen.blit(O_sign, (i * 200, j * 200))
            i += 1
        j += 1
        i = 0
