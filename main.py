import tkinter as tk
from PIL import Image, ImageTk
from extentions.custom_widgets import ChessBtn
from extentions.ask_two_options import ttk_ask_two_options

from time import sleep

from typing import Literal


class ChessWindow(tk.Tk):
    def __init__(self):
        self.IMGS_PATH = r'.\img\pieces'
        super().__init__()
        self.imgs = {
            'white': {
                'back': {
                    'left rock': ImageTk.PhotoImage(Image.open(r'.\img\pieces\white\left_rock.png')),
                    'left knight': ImageTk.PhotoImage(Image.open(fr'{self.IMGS_PATH}\white\left_knight.png')),
                    'left bishop': ImageTk.PhotoImage(Image.open(fr'{self.IMGS_PATH}\white\left_bishop.png')),
                    'queen': ImageTk.PhotoImage(Image.open(fr'{self.IMGS_PATH}\white\queen.png')),
                    'king': ImageTk.PhotoImage(Image.open(fr'{self.IMGS_PATH}\white\king.png')),
                    'right bishop': ImageTk.PhotoImage(Image.open(fr'{self.IMGS_PATH}\white\right_bishop.png')),
                    'right knight': ImageTk.PhotoImage(Image.open(fr'{self.IMGS_PATH}\white\right_knight.png')),
                    'right rock': ImageTk.PhotoImage(Image.open(fr'{self.IMGS_PATH}\white\right_rock.png'))
                },
                'fore': {
                    'left pawn': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/white/left_pawn.png')),
                    'right pawn': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/white/right_pawn.png'))
                }
            },
            'black': {
                'back': {
                    'left rock': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/black/left_rock.png')),
                    'left knight': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/black/left_knight.png')),
                    'left bishop': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/black/left_bishop.png')),
                    'queen': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/black/queen.png')),
                    'king': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/black/king.png')),
                    'right bishop': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/black/right_bishop.png')),
                    'right knight': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/black/right_knight.png')),
                    'right rock': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/black/right_rock.png'))
                },
                'fore': {
                    'left pawn': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/black/left_pawn.png')),
                    'right pawn': ImageTk.PhotoImage(Image.open(f'{self.IMGS_PATH}/black/right_pawn.png'))
                }
            },
            'empty': ImageTk.PhotoImage(Image.open('./img/empty.png'))
        }
        self.title('Sakk')
        self.geometry('1158x608+180+80')
        self.iconbitmap(default='./img/logo.ico')
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.letters = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
        self.next: Literal["white", "black"] = 'white'
        self.next_lbl_var = tk.StringVar(self, 'Következő játékos: fehér')

        self.board = tk.Frame(self)  # 400x400  # , width=400, height=400
        self.board.grid(column=0, row=0)
        self.next_lbl = tk.Label(self, textvariable=self.next_lbl_var, font=('Arial', 25))
        self.next_lbl.grid(column=1, row=0, sticky=tk.NW, padx=20, pady=17)

        self.row_frames = []  # 400x50
        self.btns = []
        self.generate_btns()
        self.focus_force()

    def generate_btns(self):
        """Generates the buttons and places them on the board"""
        for y in range(8):
            self.row_frames.append(tk.Frame(self.board))  # , width=400, height=50
            self.row_frames[y].grid(column=0, row=y)
            btns_row = {}
            for x in range(8):
                btns_row[self.letters[x]] = ChessBtn('empty', master=self.row_frames[y], image=self.imgs['empty'])
                btns_row[self.letters[x]].bind('<B1-ButtonRelease>', self.select_btn)
                # 50x50  , width=7, height=3
                if ((y % 2 == 0) and (x % 2 == 0)) or ((y % 2 != 0) and (x % 2 != 0)):
                    btns_row[self.letters[x]].config(bg='lightgrey', activebackground='#2a2a2a')
                else:
                    btns_row[self.letters[x]].config(bg='#2a2a2a', activebackground='lightgrey')
                btns_row[self.letters[x]].grid(column=x, row=y)
            self.btns.append(btns_row)

        standard = [
            # 1-es sor
            {'coords': (0, 'h'), 'img': self.imgs['white']['back']['left rock'], 'id': 'white left rock'},
            {'coords': (0, 'g'), 'img': self.imgs['white']['back']['left knight'], 'id': 'white left knight'},
            {'coords': (0, 'f'), 'img': self.imgs['white']['back']['left bishop'], 'id': 'white left bishop'},
            {'coords': (0, 'e'), 'img': self.imgs['white']['back']['queen'], 'id': 'white queen'},
            {'coords': (0, 'd'), 'img': self.imgs['white']['back']['king'], 'id': 'white king'},
            {'coords': (0, 'c'), 'img': self.imgs['white']['back']['right bishop'], 'id': 'white right bishop'},
            {'coords': (0, 'b'), 'img': self.imgs['white']['back']['right knight'], 'id': 'white right knight'},
            {'coords': (0, 'a'), 'img': self.imgs['white']['back']['right rock'], 'id': 'white right rock'},
            # 2-es sor
            '4 left white pawn',
            '4 right white pawn',
            # 7-es sor
            '4 left black pawn',
            '4 right black pawn',
            # 8-as sor
            {'coords': (7, 'h'), 'img': self.imgs['black']['back']['left rock'], 'id': 'black left rock'},
            {'coords': (7, 'g'), 'img': self.imgs['black']['back']['left knight'], 'id': 'black left knight'},
            {'coords': (7, 'f'), 'img': self.imgs['black']['back']['left bishop'], 'id': 'black left bishop'},
            {'coords': (7, 'e'), 'img': self.imgs['black']['back']['queen'], 'id': 'black queen'},
            {'coords': (7, 'd'), 'img': self.imgs['black']['back']['king'], 'id': 'black king'},
            {'coords': (7, 'c'), 'img': self.imgs['black']['back']['right bishop'], 'id': 'black right bishop'},
            {'coords': (7, 'b'), 'img': self.imgs['black']['back']['right knight'], 'id': 'black right knight'},
            {'coords': (7, 'a'), 'img': self.imgs['black']['back']['right rock'], 'id': 'black right rock'}
        ]
        for d in standard:
            if isinstance(d, dict):
                self.btns[d['coords'][0]][d['coords'][1]].config(compound=tk.BOTTOM, image=d['img'])
                self.btns[d['coords'][0]][d['coords'][1]].img = d['id']
            else:
                words = d.split()
                btns_i = 1 if words[2] == 'white' else 6
                if words[1] == 'left':
                    for i in range(int(words[0])):
                        self.btns[btns_i][self.letters[i]].config(
                            image=self.imgs[words[2]]['fore'][' '.join([words[1], words[3]])])
                        self.btns[btns_i][self.letters[i]].img = f'{words[2]} left pawn'
                else:
                    for i in range(int(words[0]), 0, -1):
                        self.btns[btns_i][self.letters[-i]].config(
                            image=self.imgs[words[2]]['fore'][' '.join([words[1], words[3]])])
                        self.btns[btns_i][self.letters[-i]].img = f'{words[2]} right pawn'

    prev_widget = None

    def select_btn(self, event):
        if (ChessWindow.prev_widget is not None) and (
                ChessWindow.prev_widget.img.split()[0] == event.widget.img.split()[0]):
            ChessWindow.prev_widget["state"] = tk.NORMAL
        if ((self.next == 'white') and ('white' in event.widget.img)) or (
                (self.next == 'black') and ('black' in event.widget.img)):
            event.widget["state"] = tk.DISABLED
            ChessWindow.prev_widget = event.widget
        elif (ChessWindow.prev_widget is not None) and (ChessWindow.prev_widget.img != 'empty'):
            if 'king' not in event.widget.img:
                prev_w_img = ChessWindow.prev_widget.img.split(maxsplit=1)
                event.widget.config(
                    image=self.imgs[prev_w_img[0]]['fore' if 'pawn' in prev_w_img[1] else 'back'][prev_w_img[1]])
                event.widget.img = ChessWindow.prev_widget.img

                ChessWindow.prev_widget.config(image=self.imgs['empty'])
                ChessWindow.prev_widget.img = 'empty'
                ChessWindow.prev_widget['state'] = tk.NORMAL
                if self.next == 'white':
                    self.next = 'black'
                    self.next_lbl_var.set('Következő játékos: fekete')
                else:
                    self.next = 'white'
                    self.next_lbl_var.set('Következő játékos: fehér')
            else:
                event.widget.config(activebackground='red', bg='red')
                if ttk_ask_two_options(f'Nyert a {self.next_lbl_var.get().split()[2]} játékos.\nKérsz új játékot? '
                                       f'Ha nem, akkor bezárjuk az alkalmazást.', 'Kérek új játékot!',
                                       'Bezárom az alkalmazást', ('Arial', 15), self) == 0:
                    self.destroy()
                    ChessWindow.prev_widget = None
                    del self
                    main()
                else:
                    self.close()
        print(event.widget.img)

    def close(self):
        self.update_idletasks()
        for i in range(1, 101):
            self.attributes('-alpha', (100 - i) / 100)
            sleep(0.01)
        self.destroy()


def main():
    app = ChessWindow()
    app.mainloop()
    # del app


main()
