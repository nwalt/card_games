import random
import tkinter
import asyncio
import threading
from tkinter import ttk
from threading import Lock

from PIL.ImageTk import PhotoImage

from src.ui import GameUI
from src.game.solitaire import SolitaireGame, SolitaireLoop

class SolitaireUI(GameUI):

    name = 'Solitaire'
    WIDTH = 700
    HEIGHT = 600
    # TODO: position out mathematically instead of hardcoding. Too tired now
    initial_tableau_positions = [
        [(10,10), (10+76,10), (10+76*2, 10), (10+76*3, 10), (10+76*4, 10), (10+76*5, 10), (10+76*6, 10)],
        [(10+76, 10+15), (10+76*2, 10+15), (10+76*3, 10+15), (10+76*4, 10+15), (10+76*5, 10+15), (10+76*6, 10+15)],
        [(10+76*2, 10+15*2), (10+76*3, 10+15*2), (10+76*4, 10+15*2), (10+76*5, 10+15*2), (10+76*6, 10+15*2),],
        [(10+76*3, 10+15*3), (10+76*4, 10+15*3), (10+76*5, 10+15*3), (10+76*6, 10+15*3),],
        [(10+76*4, 10+15*4), (10+76*5, 10+15*4), (10+76*6, 10+15*4),],
        [(10+76*5, 10+15*5), (10+76*6, 10+15*5),],
        [(10+76*6, 10+15*6),]
    ]
    initial_tableau_cards = 28


    def __init__(self, root, game_select_frame):
        super().__init__(root, game_select_frame)

        self.canvas = tkinter.Canvas(self, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.grid(row=0, column=0, sticky='nwes')
        button_frame = ttk.Frame(self)
        button_frame.grid(row=0, column=1)
        ttk.Button(button_frame, text='Reset', command=self.reset_card_positions).grid(row=0, column=0)
        ttk.Button(
            button_frame, text='End Game', command=self.exit
        ).grid(row=1, column=0)
        # initialize game state
        self.game_lock = Lock()
        self.game_state = SolitaireGame()
        # TODO: move .cards and .card_lookup into game state?
        self.cards = {}
        self.card_lookup = {}
        # Draw lil boxes for the scoring zones, draw zone, and discard zone
        self.canvas.create_rectangle(10, self.HEIGHT-120, 86, self.HEIGHT-20)
        self.canvas.create_rectangle(10+86, self.HEIGHT-120, 86+86, self.HEIGHT-20)
        self.canvas.create_rectangle(10+86*2, self.HEIGHT-120, 86+86*2, self.HEIGHT-20)
        self.canvas.create_rectangle(10+86*3, self.HEIGHT-120, 86+86*3, self.HEIGHT-20)
        self.canvas.create_rectangle(
            self.WIDTH-81, self.HEIGHT-120, self.WIDTH-5, self.HEIGHT-20
        )
        self.canvas.create_rectangle(
            self.WIDTH-81, self.HEIGHT-220, self.WIDTH-5, self.HEIGHT-120
        )
        # TODO: draw suit symbols in the scoring zones?
        for card in self.game_state.deck.cards:
            card_item = self.canvas.create_image(
                self.WIDTH-76, self.HEIGHT-110, image=self.card_sprite_images_tk['BLUE_BACK'], anchor='nw', tags=('card')
            )
            self.cards[card.name] = {
                'x':self.WIDTH-76, 'y':self.HEIGHT-110, 'canvas_item':card_item, 'card_name':card.name, 'img':'BLUE_BACK'
            }
            self.card_lookup[card_item] = card.name
        self.reset_card_positions(first_deal=True)
        # tk and asyncio CANNOT exist in the same thread
        # so we create an event loop, and send it to another thread to start
        self.async_loop = asyncio.new_event_loop()
        self.game_loop = SolitaireLoop(
            tk_root=root, loop=self.async_loop, game=self.game_state, game_lock=self.game_lock,
        )
        self.game_loop_thread = threading.Thread(
            name='solitaire_game_loop_thread', target=self.game_loop.main,
            # daemon threads are killed ungracefully on main thread exit.
            # Make sure they get cleaned up nicely instead
            daemon=True
        )
        self.game_loop_thread.start()
        # asyncio thread can only send events to root, so all binds that react to 
        # network or game loop activity must bind to root
        # root.bind('<<UpdateDisplay>>', self.draw_game)
        self.canvas.tag_bind('card', '<ButtonPress-1>', self.drag_start)
        self.canvas.tag_bind('card', '<ButtonRelease-1>', self.drag_stop)
        self.canvas.tag_bind('card', '<B1-Motion>', self.drag)
        self.canvas.tag_bind('card', '<ButtonPress-3>', self.flip)

    def draw_game(self, *args):
        # self.canvas.update()
        pass
    
    def reset_card_positions(self, first_deal=False):
        if not first_deal:
            self.game_state.deck.shuffle()
            for c in self.cards:
                self.canvas.itemconfig(
                    self.cards[c]['canvas_item'], image=self.card_sprite_images_tk['BLUE_BACK']
                )
                self.cards[c]['img'] = 'BLUE_BACK'
                self.canvas.moveto(self.cards[c]['canvas_item'], self.WIDTH-76, self.HEIGHT-110)
        i = 0
        target_card = self.cards[self.game_state.deck.cards[i].name]
        for row in self.initial_tableau_positions:
            self.canvas.itemconfig(target_card['canvas_item'], image=self.card_sprite_images_tk[target_card['card_name']])
            for position in row:
                x, y = position
                self.canvas.moveto(target_card['canvas_item'], x, y)
                self.canvas.tag_raise(target_card['canvas_item'])
                i += 1
                target_card = self.cards[self.game_state.deck.cards[i].name]

    def flip(self, event):
        target_item = self.canvas.find_closest(event.x, event.y)[0]
        card_name = self.card_lookup[target_item]
        target_card = self.cards[card_name]
        if target_card['img'] == 'BLUE_BACK':
            self.canvas.itemconfig(target_item, image=self.card_sprite_images_tk[card_name])
            target_card['img'] = card_name
        else:
            self.canvas.itemconfig(target_item, image=self.card_sprite_images_tk['BLUE_BACK'])
            target_card['img'] = 'BLUE_BACK'