import pygame
import chess
import time
from evaluation import ChessLogic
from pathlib import Path
from constants import *
from renderer import Renderer, Phase

def mouse_to_square(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return (7 - row) * 8 + col

def ask_promotion():
    """Block until the user picks Q/R/B/K or clicks; return chess piece or None."""
    pygame.event.clear()
    while True:
        ev = pygame.event.wait()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            return None
        if ev.type == pygame.KEYDOWN:
            return {
                pygame.K_q: chess.QUEEN,
                pygame.K_r: chess.ROOK,
                pygame.K_b: chess.BISHOP,
                pygame.K_k: chess.KNIGHT
            }.get(ev.key, None)

def choose_color(screen, renderer):
    screen.fill(WHITE)
    renderer.show_text("Press W for White or B for Black")
    pygame.display.flip()
    while True:
        ev = pygame.event.wait()
        if ev.type == pygame.QUIT:
            return False, False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_w:
                return True, False
            if ev.key == pygame.K_b:
                return True, True


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess Bot')
    clock = pygame.time.Clock()

    img_dir = Path(__file__).parent / 'img'
    renderer = Renderer(screen, img_dir)
    chesslogic = ChessLogic(depth=3)
    board = chess.Board()

    running, bot_color = choose_color(screen, renderer)
    if not running:
        pygame.quit()
        return

    phase = Phase.WAITING_SOURCE
    selected = None
    legal_moves = []

    while running:
        clock.tick(FPS)
        # Bot move
        if board.turn == bot_color:
            board.push(chesslogic.get_move(board))
            phase = Phase.WAITING_SOURCE

        # Event handling
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                break

            if board.turn != bot_color:
                if phase == Phase.WAITING_SOURCE and ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    sq = mouse_to_square(ev.pos)
                    piece = board.piece_at(sq)
                    if piece and piece.color != bot_color:
                        selected = sq
                        legal_moves = [m for m in board.legal_moves if m.from_square == sq]
                        phase = Phase.WAITING_DEST

                elif phase == Phase.WAITING_DEST and ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    dst = mouse_to_square(ev.pos)
                    move = chess.Move(from_square=selected, to_square=dst)
                    # Pawn promotion check
                    piece = board.piece_at(selected)
                    rank_mask = chess.BB_RANK_8 if piece.color == chess.WHITE else chess.BB_RANK_1
                    if piece.piece_type == chess.PAWN and dst in chess.SquareSet(rank_mask) and dst % 8 == selected % 8:
                        promotion = chesslogic.ask_promotion()
                        if promotion:
                            move = chess.Move(selected, dst, promotion=promotion)
                    if move in board.legal_moves:
                        board.push(move)
                    phase = Phase.WAITING_SOURCE
                    selected, legal_moves = None, []

        # Rendering
        renderer.draw_board()
        renderer.draw_pieces(board)
        if selected is not None:
            renderer.highlight({'moves': legal_moves})

        pygame.display.flip()

        # Check for game over
        if board.is_game_over():
            time.sleep(0.5)
            screen.fill((0, 0, 0))
            msg = 'Draw' if board.is_stalemate() else ('Checkmate: You Lost' if board.turn else 'Checkmate: You Won')
            renderer.show_text(msg)
            pygame.display.flip()
            time.sleep(2)
            running = False

    pygame.quit()

if __name__ == '__main__':
    main()