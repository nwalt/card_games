import tkinter as tk
from tkinter import ttk
from functools import partial

from src.ui.blackjack import BlackJackUI

class GameSelectFrame(ttk.Frame):
    GAMES = [
        BlackJackUI
    ]

    def __init__(self, root):
        super().__init__(
            root,
        )
        self.grid(row=0, column=0)
        for i, game in enumerate(self.GAMES):
            # game_open = partial()
            but = ttk.Button(
                self, text=game.name, 
                command=lambda: [self.grid_remove(), game(root, self)])
            but.grid(column=i, row=0)

if __name__ == '__main__':
    root = tk.Tk()
    GameSelectFrame(root)
    root.mainloop()