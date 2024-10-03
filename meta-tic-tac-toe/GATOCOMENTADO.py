# -*- coding: utf-8 -*-
"""
Manual de Usuario

Descripción General
Este juego es una versión de "Ultimate Tic-Tac-Toe", donde se juega en 9 tableros de Tic-Tac-Toe (gatos) individuales organizados en una cuadrícula de 3x3. Cada movimiento afecta a qué tablero jugará el oponente en el siguiente turno.

Cómo Jugar
- Tú juegas como 'O' y la IA juega como 'X'.
- Al inicio del juego, puedes elegir si juegas primero o si lo hace la IA.
- Para hacer una jugada, debes ingresar dos caracteres: 
  - El primero representa el tablero en el que deseas jugar (A-I).
  - El segundo representa la posición dentro de ese tablero (a-i).

Ejemplo de Entrada:
- Si ingresas `Ae`, significa que jugarás en la posición central del tablero superior izquierdo (tablero A, posición e).

Reglas Especiales:
- Si juegas en una posición dentro de un tablero, tu oponente debe jugar en el tablero correspondiente a esa posición.
- Si un tablero ya fue ganado o empatado, no se puede jugar en él.
- El juego termina cuando se ha ganado el tablero meta o si todos los tableros están ocupados y no hay más movimientos posibles (empate).

Objetivo del Juego:
- El objetivo es ganar tres tableros individuales en línea (fila, columna o diagonal) dentro del tablero meta.

"""

# Clase que representa un tablero individual de Tic-Tac-Toe
class Board(dict):
    def __init__(self):
        super().__init__()
        for key in 'abcdefghi':  # Inicializa cada posición del tablero como None
            self[key] = None
        self.count = 0  # Lleva la cuenta de cuántas jugadas se han realizado
        # Definición de las combinaciones ganadoras
        self.winning_combinations = [
            'abc', 'def', 'ghi',  # Filas
            'adg', 'beh', 'cfi',  # Columnas
            'aei', 'ceg'          # Diagonales
        ]

    # Método que devuelve el estado del tablero en formato string
    def __str__(self):
        return (
            f"{self['a'] or ' '} | {self['b'] or ' '} | {self['c'] or ' '}\n"
            f"---------\n"
            f"{self['d'] or ' '} | {self['e'] or ' '} | {self['f'] or ' '}\n"
            f"---------\n"
            f"{self['g'] or ' '} | {self['h'] or ' '} | {self['i'] or ' '}"
        )

    # Método que asigna un valor (X o O) a una posición si está disponible
    def set_value(self, key, value):
        if self[key] is None:
            self[key] = value
            self.count += 1
            return True
        return False

    # Método para verificar si alguien ganó o si el tablero terminó en empate
    def checkState(self):
        for combo in self.winning_combinations:  # Revisa todas las combinaciones ganadoras
            if self[combo[0]] == self[combo[1]] == self[combo[2]] and self[combo[0]] is not None:
                return self[combo[0]]  # Devuelve el ganador (X u O)
        if self.count == 9:  # Si se llenaron las 9 posiciones sin ganador, es empate
            return 'Tie'
        return None  # Si aún no hay ganador ni empate

# Clase que representa el tablero meta (tablero de tableros)
class MetaBoard(dict):
    def __init__(self):
        super().__init__()
        for key in 'ABCDEFGHI':  # Inicializa 9 tableros individuales
            self[key] = Board()
        self.current_board = None  # Indica el tablero en el que debe jugarse la próxima jugada
        # Combinaciones ganadoras para el tablero meta
        self.winning_combinations = [
            'ABC', 'DEF', 'GHI',  # Filas
            'ADG', 'BEH', 'CFI',  # Columnas
            'AEI', 'CEG'          # Diagonales
        ]

    # Verifica el estado del tablero meta (si hay un ganador o empate)
    def checkMetaState(self):
        for combo in self.winning_combinations:  # Revisa todas las combinaciones ganadoras en el tablero meta
            states = [self[key].checkState() for key in combo]
            if states[0] in ['X', 'O'] and all(state == states[0] for state in states):
                return states[0]  # Devuelve el ganador del tablero meta
        if all(self[key].checkState() is not None for key in 'ABCDEFGHI'):  # Si todos los tableros individuales terminaron
            return 'Tie'  # Empate
        return None

    # Método para imprimir el estado actual del tablero meta
    def __str__(self):
        meta_rows = ['ABC', 'DEF', 'GHI']
        meta_str = ""
        for meta_row in meta_rows:
            board_rows = [str(self[key]).split('\n') for key in meta_row]
            for i in range(5):
                meta_str += " | ".join(board_rows[j][i] for j in range(3)) + "\n"
            if meta_row != meta_rows[-1]:
                meta_str += "-" * 34 + "\n"
        return meta_str

# Función que permite al jugador humano realizar su movimiento
def human_move(meta_board):
    while True:
        move = input("Enter your move (board A-I and position a-i, e.g., Ab): ").strip()
        if len(move) != 2:
            print("Invalid input. Please enter two characters: one for the board (A-I) and one for the position (a-i).")
            continue
        
        meta_key = move[0].upper()  # Tablero seleccionado
        board_key = move[1].lower()  # Posición dentro del tablero

        # Validaciones de entrada
        if meta_key not in 'ABCDEFGHI' or board_key not in 'abcdefghi':
            print("Invalid input. Please use letters A-I for the board and a-i for the position.")
            continue

        if meta_board.current_board is not None and meta_board.current_board != meta_key:
            print(f"You must play in board {meta_board.current_board}.")
            continue

        if meta_board[meta_key].checkState() is not None:
            print(f"Board {meta_key} is already won or tied.")
            continue

        if meta_board[meta_key][board_key] is not None:
            print(f"Position {board_key} in board {meta_key} is already occupied.")
            continue

        return meta_key, board_key  # Devuelve el movimiento válido

# Evalúa el tablero desde la perspectiva de un jugador
def evaluate_board(meta_board, player):
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    for board_key in 'ABCDEFGHI':
        board_state = meta_board[board_key].checkState()
        if board_state == player:
            score += 10  # Si el tablero fue ganado por el jugador, suma 10
        elif board_state == opponent:
            score -= 10  # Si el tablero fue ganado por el oponente, resta 10
        elif board_state is None:  # Si el tablero no ha terminado
            # Suma un punto por cada posición ocupada por el jugador, resta por el oponente
            score += sum(1 for pos in 'abcdefghi' if meta_board[board_key][pos] == player)
            score -= sum(1 for pos in 'abcdefghi' if meta_board[board_key][pos] == opponent)
    return score

# Algoritmo Minimax con poda alpha-beta para decidir el mejor movimiento de la IA
def minimax(meta_board, depth, is_maximizing, player, alpha, beta):
    state = meta_board.checkMetaState()
    if state == player:  # Si la IA ganó
        return 1000
    elif state == ('O' if player == 'X' else 'X'):  # Si el oponente ganó
        return -1000
    elif state == 'Tie':  # Si es empate
        return 0
    elif depth == 0:  # Si se ha alcanzado la profundidad máxima de búsqueda
        return evaluate_board(meta_board, player)

    if is_maximizing:  # Si es el turno de maximizar (IA)
        best_score = float('-inf')
        for meta_key in 'ABCDEFGHI':
            if meta_board[meta_key].checkState() is None:
                for board_key in 'abcdefghi':
                    if meta_board[meta_key][board_key] is None:
                        meta_board[meta_key][board_key] = player
                        score = minimax(meta_board, depth - 1, False, player, alpha, beta)
                        meta_board[meta_key][board_key] = None
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
        return best_score
    else:  # Si es el turno de minimizar (oponente)
        best_score = float('inf')
        opponent = 'O' if player == 'X' else 'X'
        for meta_key in 'ABCDEFGHI':
            if meta_board[meta_key].checkState() is None:
                for board_key in 'abcdefghi':
                    if meta_board[meta_key][board_key] is None:
                        meta_board[meta_key][board_key] = opponent
                        score = minimax(meta_board, depth - 1, True, player, alpha, beta)
                        meta_board[meta_key][board_key] = None
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
        return best_score

# Función que ejecuta el movimiento de la IA usando el algoritmo Minimax
def ai_move(meta_board):
    best_score = float('-inf')
    best_move = None
    for meta_key in 'ABCDEFGHI':
        if meta_board[meta_key].checkState() is None:
            for board_key in 'abcdefghi':
                if meta_board[meta_key][board_key] is None:
                    meta_board[meta_key][board_key] = 'X'
                    score = minimax(meta_board, 3, False, 'X', float('-inf'), float('inf'))
                    meta_board[meta_key][board_key] = None
                    if score > best_score:
                        best_score = score
                        best_move = (meta_key, board_key)

    return best_move

# Función principal que permite jugar al juego
def play_game():
    meta_board = MetaBoard()
    
    print("Welcome to Ultimate Tic-Tac-Toe!")
    print("You are 'O', and the AI is 'X'.")
    print("Enter your moves as two letters: the first for the board (A-I), the second for the position (a-i).")
    print("For example, 'Ae' means you're playing in the center of the top-left board.")
    
    while True:
        first_move = input("Who should make the first move? (1 for You, 2 for AI): ").strip()
        if first_move in ['1', '2']:
            current_player = 'O' if first_move == '1' else 'X'
            break
        else:
            print("Invalid input. Please enter 1 or 2.")
    
    while True:
        print("\nCurrent board state:")
        print(meta_board)
        print(f"Current player: {current_player}")
        
        if meta_board.current_board:
            print(f"You must play in board {meta_board.current_board}")
        
        if current_player == 'O':  # Turno del humano
            meta_key, board_key = human_move(meta_board)
        else:  # Turno de la IA
            print("AI is thinking...")
            meta_key, board_key = ai_move(meta_board)
            print(f"AI played: {meta_key}{board_key}")
        
        meta_board[meta_key].set_value(board_key, current_player)
        meta_board.current_board = board_key.upper() if meta_board[board_key.upper()].checkState() is None else None
        
        # Verifica si hay ganador o empate en el tablero individual
        board_state = meta_board[meta_key].checkState()
        if board_state:
            print(f"Board {meta_key} has been won by {board_state}!" if board_state != 'Tie' else f"Board {meta_key} is a tie!")
        
        # Verifica si hay ganador o empate en el tablero meta
        meta_state = meta_board.checkMetaState()
        if meta_state:
            print("\nFinal board state:")
            print(meta_board)
            if meta_state == 'Tie':
                print("The game is a tie!")
            else:
                print(f"Player {meta_state} wins the game!")
            break
        
        # Cambia de turno
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    play_game()
