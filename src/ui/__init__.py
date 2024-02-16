import random
import asyncio
import threading
from tkinter import ttk
from threading import Lock

from PIL import Image
from PIL.ImageTk import PhotoImage

class GameUI(ttk.Frame):

    name = 'Game UI Base Class'

    CARD_SPRITE_MATRIX = [
        ['RED_BACK', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH'],
        ['BLUE_BACK', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC'],
        ['JOKER_1', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD'],
        ['JOKER_2', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS'],
    ]

    def __init__(self, root, game_select_frame):
        super().__init__(root)
        self._drag_data = {'x': 0, 'y': 0, 'item': None}
        self.card_sprite_images = {}
        self.card_sprite_images_tk = {}
        card_sprites = Image.open('src/assets/8BitDeckAssets.png')
        x, y = 1, 1
        x2 = 34
        y2 = 46
        for row in self.CARD_SPRITE_MATRIX:
            for card in row:
                self.card_sprite_images[card] = card_sprites.crop(
                    (x, y, x2, y2)).resize((66, 90), resample=Image.Resampling.BOX)
                self.card_sprite_images_tk[card] = PhotoImage(
                    self.card_sprite_images[card])
                x += 35; x2 += 35
            x = 1; x2 = 34
            y += 47; y2 += 47
        
        self.root = root
        self.game_select_frame = game_select_frame
        self.grid(row=0, column=0)
        # these will be fully initialized in the actual game ui classes
        # just placeholders so we can define exit
        self.game_loop = None
        self.async_loop = None

    # These three functions enable dragging items around a canvas, if:
    # - there is a canvas in the frame
    # - the frame has a _drag_data
    def drag_start(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        self._drag_data['item'] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def drag_stop(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data['item'] = None
        self._drag_data['x'] = 0
        self._drag_data['y'] = 0

    def drag(self, event):
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data['x']
        delta_y = event.y - self._drag_data['y']
        # move the object the appropriate amount
        self.canvas.move(self._drag_data['item'], delta_x, delta_y)
        self.canvas.tag_raise(self._drag_data['item'])
        # record the new position
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def exit(self):
        #self.async_loop.call_soon_threadsafe(self.game_loop.set_stop_event)
        stop_future = asyncio.run_coroutine_threadsafe(self.game_loop.set_stop_event(), self.async_loop)
        stop_future.result()
        self.game_loop_thread.join()
        self.root.unbind('<<UpdateDisplay>>')
        self.grid_remove()
        self.game_select_frame.grid()
