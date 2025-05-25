from enum import Enum
from constants import *
from pathlib import Path
import pygame

class Phase(Enum):
    CHOOSING_COLOR = 1
    WAITING_SOURCE = 2
    WAITING_DEST = 3
    PROMOTING = 4
    
class Renderer:
    def __init__(self, screen, img_folder: Path):
        self.screen = screen
        self.img_folder = img_folder
        self._load_images()
        self.font = pygame.font.Font(None, FONT_SIZE)

    def _load_images(self):
        PIECE_MAP = {
            'P': 'wP.png', 'N': 'wN.png', 'B': 'wB.png',
            'R': 'wR.png', 'Q': 'wQ.png', 'K': 'wK.png',
            'p': 'bP.png', 'n': 'bn.png', 'b': 'bB.png',
            'r': 'bR.png', 'q': 'bQ.png', 'k': 'bK.png'
        }
        self.images = {}
        for sym, fname in PIECE_MAP.items():
            path = self.img_folder / fname
            self.images[sym] = pygame.image.load(str(path)).convert_alpha()

    def draw_board(self):
        for r in range(ROWS):
            for c in range(COLS):
                color = WHITE if (r + c) % 2 == 0 else GREEN
                rect = (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def draw_pieces(self, board):
        for sq, piece in board.piece_map().items():
            row = 7 - (sq // 8)
            col = sq % 8
            img = self.images[piece.symbol()]
            pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                   row * SQUARE_SIZE + SQUARE_SIZE // 2)
            rect = img.get_rect(center=pos)
            self.screen.blit(img, rect.topleft)

    def highlight(self, square):
        # yellow dot on legal destinations
        for move in square['moves']:
            dest = move.to_square
            r = 7 - (dest // 8)
            c = dest % 8
            center = (c * SQUARE_SIZE + SQUARE_SIZE // 2,
                      r * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(self.screen, (255, 255, 0), center, SQUARE_SIZE // 6)

    def show_text(self, message):
        text = self.font.render(message, True, (0, 0, 0))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, rect)