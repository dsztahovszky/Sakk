import tkinter as tk
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
from extentions.custom_widgets import ChessBtn, Tooltip
from extentions.ttk_ask import ttk_ask_two_options, ttk_ask_str, Message

from extentions.communication.chess_server import ChessServer
import socket
import requests

from threading import Thread
from time import sleep
from sys import exit

from typing import Literal


def get_internal_ip():
    hostname = socket.gethostname()
    internal_ip = socket.gethostbyname(hostname)
    return internal_ip


def get_external_ip():
    response = requests.get('https://api.ipify.org')
    external_ip = response.text
    return external_ip


class OnlineChessWindow(tk.Tk):
    def __init__(self):
        self.IMGS_PATH = r'.\img\pieces'
        self.server: ChessServer | None = None
        self.mode: Literal["server", "client"] = 'server' if ttk_ask_two_options('Válassz módot:', 'Szerver', 'Kliens',
                                                                                 ('Calibri', 20),
                                                                                 b1_tooltip_text='Profil, melyhez egy '
                                                                                                 'másik játékos '
                                                                                                 'csatlakozhat (csak '
                                                                                                 'a szerver '
                                                                                                 'választhat színt)',
                                                                                 b2_tooltip_text='Profil, mely képes '
                                                                                                 'másokhoz '
                                                                                                 'csatlakozni') == 0 \
            else 'client'
        if self.mode == "server":
            self.color: Literal["white", "black"] = 'white' if ttk_ask_two_options('Válassz színt:', 'Fehér', 'Fekete',
                                                                                   ('Calibri', 20)) == 0 else 'black'
        else:
            self.connect_to = ttk_ask_str('Add meg a gép IP-címét, amelyhez csatlakozni szeretnél:', ('Calibri', 20),
                                          input_placeholder_text='Ide írd az IP-címet')
            self.server = ChessServer("client")
            try:
                self.server.connect_to_server(self.connect_to, 12345)
            except Exception as ex:
                showerror('Hiba a csatlakozás közben', str(ex))
                exit()

            def get_color():
                self.color = self.server.receive().split()[1]

            get_color_thread = Thread(target=get_color)
            get_color_thread.start()

            # msg = Message(f'Csatlakozás ehhez: {self.connect_to}', ('Calibri', 20))
            # sleep(1)
            # msg.close()
            # exit()
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
        self.title('Online Sakk')
        self.geometry('1158x608+180+80')
        self.iconbitmap(default='./img/logo.ico')
        self.protocol("WM_DELETE_WINDOW", self.close)
        # self.protocol('WM_DELETE_WINDOW', self.close)
        self.letters = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
        self.color_lbl_var = tk.StringVar(self, f'Saját szín: {"fehér" if self.color == "white" else "fekete"}')

        self.next: Literal["white", "black"] = 'white'
        self.next_lbl_var = tk.StringVar(self, 'Következő játékos: fehér')

        self.board = tk.Frame(self)  # 400x400  # , width=400, height=400
        self.board.grid(column=0, row=0)
        self.others_frame = tk.Frame(self)
        self.others_frame.grid(column=1, row=0, sticky=tk.NW, padx=20)
        self.color_lbl = tk.Label(self.others_frame, textvariable=self.color_lbl_var, font=('Arial', 20))
        self.color_lbl.grid(column=0, row=0, sticky=tk.NW, pady=17)
        self.next_lbl = tk.Label(self.others_frame, textvariable=self.next_lbl_var, font=('Arial', 25))
        self.next_lbl.grid(column=0, row=1, sticky=tk.NW, pady=17)

        if self.mode == 'server':
            self.ip_frame = tk.Frame(self.others_frame)
            self.ip_frame.grid(column=0, row=2, sticky=tk.NW, pady=17)
            self.ip_info_frame = tk.Frame(self.ip_frame)
            self.ip_info_frame.grid(column=0, row=0)

            self.internal_ip = get_internal_ip()
            self.internal_ip_lbl = tk.Label(self.ip_info_frame, text=f'Belső IP-cím: {self.internal_ip}',
                                            font=('Times New Roman', 12))
            Tooltip(self.internal_ip_lbl, 'Ha a két fél ugyanahhoz a hálózathoz csatlakozik, akkor ezt küldje el '
                                          'ellenfelének')
            self.internal_ip_lbl.grid(column=0, row=0, sticky=tk.NW)

            self.external_ip = get_external_ip()
            self.external_ip_lbl = tk.Label(self.ip_info_frame, text=f'Külső IP-cím: {self.external_ip}',
                                            font=('Times New Roman', 12))
            Tooltip(self.external_ip_lbl, 'Ha a két fél két különböző hálózathoz csatlakozik, akkor ezt küldje el '
                                          'ellenfelének')
            self.external_ip_lbl.grid(column=0, row=1, sticky=tk.NW, pady=(5, 0), padx=(0, 20))

            self.copy_internal_ip = tk.Button(self.ip_info_frame, text='Belső IP-cím másolása',
                                              command=lambda: self.add_to_clipboard(self.internal_ip))
            self.copy_internal_ip.grid(column=1, row=0, sticky=tk.E)
            self.copy_external_ip = tk.Button(self.ip_info_frame, text='Külső IP-cím másolása',
                                              command=lambda: self.add_to_clipboard(self.external_ip))
            self.copy_external_ip.grid(column=1, row=1, sticky=tk.E)

            self.ip_info_lbl = tk.Label(self.ip_frame, text='Az IP-címe segítségével tudnak mások Önhöz csatlakozni.')
            self.ip_info_lbl.grid(column=0, row=1, sticky=tk.W, pady=10)

            self.server_state_var = tk.StringVar(self, 'Szerver indítása..')
            self.server_state_lbl = tk.Label(self.others_frame, textvariable=self.server_state_var)
            self.server_state_lbl.grid(column=0, row=3, sticky=tk.W)
            self.stop_server_btn = tk.Button(self.others_frame, text='Szerver leállítása')
            self.stop_server_btn.grid(column=1, row=3)
            self.update()

            self.server_thread: Thread | None = None
            self.start_server()

        else:
            pass

        self.focus_force()

    def add_to_clipboard(self, string):
        self.clipboard_clear()
        self.clipboard_append(string)

    def start_server(self):
        def start():
            self.server = ChessServer('server', '0.0.0.0', 12345)
            self.server_state_var.set('A szerver elindult.')
            self.stop_server_btn.config(command=self.stop_server)
            connected_addr = self.server.wait_for_connection()
            if connected_addr is not None:
                self.server_state_var.set(f'Csatlakozva a következőhöz: {connected_addr}')
                self.server.send_message(f'you: {"black" if self.color == "white" else "white"}')

        self.server_thread = Thread(target=start, daemon=True)
        self.server_thread.start()

    def stop_server(self):
        def start():
            self.server_state_var.set('Szerver indítása..')
            self.stop_server_btn.config(text='Szerver leállítása')
            self.update()
            self.start_server()

        self.server.close_server()
        self.server_state_var.set('Szerver leállítva.')
        self.stop_server_btn.config(text='Szerver újraindítása', command=start)

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
                                       'Bezárom az alkalmazást', ('Arial', 15), parent=self) == 0:
                    self.destroy()
                    ChessWindow.prev_widget = None
                    del self
                    main()
                else:
                    self.close()
        print(event.widget.img)

    def close(self):
        self.server.close_server()
        self.update_idletasks()
        for i in range(1, 101):
            self.attributes('-alpha', (100 - i) / 100)
            sleep(0.01)
        self.destroy()


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
        self.others_frame = tk.Frame(self)
        self.others_frame.grid(column=1, row=0, sticky=tk.NW)
        self.next_lbl = tk.Label(self.others_frame, textvariable=self.next_lbl_var, font=('Arial', 25))
        self.next_lbl.grid(column=0, row=0, sticky=tk.NW, padx=20, pady=17)

        self.onlineplayer_btn = tk.Button(self.others_frame, text='Online játék távoli ellenféllel',
                                          font=('Calibri', 15), bg='lightyellow', activebackground='yellow',
                                          command=self.switch_to_online)
        self.onlineplayer_btn.grid(column=0, row=1, pady=100, ipadx=10, ipady=7)

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
                                       'Bezárom az alkalmazást', ('Arial', 15), parent=self) == 0:
                    self.destroy()
                    ChessWindow.prev_widget = None
                    del self
                    main()
                else:
                    self.close()
        print(event.widget.img)

    def switch_to_online(self):
        self.destroy()
        app = OnlineChessWindow()
        app.mainloop()

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
