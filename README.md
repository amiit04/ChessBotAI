# ChessBotAI

ChessBotAI is a Python-based chess-playing application featuring an interactive graphical interface (built with Pygame) and a “thinking” engine that uses the **Minimax algorithm** with **Alpha-Beta Pruning** and positional heuristics. Whether you’re learning chess, studying AI techniques, or simply looking for a fun opponent, ChessBotAI offers a smooth user experience and explainable decision-making under the hood.

---

## Table of Contents

1. [Features](#features)
2. [Demo](#demo)
3. [Dependencies & Installation](#dependencies--installation)
4. [Project Structure](#project-structure)
5. [How It Works](#how-it-works)

   * [Game Loop & GUI](#game-loop--gui)
   * [AI Logic & Evaluation](#ai-logic--evaluation)
   * [Minimax with Alpha-Beta Pruning](#minimax-with-alpha-beta-pruning)
   * [Move‐Ordering Heuristics](#move‐ordering-heuristics)
   * [Undo/Redo Functionality](#undoredo-functionality)
6. [Usage & Controls](#usage--controls)
7. [Customization & Configuration](#customization--configuration)
8. [Troubleshooting & FAQs](#troubleshooting--faqs)
9. [Contributing](#contributing)

---

## Features

* **Human vs. AI Gameplay**

  * Play as White or Black against a built‐in AI engine.
  * AI searches to a configurable depth (default: 3).
* **Efficient AI Logic**

  * **Minimax algorithm** for decision-making.
  * **Alpha-Beta pruning** to cut off large portions of the search tree.
  * **Material + Positional evaluation** via piece‐square tables.
  * **MVV-LVA and Killer / History heuristics** to order moves and improve pruning.
* **Interactive Pygame GUI**

  * Click-to-select and move pieces.
  * Smooth sliding animations for piece movement.
  * Highlight legal destinations for the selected piece.
* **Undo & Redo**

  * Press ◀ (Left Arrow) to undo one or two plies (bot + human).
  * Press ▶ (Right Arrow) to redo moves that have been undone.
* **Game-Over Detection**

  * Automatic detection of checkmate, stalemate, fivefold repetition, 75-move rule, insufficient material.
  * Centered “Game Over” message with an explanation (e.g. “Checkmate! You Win”).

---

## Demo

Below is a high-level overview of a typical game session:

1. **Start**: The application opens a Pygame window displaying an empty chessboard.
2. **Choose Side**: You’re prompted to press **W** (White) or **B** (Black).
3. **Gameplay**:

   * If you play White, you click on a piece to select, then click on a legal destination to move.
   * If you play Black, the AI (bot) moves first as White.
4. **Animations**: Each move—your own or the bot’s—is animated with a smooth sliding piece transition.
5. **Undo/Redo**: Press **Left Arrow (◀)** to undo, **Right Arrow (▶)** to redo.
6. **End**: When the game is over (checkmate/draw), a message appears for 2 seconds before exiting.

---

## Dependencies & Installation

### Requirements

* Python 3.7+
* The following packages (see `requirements.txt`):

  ```text
  pygame==2.3.0
  chess==1.9.1
  ```

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/amiit04/ChessBotAI.git
   cd ChessBotAI
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python ui.py
   ```

---

## Project Structure

```
ChessBotAI/
├── img/                        # PNG images for each chess piece
│   ├── wP.png
│   ├── wN.png
│   ├── … (white pieces)
│   ├── bP.png
│   └── … (black pieces)
├── constants.py                # Constants: WIDTH, HEIGHT, SQUARE_SIZE, COLORS, FPS, etc.
├── evaluation.py               # ChessLogic class: evaluation + minimax search
├── renderer.py                 # Renderer class: draw board, pieces, highlights, animations
├── ui.py                       # Main Pygame application (game loop, event handling)
├── requirements.txt            # pip dependencies (pygame, python-chess)
└── README.md                   # This README file
```

* **constants.py**
  Holds shared configuration:

  ```python
  WIDTH, HEIGHT = 640, 640
  ROWS, COLS = 8, 8
  SQUARE_SIZE = WIDTH // COLS
  FPS = 60
  WHITE = (255, 255, 255)
  GREEN = (106, 168, 79)
  FONT_SIZE = 60
  ```

* **evaluation.py**
  Defines `class ChessLogic`:

  * Material scores (`PIECE_VALUES`)
  * Piece-square tables (`PIECE_SQUARE_TABLES`)
  * `evaluate_board()` for static evaluation
  * `minimax()` (with α-β pruning) that returns `(score, best_move)`
  * `get_move(board, turn)` to retrieve AI’s chosen move

* **renderer.py**
  Defines `class Renderer`:

  * `_load_images()` loads PNGs into `self.images`
  * `draw_board()` paints squares
  * `draw_pieces(board)` places piece images
  * `highlight({'moves': legal_moves})` draws dots on legal targets
  * `show_text(message)` draws centered text
  * `animate_move(board, piece_img, from_sq, to_sq, duration)` interpolates piece sliding

* **ui.py**
  Orchestrates the Pygame window and game loop:

  * `mouse_to_square(pos)` maps mouse clicks to 0–63 square indices
  * `ask_promotion()` blocks until Q/R/B/K or click to decide pawn promotion
  * `choose_color()` prompts “Press W or B”
  * Main loop:

    * Bot’s turn → `logic.get_move(...)` → `make_move(...)` → AI animation
    * Human’s turn → click handling, selection, promotion, push move
    * Undo/Redo: Left/Right arrow keys call `undo()` / `redo()` (with animations)
    * Rendering: `renderer.draw_board()`, `renderer.draw_pieces()`, `renderer.highlight(...)`
    * Game-over detection via `check_for_gameover(...)`

---

## How It Works

### Game Loop & GUI

1. **Initialize**

   * Pygame is initialized (`pygame.init()`).
   * The window is created at `WIDTH × HEIGHT`.
   * `Renderer(screen, img_folder)` loads piece images and sets up fonts.

2. **Choose Side**

   * `choose_color()` displays “Press W for White or B for Black.”
   * Depending on your choice, `bot_color` is set to `True` (Black bot) or `False` (White bot).

3. **Main Loop**

   * **Bot’s Turn** (`board.turn == bot_color`):

     * Call `ChessLogic.get_move(board, turn=bot_color)`.
     * Animate with `animate_move()`, then `board.push(move)`.
     * Clear `redo_stack`.
   * **Human’s Turn**:

     * Phase 1: Wait for **MOUSEBUTTONDOWN** → record `selected_square` and gather `legal_moves`.
     * Phase 2: Wait for **MOUSEBUTTONDOWN** → if clicked square is a legal destination:

       * If a pawn push to final rank → call `ask_promotion()`.
       * Animate, `board.push(move)`, clear `redo_stack`.
   * **Undo/Redo**:

     * **← (Left Arrow)** → call `undo()`:

       * Pop last two moves (if exist), animate each backwards, and push them onto `redo_stack`.
     * **→ (Right Arrow)** → call `redo()`:

       * Pop up to two moves from `redo_stack`, animate forwards, and push them onto `board`.
   * **Rendering**:

     * `renderer.draw_board()`, `renderer.draw_pieces(board)`, and if `selected` ≠ None, call `renderer.highlight({'moves': legal_moves})`.
     * `pygame.display.flip()`.

4. **Game-Over**

   * After each frame, call `check_for_gameover(board, screen, renderer, bot_color)`.
   * If the function returns `False`, break the loop and exit.

---

### AI Logic & Evaluation

#### Material + Positional Evaluation

* **Material**: Each piece has a base value in `PIECE_VALUES` (centipawns).
* **Piece-Square Tables**: `PIECE_SQUARE_TABLES` holds an 8×8 matrix for each piece type. White’s score is taken directly; Black’s is mirrored vertically.
* **Total evaluation**:

  ```python
  val = sum(material_sign * base_value for each piece)
  + sum(positional_sign * PST_value for each piece at its square)
  ```

  where `material_sign = +1` for White, `-1` for Black; similarly for positional.

#### Minimax with Alpha-Beta Pruning

* Method signature:

  ```python
  minimax(self, board, depth, alpha, beta, maximizing_player) -> (score, best_move)
  ```

* **Terminal Checks** (in order):

  1. `board.is_game_over()`:

     * If `is_checkmate()`: return `±∞` based on side to move.
     * Else (draw/stalemate): return `0`.
  2. `depth == 0`: return `evaluate_board(board)`.

* **Recursion**:

  * Generate all legal moves.
  * Order them via **MVV-LVA** (Most Valuable Victim – Least Valuable Aggressor):

    ```python
    moves.sort(key=lambda m: (board.is_capture(m), capture_score(board, m)), reverse=True)
    ```
  * If `maximizing_player`:

    * Initialize `best_score = -∞`.
    * For each move `m`:

      * `board.push(m)`
      * Recurse: `val, _ = minimax(board, depth-1, alpha, beta, False)`
      * `board.pop()`
      * If `val > best_score`: update `best_score` and `best_move`.
      * Update `alpha = max(alpha, best_score)`.
      * If `alpha >= beta`: break (beta-cut).
  * If minimizing: do the symmetric logic with `+∞`, `beta = min(beta, best_score)`, and alpha-cut.

* **Return**: `(best_score, best_move)` at the top of the recursion.

#### Move-Ordering Heuristics

* **MVV-LVA (Most Valuable Victim, Least Valuable Attacker)**:

  * `capture_score(board, move) = PIECE_VALUES[victim] * 100 – PIECE_VALUES[attacker]`
  * Puts captures first, prioritized by capturing the highest-value piece with the lowest-value attacker.

> *Optional Extensions (not fully implemented here):*
>
> * **Killer Moves**: store moves that caused beta-cutoffs to try them early at the same depth.
> * **History Heuristic**: track how often quiet moves cause cutoffs across all depths.

---

## Usage & Controls

1. **Launch**:

   ```bash
   python ui.py
   ```

2. **Choose Color**:

   * Press **W** to play White.
   * Press **B** to play Black.

3. **Make a Move** (when it’s your turn):

   * Click on a square containing your piece → legal moves highlight with yellow circles.
   * Click on a highlighted square → piece slides there (animated).
   * If a pawn reaches the final rank, press one of:

     * **Q** (Queen), **R** (Rook), **B** (Bishop), **K** (Knight).
     * Or click anywhere to cancel promotion (no move).

4. **Undo / Redo**:

   * **Undo** (Left Arrow) → Undoes both your last move and the bot’s reply (2 plies).
   * **Redo** (Right Arrow) → Replays undone moves (2 plies).

5. **Game Over**:

   * When checkmate or draw occurs, a centered message appears (white text on black background).
   * The message remains for 2 seconds, then the application exits.

---

## Customization & Configuration

* **Search Depth**:

  * By default, `ChessLogic(depth=3)` searches to depth 3 plies.
  * Increase to depth 4 or 5 for a stronger engine, but be aware of exponential time growth.

* **Time Control / Iterative Deepening**:

  * Not implemented, but you can modify `get_move(...)` to call `negamax` or `minimax` with increasing depths until a timer expires.

* **Piece-Square Tables**:

  * You can tweak `PIECE_SQUARE_TABLES` to adjust positional play (e.g., encourage central control, king safety).

* **GUI Appearance** (`constants.py`):

  * Change `WIDTH`, `HEIGHT`, or `COLORS` to customize board appearance.
  * Adjust `FPS` for smoother or faster animations.

---

## Troubleshooting & FAQs

* **Black Screen / No Pieces**

  * Ensure you have an `img/` folder in the same directory as `ui.py`, containing all PNG files named exactly as in `Renderer._load_images()`.
  * Check that `requirements.txt` is installed:

    ```bash
    pip install -r requirements.txt
    ```
* **Pygame Window Freezes on Animation**

  * Make sure event polling remains active inside `animate_move()`. If you remove the `for ev in pygame.event.get():` loop, Pygame will think the window is “Not Responding.”
* **Promotion Not Triggering**

  * Confirm that you click a pawn moving straight into the final rank (same file, one rank before).
  * Then press Q/R/B/K while the board is stationary—do not click again until you choose a piece.

---

## Contributing

1. **Fork** the repository and **clone** your fork locally.
2. Create a **new branch** for your feature/bugfix:

   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Install dependencies** and run tests (if any).
4. **Commit** your changes with clear messages.
5. **Push** to your fork and open a **Pull Request** against the `master` branch.
6. Include a brief description of your changes, any new dependencies, and what you tested.

We welcome enhancements such as: improved heuristics, GUI polish, time controls, UCI support, or modularizing the code further.
