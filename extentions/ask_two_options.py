import tkinter as tk
from tkinter import ttk

try:
    from custom_widgets import Tooltip
except ModuleNotFoundError:
    from extentions.custom_widgets import Tooltip


def ttk_ask_two_options(question_text: str, button1_text: str, button2_text: str, question_font=..., alone=False,
                        b1_tooltip_text='', b2_tooltip_text='', parent: tk.Misc | None = None):
    win = tk.Toplevel(parent) if not alone else tk.Tk()
    win.wm_overrideredirect(True)

    answer = tk.IntVar(win)

    def set_int(val: int):
        answer.set(val)
        win.quit()

    b_frame = tk.LabelFrame(win, labelanchor=tk.N, labelwidget=tk.Label(win, text=question_text, font=question_font))
    btns_frame = tk.Frame(b_frame)
    option_1 = ttk.Button(btns_frame, text=button1_text, command=lambda: set_int(0))
    option_1.grid(column=0, row=0, ipadx=3, ipady=2)
    if b1_tooltip_text != '':
        Tooltip(option_1, b1_tooltip_text)
    option_2 = ttk.Button(btns_frame, text=button2_text, command=lambda: set_int(1))
    option_2.grid(column=1, row=0, ipadx=3, ipady=2)
    if b2_tooltip_text != '':
        Tooltip(option_2, b2_tooltip_text)
    btns_frame.pack(anchor=tk.CENTER)
    b_frame.pack()

    win.update_idletasks()
    win.geometry(f'+{int((win.winfo_screenwidth() / 2) - (win.winfo_width() / 2))}'
                 f'+{int((win.winfo_screenheight() / 2) - (win.winfo_height() / 2))}')
    win.mainloop()
    win.destroy()
    return answer.get()
