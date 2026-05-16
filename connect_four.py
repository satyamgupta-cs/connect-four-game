import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLS = 7

EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2

CELL_SIZE = 90

BG_COLOR = "#1E1E2E"
BOARD_COLOR = "#3B82F6"
EMPTY_COLOR = "#E5E7EB"
PLAYER1_COLOR = "#EF4444"
PLAYER2_COLOR = "#FACC15"

# GAME CLASS

class ConnectFour:

    def __init__(self, root):

        self.root = root
        self.root.title("Connect Four")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.current_player = PLAYER_1

        # Create board
        self.board = [
            [EMPTY for _ in range(COLS)]
            for _ in range(ROWS)
        ]

        # Title
        title = tk.Label(
            root,
            text="CONNECT FOUR",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg="white"
        )
        title.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(
            root,
            text="Player 1 Turn (Red)",
            font=("Arial", 14),
            bg=BG_COLOR,
            fg="white"
        )
        self.status_label.pack()

        # Canvas
        canvas_width = COLS * CELL_SIZE
        canvas_height = ROWS * CELL_SIZE

        self.canvas = tk.Canvas(
            root,
            width=canvas_width,
            height=canvas_height,
            bg=BOARD_COLOR,
            highlightthickness=0
        )

        self.canvas.pack(padx=10, pady=10)

        # Mouse click event
        self.canvas.bind("<Button-1>", self.handle_click)

        # Restart Button
        restart_btn = tk.Button(
            root,
            text="Restart Game",
            font=("Arial", 12, "bold"),
            bg="#10B981",
            fg="white",
            padx=10,
            pady=5,
            command=self.restart_game
        )

        restart_btn.pack(pady=10)

        self.draw_board()

    # DRAW BOARD

    def draw_board(self):

        self.canvas.delete("all")

        for row in range(ROWS):
            for col in range(COLS):

                x1 = col * CELL_SIZE + 10
                y1 = row * CELL_SIZE + 10

                x2 = x1 + CELL_SIZE - 20
                y2 = y1 + CELL_SIZE - 20

                piece = self.board[row][col]

                color = EMPTY_COLOR

                if piece == PLAYER_1:
                    color = PLAYER1_COLOR

                elif piece == PLAYER_2:
                    color = PLAYER2_COLOR

                self.canvas.create_oval(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline=""
                )

    # HANDLE CLICK

    def handle_click(self, event):

        col = event.x // CELL_SIZE

        if col >= COLS:
            return

        row = self.get_open_row(col)

        if row is not None:

            self.board[row][col] = self.current_player

            self.draw_board()

            # Check winner
            if self.check_winner(self.current_player):

                winner = "Player 1 (Red)" if self.current_player == PLAYER_1 else "Player 2 (Yellow)"

                messagebox.showinfo(
                    "Game Over",
                    f"{winner} Wins!"
                )

                self.restart_game()
                return

            # Draw check
            if self.is_draw():
                messagebox.showinfo(
                    "Game Over",
                    "It's a Draw!"
                )

                self.restart_game()
                return

            # Switch player
            self.current_player = (
                PLAYER_2
                if self.current_player == PLAYER_1
                else PLAYER_1
            )

            self.update_status()

    # FIND EMPTY ROW
   
    def get_open_row(self, col):

        for row in range(ROWS - 1, -1, -1):

            if self.board[row][col] == EMPTY:
                return row

        return None

    # UPDATE STATUS
  
    def update_status(self):

        if self.current_player == PLAYER_1:
            text = "Player 1 Turn (Red)"
        else:
            text = "Player 2 Turn (Yellow)"

        self.status_label.config(text=text)

    # CHECK DRAW
   
    def is_draw(self):

        for col in range(COLS):

            if self.board[0][col] == EMPTY:
                return False

        return True

    # CHECK WINNER

    def check_winner(self, player):

        # Horizontal
        for row in range(ROWS):
            for col in range(COLS - 3):

                if all(
                    self.board[row][col + i] == player
                    for i in range(4)
                ):
                    return True

        # Vertical
        for row in range(ROWS - 3):
            for col in range(COLS):

                if all(
                    self.board[row + i][col] == player
                    for i in range(4)
                ):
                    return True

        # Diagonal \
        for row in range(ROWS - 3):
            for col in range(COLS - 3):

                if all(
                    self.board[row + i][col + i] == player
                    for i in range(4)
                ):
                    return True

        # Diagonal /
        for row in range(3, ROWS):
            for col in range(COLS - 3):

                if all(
                    self.board[row - i][col + i] == player
                    for i in range(4)
                ):
                    return True

        return False

    # RESTART GAME

    def restart_game(self):

        self.board = [
            [EMPTY for _ in range(COLS)]
            for _ in range(ROWS)
        ]

        self.current_player = PLAYER_1

        self.update_status()

        self.draw_board()

# MAIN

if __name__ == "__main__":

    root = tk.Tk()

    game = ConnectFour(root)

    root.mainloop()
