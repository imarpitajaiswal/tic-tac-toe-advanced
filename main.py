import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import pickle

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Pro")
        
        # Game State
        self.player1_name = simpledialog.askstring("Input", "Enter Player 1 (X) Name:") or "Player 1"
        self.player2_name = simpledialog.askstring("Input", "Enter Player 2 (O) Name:") or "Player 2"
        self.scores = {"player1": 0, "player2": 0}
        self.load_scores()
        
        self.current_player = "X"
        self.buttons = []
        
        # GUI Setup
        self.score_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.score_label.grid(row=0, column=0, columnspan=3, pady=10)
        self.update_score_display()
        
        for i in range(9):
            btn = tk.Button(root, text="", font=("Helvetica", 24), width=5, height=2,
                            command=lambda idx=i: self.button_click(idx))
            btn.grid(row=1 + i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)
            
        tk.Button(root, text="Restart Game", command=self.reset_board).grid(row=4, column=0, columnspan=3, pady=10)

    def load_scores(self):
        if os.path.exists("scores.pkl"):
            with open("scores.pkl", "rb") as f:
                self.scores = pickle.load(f)

    def save_scores(self):
        with open("scores.pkl", "wb") as f:
            pickle.dump(self.scores, f)

    def update_score_display(self):
        self.score_label.config(text=f"{self.player1_name}: {self.scores['player1']} | {self.player2_name}: {self.scores['player2']}")

    def reset_board(self):
        self.current_player = "X"
        for btn in self.buttons:
            btn.config(text="", bg="SystemButtonFace")

    def check_winner(self):
        wins = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        for c in wins:
            if self.buttons[c[0]]["text"] == self.buttons[c[1]]["text"] == self.buttons[c[2]]["text"] != "":
                winner_text = self.buttons[c[0]]["text"]
                self.scores['player1' if winner_text == "X" else 'player2'] += 1
                self.save_scores()
                self.update_score_display()
                messagebox.showinfo("Result", f"Winner: {'Player 1' if winner_text == 'X' else 'Player 2'}")
                self.reset_board()
                return
        if all(btn["text"] != "" for btn in self.buttons):
            messagebox.showinfo("Result", "It's a tie!")
            self.reset_board()

    def button_click(self, idx):
        if self.buttons[idx]["text"] == "":
            self.buttons[idx]["text"] = self.current_player
            self.check_winner()
            self.current_player = "O" if self.current_player == "X" else "X"

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()
