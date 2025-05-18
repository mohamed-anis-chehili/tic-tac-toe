import tkinter as tk
from tkinter import messagebox
import copy

class TicTacToe:
    def __init__(self):
        # Game setup
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe with Minimax AI")
        
        # Game state
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.human = "X"
        self.computer = "O"
        self.current_player = self.human
        self.game_over = False
        
        # Create UI elements
        self.create_widgets()
    
    def create_widgets(self):
        # Status label
        self.status_label = tk.Label(
            self.window, 
            text=f"Your turn ({self.human})", 
            font=("Arial", 16)
        )
        self.status_label.pack(pady=10)
        
        # Game board
        self.frame = tk.Frame(self.window)
        self.frame.pack(padx=10, pady=10)
        
        # Create buttons
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.frame, 
                    text="",
                    font=("Arial", 24),
                    width=5, 
                    height=2,
                    command=lambda r=i, c=j: self.on_click(r, c)
                )
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)
        
        # Reset button
        self.reset_button = tk.Button(
            self.window,
            text="New Game",
            font=("Arial", 12),
            command=self.reset_game
        )
        self.reset_button.pack(pady=10)
    
    def reset_game(self):
        # Reset game state
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = self.human
        self.game_over = False
        
        # Reset UI
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL)
        
        self.status_label.config(text=f"Your turn ({self.human})")
    
    def on_click(self, row, col):
        # Ignore clicks if game is over or cell is already filled
        if self.game_over or self.board[row][col] != "":
            return
        
        # Update board and UI
        self.make_move(row, col, self.human)
        
        # Check for game end conditions
        if self.check_winner_for_player(self.board, self.human):
            self.status_label.config(text=f"You win!")
            self.game_over = True
            return
        
        if self.is_board_full():
            self.status_label.config(text="It's a draw!")
            self.game_over = True
            return
        
        # Computer's turn
        self.status_label.config(text=f"Computer's turn ({self.computer})...")
        self.window.update()
        
        # Add a small delay to make computer's move visible
        self.window.after(500, self.computer_move)
    
    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col].config(text=player, state=tk.DISABLED)
        self.current_player = self.computer if player == self.human else self.human
    
    def computer_move(self):
        if self.game_over:
            return
            
        # Find the best move using minimax algorithm
        best_score = float("-inf")
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = self.computer
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ""
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        if best_move:
            row, col = best_move
            self.make_move(row, col, self.computer)
            
            if self.check_winner_for_player(self.board, self.computer):
                self.status_label.config(text="Computer wins!")
                self.game_over = True
                return
                
            if self.is_board_full():
                self.status_label.config(text="It's a draw!")
                self.game_over = True
                return
            
            self.status_label.config(text=f"Your turn ({self.human})")
    
    def minimax(self, board, depth, is_maximizing):
        # Check for terminal states
        if self.check_winner_for_player(board, self.computer):
            return 10 - depth
        elif self.check_winner_for_player(board, self.human):
            return depth - 10
        elif self.is_board_full_static(board):
            return 0
        
        if is_maximizing:
            # Computer's turn (maximizing)
            best_score = float("-inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.computer
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            # Human's turn (minimizing)
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.human
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score
    
    def check_winner(self):
        return self.check_winner_for_player(self.board, self.current_player)
    
    def check_winner_for_player(self, board, player):
        # Check rows
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] == player:
                return True
        
        # Check columns
        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] == player:
                return True
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        
        return False
    
    def is_board_full(self):
        return self.is_board_full_static(self.board)
    
    def is_board_full_static(self, board):
        for row in board:
            for cell in row:
                if cell == "":
                    return False
        return True
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
