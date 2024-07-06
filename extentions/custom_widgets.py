import tkinter as tk


class ChessBtn(tk.Button):
    def __init__(self, img, **kwargs):
        super().__init__(**kwargs)
        self.img = img
