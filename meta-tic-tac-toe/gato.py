def human_move(meta_board):
    """
    Esta función solicita al usuario que ingrese un movimiento válido.
    """
    while True:
        move = input("Que quieres mover (tablero A-I y posicion a-i, e.g., Ab): ").strip()
        if len(move) != 2:
            print("Demasiados caracteres. Solo puedes introducir dos caracteres: una letra para el tablero (A-I) y una para la posicion (a-i).")
            continue
        
        # esta parte es por si escribes mal el movimiento, por ejemplo, si escribes "A1" en lugar de "Aa" lo corrige
        meta_key = move[0].upper()
        board_key = move[1].lower()

        print(f"Intentando: {meta_key}{board_key}")

        if meta_key not in 'ABCDEFGHI':
            print(f"valor de tablero invalida '{meta_key}'. Tiene que ser una letra entre A I.")
            continue

        if board_key not in 'abcdefghi':
            print(f"valor de posicion invalida '{board_key}'. Tiene que ser una letra entre a, i.")
            continue

        # Checa si el movimineto que hiciste se puede hacer
        if meta_board.current_board is not None and meta_board.current_board != meta_key:
            print(f"Tienes que jugar en el tablero: {meta_board.current_board}. Movimiento en el tablero {meta_key} no se puede.")
            continue

        # Checa si el minitablero ya esta ganado o perdido
        board_state = meta_board[meta_key].checkState()
        if board_state is not None:
            print(f"Tablero {meta_key} ya fue ganado o empatado. Estado actual: {board_state}")
            continue

        # Checa si la posición ya esta ocupada
        if meta_board[meta_key][board_key] is not None:
            print(f"Posicion {board_key} en tablero {meta_key} ya esta ocupada.")
            continue

        return meta_key, board_key
    
def evaluate_board(meta_board, player):
    """
    Evalua el tablero para un jugador dado.
    Regresa:
        +1 su gana la IA,
        -1 si gana el jugador,
        0 si el juego sigue o esta empatado.
    """
    for board_key in 'ABCDEFGHI':
        board_state = meta_board[board_key].checkState()
        if board_state == player:
            return 1 if player == 'X' else -1
        elif board_state == ('O' if player == 'X' else 'X'):
            return -1 if player == 'X' else 1
    return 0  # si el juego esta en progreso o empatado


def minimax(meta_board, depth, is_maximizing, current_player, opponent, valid_boards):
    """
    Algoritmo minimax con para la IA 
    Toma como parametros:
    - meta_board: El estado actual del metatablero 
    - depth: Valor actual de la profundidad
    - is_maximizing: boleano que indica si la IA esta sigue maximizando 
    - current_player: que jugador esta jugando la IA
    - opponent: que jugador es el humano 
    - valid_boards: Lista de tableros validos en los que la IA puede jugar
    
    Returns: Una tupla con el valor de la evaluación y el mejor movimiento
    """
    # Caso base: si el juego ya termino o llegamos al final de la profundidad
    board_eval = evaluate_board(meta_board, current_player)
    if board_eval != 0 or depth == 0:  # Estado terminal
        return board_eval, None
    
    best_move = None

    if is_maximizing:
        max_eval = float('-inf')  # ponemos el valor inicial en negativo infinito
        # Iteramos sobre los tableros y posiciones validas
        for board_key in valid_boards:
            for pos_key in 'abcdefghi':
                if meta_board[board_key][pos_key] is None:
                    # Simulamos el moviemiento
                    meta_board[board_key][pos_key] = current_player
                    score, _ = minimax(meta_board, depth - 1, False, current_player, opponent, valid_boards)
                    meta_board[board_key][pos_key] = None  # deshacemos el movimiento
                    if score > max_eval:
                        max_eval = score
                        best_move = (board_key, pos_key)
        return max_eval, best_move
    else:
        min_eval = float('inf')  # Ponemos el valor inicial a infinito 
        # Iteramos sobre los tableros y posiciones validas
        for board_key in valid_boards:
            for pos_key in 'abcdefghi':
                if meta_board[board_key][pos_key] is None:
                    # Simulate the move
                    meta_board[board_key][pos_key] = opponent
                    score, _ = minimax(meta_board, depth - 1, True, current_player, opponent, valid_boards)
                    meta_board[board_key][pos_key] = None  # Undo the move
                    if score < min_eval:
                        min_eval = score
                        best_move = (board_key, pos_key)
        return min_eval, best_move


def ai_move(meta_board, depth=3):
    """
    Dejamos que la IA juegue usando la funcion minimax 
    con control de profuncidad y siguiendo las reglas
    Tiene que jugar en el mini tablero que le toca 
    Dependiendo del movimeinto anterior del otro jugador
    """
    current_player = 'X'  # IA siempre es 'X'
    opponent = 'O'        # Persona siempre es 'O'

    # si un tablero es obligatorio, solo se puede jugar en ese tablero
    if meta_board.current_board is not None:
        board_to_play_in = meta_board.current_board
        # Si el tablero actual ya esta ganado o empatado, se puede jugar en cualquier tablero disponible
        if meta_board[board_to_play_in].checkState() is None:
            # IA solo puede jugar en el tablero actual
            valid_boards = [board_to_play_in]
        else:
            # si el tablero actual ya esta ganado o empatado, se puede jugar en cualquier tablero disponible
            valid_boards = [key for key in 'ABCDEFGHI' if meta_board[key].checkState() is None]
    else:
        # si no hay restricciones, IA puede jugar en cualquier tablero disponible
        valid_boards = [key for key in 'ABCDEFGHI' if meta_board[key].checkState() is None]

    # Usar la funcion minimax para encontrar el mejor movimiento
    _, move = minimax(meta_board, depth, True, current_player, opponent, valid_boards)
    
    if move:
        meta_key, board_key = move
        meta_board[meta_key][board_key] = current_player
        return meta_key, board_key
    return None  # no se encontro un movimiento valido




class Board(dict):
    def __init__(self):
        super().__init__()
        for key in 'abcdefghi':
            self[key] = None  # empeza con todos los valores en None
        self.winning_combinations = [
            'abc', 'def', 'ghi',  # filas
            'adg', 'beh', 'cfi',  # Columnas
            'aei', 'ceg'          # Diagonales
        ]
        self.count = 0

    def checkState(self):
        """checar el estado del tablero si ya gano alguien o si esta empatado"""
        for combo in self.winning_combinations:
            if self[combo[0]] == self[combo[1]] == self[combo[2]] and self[combo[0]] is not None:
                return self[combo[0]]  # Regresar el ganador
        if self.count == 9:
            return 'Tie'  # Si esta lleno y no hay ganador, es un empate
        return None  # GEl juego sigue

    def set_value(self, key, value):
        if self[key] is None:
            self[key] = value
            self.count += 1
            return True
        return False  # Posicion ya ocupada
    def __str__(self):
        """Return a string representation of the board."""
        return (
            f"{self['a']} | {self['b']} | {self['c']}\n"
            f"---------\n"
            f"{self['d']} | {self['e']} | {self['f']}\n"
            f"---------\n"
            f"{self['g']} | {self['h']} | {self['i']}"
        ).replace('None', ' ')


class MetaBoard(dict):
    def __init__(self):
        super().__init__()
        for key in 'ABCDEFGHI':
            self[key] = Board()  # cada meta tablero tiene un tablero
        self.current_board = None  # empezar si restricciones

    def checkMetaState(self):
        """chaecar el estado del metatablero si ya gano alguien o si esta empatado"""
        for board in self.values():
            if board.checkState() is not None:
                return True
        return False

def play_game(meta_board):
    # Preguntar si la IA juega primero (X) o segundo (O)
    choice = input("¿Quieres que la IA juege primero o despues? ").strip().lower()
    
    if choice == 'primero':
        current_player = 'X'  # IA va primero
    else:
        current_player = 'O'  # jugador va primero

    while not meta_board.checkMetaState():
        print(f"turno del jugador {current_player} ")
        print(print_meta_board(meta_board))

        if current_player == 'X':
            # Turno de la IA
            print("Pensando en el mejor movimiento...")
            meta_key, board_key = ai_move(meta_board)
            meta_board.current_board = board_key.upper()  # Poner el siguiente tablero en el que se juega 
            print(f"Movimiento de la IA: {meta_key}{board_key}")
        else:
            # Turno del jugador
            meta_key, board_key = human_move(meta_board)
            meta_board[meta_key].set_value(board_key, current_player)
            meta_board.current_board = board_key.upper()  # Poner el siguiente tablero en el que se juega

        # Cambio de turno 
        current_player = 'O' if current_player == 'X' else 'X'



def print_meta_board(meta_board):
    """Devuelve una representación en cadena del Meta_Board."""
    meta_rows = ['ABC', 'DEF', 'GHI']
    rows = ['abc', 'def', 'ghi']
    meta_str = ""
        
    for meta_row in meta_rows:
        # Dividir cada tablero en sus tres filas
        board_rows = [str(meta_board[key]).split('\n') for key in meta_row]
        
        # Combinar las filas de los tres tableros en cada fila del meta-tablero
        for i in range(5):
            meta_str += " | ".join(board_rows[j][i] for j in range(3)) + "\n"
            
        if meta_row != meta_rows[-1]:
            meta_str += "-" * 34 + "\n"
    
    return meta_str

# Crear el metatablero y empezar el juego
meta_board = MetaBoard()
play_game(meta_board)
