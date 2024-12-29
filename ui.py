import pygame
import os
import chess
import time
import chesslogic

# Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (106, 168, 79)
PIECE_SIZE = SQUARE_SIZE  # Size of each piece

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Bot')

# Map piece symbols to file names
PIECE_MAP = {
    'P': 'wP.png', 'N': 'wN.png', 'B': 'wB.png',
    'R': 'wR.png', 'Q': 'wQ.png', 'K': 'wK.png',
    'p': 'bP.png', 'n': 'bn.png', 'b': 'bB.png',
    'r': 'bR.png', 'q': 'bQ.png', 'k': 'bK.png'
}
# Dictionary to store Pygame surfaces for pieces
PIECE_IMAGES = {}

def load_piece_images():
    """Load all PNG images as Pygame surfaces."""
    base_dir = os.path.dirname(__file__)
    for piece, filename in PIECE_MAP.items():
        img_dir = os.path.join(base_dir, "img")
        file_path = os.path.join(img_dir, filename)
        PIECE_IMAGES[piece] = pygame.image.load(file_path).convert_alpha()

def draw_board():
    """Draw the chessboard."""
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board):
    """Draw the pieces on the board."""
    for square, piece in board.piece_map().items():
        row = 7 - (square // 8)
        col = square % 8
        piece_symbol = piece.symbol()
        piece_image = PIECE_IMAGES[piece_symbol]
        piece_rect = piece_image.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
        screen.blit(piece_image, piece_rect.topleft)
    
def choose_piece(screen):
    """Select user's piece choice"""
    running, bot_color, choice = True, False, False
    while choice == False and running == True and bot_color == False:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 50)
        text_surface = font.render("Press W for White and B for Black:", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text_surface, text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    choice, bot_color = True, True
                    break
                elif event.key == pygame.K_w:
                    choice, bot_color = True, False
                    break
        pygame.display.flip()
    return running, bot_color
    
def main():

    board = chess.Board()
    load_piece_images()

    # Variables to track the user's selection
    selected_square = None

    running, bot_color = choose_piece(screen=screen)
    while running:
        
        if(board.turn == bot_color):
            bot_move = chesslogic.get_move(board, 3)
            board.push(bot_move)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Get the clicked square
                    mouse_x, mouse_y = event.pos
                    col = mouse_x // SQUARE_SIZE
                    row = mouse_y // SQUARE_SIZE
                    square = (7 - row) * 8 + col

                    if selected_square is None:
                        # First click: select the piece
                        if board.piece_at(square):  # Check if there is a piece on the selected square
                            selected_square = square
                    
                    else:
                        # Second click: make the move
                        piece = board.piece_at(selected_square)
                        
                        if piece.piece_type != chess.PAWN:
                            move = chess.Move(from_square=selected_square, to_square=square)
                            if move in board.legal_moves:
                                board.push(move)
                                selected_square = None
                            else: selected_square = square
                        
                        else:
                            if (piece.color == chess.WHITE and square in chess.SquareSet(chess.BB_RANK_8)) or (piece.color == chess.BLACK and square in chess.SquareSet(chess.BB_RANK_1)):
                                valid = True
                                promotion_piece = None
                                # Wait for user input for promotion piece
                                while promotion_piece is None and valid:
                                    for sub_event in pygame.event.get():
                                        if sub_event.type == pygame.KEYDOWN:
                                            if sub_event.key == pygame.K_q:
                                                promotion_piece = chess.QUEEN
                                            elif sub_event.key == pygame.K_r:
                                                promotion_piece = chess.ROOK
                                            elif sub_event.key == pygame.K_b:
                                                promotion_piece = chess.BISHOP
                                            elif sub_event.key == pygame.K_k:
                                                promotion_piece = chess.KNIGHT
                                      
                                move = chess.Move(from_square=selected_square, to_square=square, promotion=promotion_piece)
                                if move in board.legal_moves:
                                    board.push(move)
                                    selected_square = None
                                else: selected_square = square
                            else: 
                                move = chess.Move(from_square=selected_square, to_square=square)
                                if move in board.legal_moves:
                                    board.push(move)
                                    selected_square = None
                                else: selected_square = square

        # Draw board and pieces
        draw_board()
        draw_pieces(board)
        
        # Highlight the selected square
        if selected_square is not None:
            # Yellow dots for legal moves
            for move in board.legal_moves:
                if move.from_square == selected_square:
                    dest_square = move.to_square
                    dest_row = 7 - (dest_square // 8)
                    dest_col = dest_square % 8
                    center_x = dest_col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = dest_row * SQUARE_SIZE + SQUARE_SIZE // 2
                    pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y), SQUARE_SIZE // 6)

        pygame.display.flip()
        
        # Check if the game is over
        if board.is_game_over():
            if board.is_checkmate():
                result_message = "Checkmate! You Lose!" if board.turn else "Checkmate! You Won!"
            elif board.is_stalemate():
                result_message = "Stalemate!"
            elif board.is_insufficient_material():
                result_message = "Draw: Insufficient Material!"
            elif board.is_seventyfive_moves():
                result_message = "Draw: 75-Move Rule!"
            elif board.is_fivefold_repetition():
                result_message = "Draw: Fivefold Repetition!"
            else:
                result_message = "Game Over!"

            time.sleep(0.5)
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 74)
            text_surface = font.render(result_message, True, (255, 255, 0))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            time.sleep(2)
            running = False
    pygame.quit()

main()