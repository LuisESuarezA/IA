import random

class Board(dict):
    def __init__(self):
        super().__init__()
        for key in 'abcdefghi':
            self[key] = None
        self.count = 0
        self.winning_combinations = [
            'abc', 'def', 'ghi',  # Rows
            'adg', 'beh', 'cfi',  # Columns
            'aei', 'ceg'          # Diagonals
        ]

    def __str__(self):
        return (
            f"{self['a'] or ' '} | {self['b'] or ' '} | {self['c'] or ' '}\n"
            f"---------\n"
            f"{self['d'] or ' '} | {self['e'] or ' '} | {self['f'] or ' '}\n"
            f"---------\n"
            f"{self['g'] or ' '} | {self['h'] or ' '} | {self['i'] or ' '}"
        )

    def set_value(self, key, value):
        if self[key] is None:
            self[key] = value
            self.count += 1
            return True
        return False

    def checkState(self):
        for combo in self.winning_combinations:
            if self[combo[0]] == self[combo[1]] == self[combo[2]] and self[combo[0]] is not None:
                return self[combo[0]]
        if self.count == 9:
            return 'Tie'
        return None

class MetaBoard(dict):
    def __init__(self):
        super().__init__()
        for key in 'ABCDEFGHI':
            self[key] = Board()
        self.current_board = None
        self.winning_combinations = [
            'ABC', 'DEF', 'GHI',  # Rows
            'ADG', 'BEH', 'CFI',  # Columns
            'AEI', 'CEG'          # Diagonals
        ]

    def checkMetaState(self):
        for combo in self.winning_combinations:
            states = [self[key].checkState() for key in combo]
            if states[0] in ['X', 'O'] and all(state == states[0] for state in states):
                return states[0]
        if all(self[key].checkState() is not None for key in 'ABCDEFGHI'):
            return 'Tie'
        return None

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

def human_move(meta_board):
    while True:
        move = input("Enter your move (board A-I and position a-i, e.g., Ab): ").strip()
        if len(move) != 2:
            print("Invalid input. Please enter two characters: one for the board (A-I) and one for the position (a-i).")
            continue
        
        meta_key = move[0].upper()
        board_key = move[1].lower()

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

        return meta_key, board_key

def evaluate_board(meta_board, player):
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    for board_key in 'ABCDEFGHI':
        board_state = meta_board[board_key].checkState()
        if board_state == player:
            score += 10
        elif board_state == opponent:
            score -= 10
        elif board_state is None:
            score += sum(1 for pos in 'abcdefghi' if meta_board[board_key][pos] == player)
            score -= sum(1 for pos in 'abcdefghi' if meta_board[board_key][pos] == opponent)
    return score

def minimax(meta_board, depth, is_maximizing, player, alpha, beta):
    state = meta_board.checkMetaState()
    if state == player:
        return 1000
    elif state == ('O' if player == 'X' else 'X'):
        return -1000
    elif state == 'Tie':
        return 0
    elif depth == 0:
        return evaluate_board(meta_board, player)

    if is_maximizing:
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
    else:
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

def ai_move(meta_board, depth=3):
    best_score = float('-inf')
    best_move = None
    player = 'X'  # AI is always 'X'

    valid_boards = [meta_board.current_board] if meta_board.current_board else 'ABCDEFGHI'
    for meta_key in valid_boards:
        if meta_board[meta_key].checkState() is None:
            for board_key in 'abcdefghi':
                if meta_board[meta_key][board_key] is None:
                    meta_board[meta_key][board_key] = player
                    score = minimax(meta_board, depth - 1, False, player, float('-inf'), float('inf'))
                    meta_board[meta_key][board_key] = None
                    if score > best_score:
                        best_score = score
                        best_move = (meta_key, board_key)

    return best_move

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
        
        if current_player == 'O':
            meta_key, board_key = human_move(meta_board)
        else:
            print("AI is thinking...")
            meta_key, board_key = ai_move(meta_board)
            print(f"AI played: {meta_key}{board_key}")
        
        meta_board[meta_key].set_value(board_key, current_player)
        meta_board.current_board = board_key.upper() if meta_board[board_key.upper()].checkState() is None else None
        
        board_state = meta_board[meta_key].checkState()
        if board_state:
            print(f"Board {meta_key} has been won by {board_state}!" if board_state != 'Tie' else f"Board {meta_key} is a tie!")
        
        meta_state = meta_board.checkMetaState()
        if meta_state:
            print("\nFinal board state:")
            print(meta_board)
            if meta_state == 'Tie':
                print("The game is a tie!")
            else:
                print(f"Player {meta_state} wins the game!")
            break
        
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    play_game()