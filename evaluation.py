import chess, random
from typing import Optional, List, Dict, Tuple

class ChessLogic:
    """
    Encapsulates material scoring, piece-square tables, and minimax search with alpha-beta pruning.
    """
    # Base piece values (centipawns)
    PIECE_VALUES: Dict[int, int] = {
        chess.PAWN:   10,
        chess.KNIGHT: 30,
        chess.BISHOP: 30,
        chess.ROOK:   50,
        chess.QUEEN:  90,
        chess.KING:   0,
    }

    # Piece-square tables: nested lists for 8x8 values.
    PIECE_SQUARE_TABLES: Dict[int, List[List[float]]] = {
        chess.KING: [
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
            [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]
        ],
        chess.QUEEN: [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ],
        chess.ROOK: [
            [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
        ],
        chess.BISHOP: [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
            [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
            [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
            [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
            [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        ],
        chess.KNIGHT: [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
            [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
            [-3.0,  0.5,  1.5,  1.7,  1.7,  1.5,  0.5, -3.0],
            [-3.0,  0.0,  1.5,  1.7,  1.7,  1.5,  0.0, -3.0],
            [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
            [-2.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -2.0],
            [-3.0, -0.5,  0.0, -1.0, -1.0,  0.0, -0.5, -3.0]
        ],
        chess.PAWN: [
            [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
            [ 1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
            [ 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
            [ 0.0,  0.0,  2.0,  2.0,  2.0,  2.0,  0.0,  0.0],
            [ 0.5, -0.5, -1.0,  2.0,  2.0, -1.0, -0.5,  0.5],
            [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
            [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ],
    }

    def __init__(self, depth: int = 3):
        self.search_depth = depth
        # Transposition table: zobrist key -> (depth, score)
        self.transposition: Dict[int, Tuple[int, float]] = {}

    def piece_value(self, piece: chess.Piece) -> int:
        return self.PIECE_VALUES.get(piece.piece_type, 0)

    def pos_value(self, piece_type: int, pos: int, color: bool) -> float:
        table = self.PIECE_SQUARE_TABLES[piece_type]
        row = pos // 8 if color else 7 - (pos // 8)
        col = pos % 8
        return table[row][col]

    def evaluate_board(self, board: chess.Board) -> float:
        val = 0.0
        # Material
        for piece in board.piece_map().values():
            v = self.piece_value(piece)
            val += v if piece.color == chess.WHITE else -v
        # Positional
        for sq in range(64):
            piece = board.piece_at(sq)
            if piece:
                color = (piece.color == chess.WHITE)
                val += self.pos_value(piece.piece_type, sq, color)
        return val

    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:
        # Transposition lookup using private key
        key = board._transposition_key()
        entry = self.transposition.get(key)
        if entry and entry[0] >= depth:
            return entry[1]

        if board.is_game_over():
            if board.is_checkmate():
                score = float('inf') if maximizing_player else -float('inf')
            else:
                score = -float('inf') if maximizing_player else float('inf')
        elif depth == 0:
            score = self.evaluate_board(board)
        else:
            moves = list(board.legal_moves)
            # Order captures first
            moves.sort(key=lambda m: board.is_capture(m), reverse=True)

            if maximizing_player:
                score = -float('inf')
                for mv in moves:
                    board.push(mv)
                    val = self.minimax(board, depth-1, alpha, beta, False)
                    board.pop()
                    score = max(score, val)
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break
            else:
                score = float('inf')
                for mv in moves:
                    board.push(mv)
                    val = self.minimax(board, depth-1, alpha, beta, True)
                    board.pop()
                    score = min(score, val)
                    beta = min(beta, val)
                    if beta <= alpha:
                        break
        # Store in transposition table
        self.transposition[key] = (depth, score)
        return score

    def get_move(self, board: chess.Board) -> Optional[chess.Move]:
        self.transposition.clear()
        legal_moves = list(board.legal_moves)
        # Order captures first
        legal_moves.sort(key=lambda m: board.is_capture(m), reverse=True)
        best_move = None
        best_eval = float('inf')
        for mv in legal_moves:
            board.push(mv)
            eval_score = self.minimax(board, self.search_depth-1, -float('inf'), float('inf'), True)
            board.pop()
            if eval_score < best_eval:
                best_eval, best_move = eval_score, mv
        return best_move