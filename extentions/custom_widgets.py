import tkinter as tk


class ChessBtn(tk.Button):
    def __init__(self, img, **kwargs):
        super().__init__(**kwargs)
        self.img = img


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.tooltip_text = text
        self.tooltip_window = None

        self.widget.bind("<Enter>", self.show_tooltip, add='+')
        self.widget.bind("<Leave>", self.hide_tooltip, add='+')
        self.widget.bind("<Motion>", self.move_tooltip, add='+')

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += event.x_root + 12
        y += event.y_root + 12

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.attributes('-topmost', True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        tooltip_label = tk.Label(
            self.tooltip_window, borderwidth=1, background="#FFFFDD", relief="solid",
            text=self.tooltip_text if isinstance(self.tooltip_text, str) else self.tooltip_text.get())
        tooltip_label.pack(ipady=1, ipadx=2)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def move_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += event.x_root + 12
        y += event.y_root + 12

        try:
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
        except AttributeError:
            self.hide_tooltip()
