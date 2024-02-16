import tkinter as tk
from tkinter import ttk

from src.ui.solitaire import SolitaireUI
from src.ui.blackjack import BlackJackUI

class GameSelectFrame(ttk.Frame):

    def __init__(self, root):
        super().__init__(
            root,
        )
        self.grid(row=0, column=0)
        ttk.Button(
            self, text=SolitaireUI.name, 
            command=lambda: [self.grid_remove(), SolitaireUI(root, self)]
        ).grid(row=0, column=0)
        ttk.Button(
            self, text=BlackJackUI.name, 
            command=lambda: [self.grid_remove(), BlackJackUI(root, self)]
        ).grid(row=0, column=1)


if __name__ == '__main__':
    root = tk.Tk()
    GameSelectFrame(root)
    root.mainloop()