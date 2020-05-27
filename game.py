import os, pygame, grid
import sys

pygame.init()

def main():

    grid.clean()
    h_choice = 'X'  
    c_choice = 'O'  
    first = 'Y'     #gracz startuje


    while len(grid.empty_cells(grid.board)) > 0 and not grid.game_over(grid.board):
        if first == 'N':
            grid.ai_turn(c_choice, h_choice)
            first = ''

        grid.human_turn(c_choice, h_choice)

        grid.ai_turn(c_choice, h_choice)
    #informacje o przebiegu gry
    if grid.wins(grid.board, grid.HUMAN):
        grid.clean()
        print(f'Human turn [{h_choice}]')
        print('Wygrales!')
    elif grid.wins(grid.board, grid.COMP):
        grid.clean()
        print(f'Computer turn [{c_choice}]')
        print('Przegrales!')
    else:
        grid.clean()
        print('Remis!')
    
    sys.exit()


if __name__ == '__main__':
    main()
