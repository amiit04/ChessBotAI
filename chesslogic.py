import chess, random

#Position Matrix
pos_KING = [
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
    [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
]

pos_QUEEN = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

pos_ROOK = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
]

pos_BISHOP = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
    [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
    [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
    [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
    [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

pos_KNIGHT = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
    [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
    [-3.0, 0.5, 1.5, 1.7, 1.7, 1.5, 0.5, -3.0],
    [-3.0, 0.0, 1.5, 1.7, 1.7, 1.5, 0.0, -3.0],
    [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
    [-2.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -2.0],
    [-3.0, -0.5, 0.0, -1.0, -1.0, 0.0, -0.5, -3.0]
]

pos_PAWN = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
    [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
    [0.0, 0.0, 2.0, 2.0, 2.0, 2.0, 0.0, 0.0],
    [0.5, -0.5, -1.0, 2.0, 2.0, -1.0, -0.5, 0.5],
    [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
]

def piece_value(piece):
    values = {chess.PAWN: 10, chess.KNIGHT: 30, chess.BISHOP: 30, chess.ROOK: 50, chess.QUEEN: 90, chess.KING: 0}
    return values.get(piece.piece_type, 0)

def pos_value(piece, pos, color):
    if(piece == chess.KING):
        return pos_KING[pos // 8 if color == True else 7 - pos // 8][pos % 8]
    if(piece == chess.QUEEN):
        return pos_QUEEN[pos // 8 if color == True else 7 - pos // 8][pos % 8]
    if(piece == chess.ROOK):
        return pos_ROOK[pos // 8 if color == True else 7 - pos // 8][pos % 8]
    if(piece == chess.BISHOP):
        return pos_BISHOP[pos // 8 if color == True else 7 - pos // 8][pos % 8]
    if(piece == chess.KNIGHT):
        return pos_KNIGHT[pos // 8 if color == True else 7 - pos // 8][pos % 8]
    if(piece == chess.PAWN):
        return pos_PAWN[pos // 8 if color == True else 7 - pos // 8][pos % 8]

def evaluate_board(board):
    val = 0
    for piece in board.piece_map().values():
        value = piece_value(piece)
        if piece.color != chess.WHITE:
            value *= -1
        val += value
    
    for square in range(64):
        piece = board.piece_at(square)
        if piece is not None:
            val += pos_value(piece.piece_type, square, True if piece.color == chess.WHITE else False)
    return val

def minimax(board, depth, alpha, beta, maximizing_player):
    if board.is_game_over():
        if board.is_checkmate():
            return float('inf') if maximizing_player else -float('inf')
        else:
            return -float('inf') if maximizing_player else float('inf')
    if depth == 0:
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)
    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_move(state, depth):
    board = chess.Board(state.fen())
    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)
    res_move = None
    min_eval = float('inf')
    for move in legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, -float('inf'), float('inf'), True)
        board.pop()
        if(min_eval > eval):
            min_eval = eval
            res_move = move
    return res_move
    

    
    
    