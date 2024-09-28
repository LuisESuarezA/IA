# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 19:48:01 2024

@author: ivanv
"""

# Funciones para el juego de tres en raya
def check_tic_tac_toe(board):
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # filas
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columnas
        (0, 4, 8), (2, 4, 6)              # diagonales
    ]
    
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] in ['X', 'O']:
            return board[combo[0]]  # Retorna el marcador del jugador ganador ('X' o 'O')
    return None  # Retorna None si no hay ganador en el tablero

def board_check(board):
    big_board = [None] * 9
    for i in range(len(board)):
        res = check_tic_tac_toe(board[i])
        big_board[i] = res
    return check_tic_tac_toe(big_board)

def print_ultimate_board(ultimate_board):
    for row in range(3):
        for sub_row in range(3):
            for board_index in range(row * 3, (row + 1) * 3):
                print(' | '.join(str(x) if x is not None else ' ' for x in ultimate_board[board_index][sub_row * 3:(sub_row + 1) * 3]), end='   ')
            print()  
        if row != 2:  
            print('-' * 71)  

def movimientos_validos(current, board):
    posibles = []
    if current is not None and check_tic_tac_toe(board[current]) is None:
        return [[current, i] for i in range(9) if board[current][i] is None]
    else:
        for i in range(9):
            if check_tic_tac_toe(board[i]) is None:
                for j in range(9):
                    if board[i][j] is None:
                        posibles.append([i, j]) 
        return posibles

def movimiento(board, mov, player):
    new_board = [row[:] for row in board]
    new_board[mov[0]][mov[1]] = player
    if check_tic_tac_toe(new_board[mov[0]]) is not None:
        current = None
    else:
        current = mov[1]  # Establece el índice del tablero actual
    player = 'O' if player == 'X' else 'X'  # Cambia el jugador
    return [new_board, current, player]

def game_over(board):
    return board_check(board) is not None

def minimax(board, current, depth, is_maximizing):
    if game_over(board) or depth == 0:
        return evaluate_tic_tac_toe(board)

    if is_maximizing:
        max_eval = float('-inf')
        for move in movimientos_validos(current, board):
            new_board = board.copy()  
            new_board = movimiento(new_board, move, 'O')[0]  
            evaluation = minimax(new_board, current, depth - 1, False)
            max_eval = max(max_eval, evaluation)
        return max_eval
    else:
        min_eval = float('inf')
        for move in movimientos_validos(current, board):
            new_board = board.copy()  
            new_board = movimiento(new_board, move, 'X')[0]  
            evaluation = minimax(new_board, current, depth - 1, True)
            min_eval = min(min_eval, evaluation)
        return min_eval

def best_move(current, board, depth):
    new_board = board.copy()  
    best_score = float('-inf')
    best_move = None
    for move in movimientos_validos(current, new_board):
        temp_board = new_board.copy() 
        temp_board = movimiento(temp_board, move, 'O')[0]
        score = minimax(temp_board, current, depth - 1, True)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def evaluate_tic_tac_toe(board):
    board = [board[i:i+3] for i in range(0, len(board), 3)]
    two_in_row_score = 0.5

    score = 0
    for i in range(3):
        row = board[i]
        if row.count('O') == 3:
            return 5
        elif row.count('X') == 3:
            return -5
        elif row.count('O') == 2 and row.count('X') == 0:
            score += two_in_row_score
        elif row.count('X') == 2 and row.count('O') == 0:
            score -= two_in_row_score
    
        column = [board[0][i], board[1][i], board[2][i]]
        if column.count('O') == 3:
            return 5
        elif column.count('X') == 3:
            return -5
        elif column.count('O') == 2 and column.count('X') == 0:
            score += two_in_row_score
        elif column.count('X') == 2 and column.count('O') == 0:
            score -= two_in_row_score

    diag1 = [board[0][0], board[1][1], board[2][2]]
    diag2 = [board[0][2], board[1][1], board[2][0]]
    for diag in [diag1, diag2]:
        if diag.count('O') == 3:
            return 5
        elif diag.count('X') == 3:
            return -5
        elif diag.count('O') == 2 and diag.count('X') == 0:
            score += two_in_row_score
        elif diag.count('X') == 2 and diag.count('O') == 0:
            score -= two_in_row_score

    return score

def convert_move(move):
    mega_gato_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    mini_gato_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    if move is None:
        return None
    
    mega_index, mini_index = move
    mega_label = mega_gato_labels[mega_index]
    mini_label = mini_gato_labels[mini_index]
    return f"{mega_label}{mini_label}"

def play_game():
    board = [[None] * 9 for _ in range(9)]  # Crea un tablero grande de 3x3
    current = None  # Tablero actual donde se debe jugar
    player = input("Elige tu jugador (X o O): ").strip().upper()
    depth = 3

    while not game_over(board):
        print_ultimate_board(board)
        if player == 'X':
            print("Es tu turno.")
            valid_moves = movimientos_validos(current, board)
            print("Movimientos válidos: ", [convert_move(move) for move in valid_moves])
            mov = input("Introduce tu movimiento (ejemplo: Gc): ")
            mega_index = ord(mov[0]) - ord('A')
            mini_index = ord(mov[1]) - ord('a')
            board, current, player = movimiento(board, [mega_index, mini_index], player)
        else:
            print("Turno de la IA.")
            mov = best_move(current, board, depth)
            board, current, player = movimiento(board, mov, player)
            print(f"Movimiento de la IA: {convert_move(mov)}")

    print_ultimate_board(board)
    if board_check(board) == 'X':
        print("¡El jugador X gana!")
    elif board_check(board) == 'O':
        print("¡La IA gana!")
    else:
        print("¡Es un empate!")

play_game()
