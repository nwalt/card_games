import random
import asyncio
import threading
from tkinter import ttk
from threading import Lock

from src.game.blackjack_new import BlackJackGame, BlackJackLoop

class BlackJackUI(ttk.Frame):

    name = 'BlackJack'

    def __init__(self, root, game_select_frame):
        super().__init__(root)
        self.root = root
        self.game_select_frame = game_select_frame
        self.grid(row=0, column=0)
        
        # draw some placeholder stuff. These likely removed later for real drawing
        self.placeholder = ttk.Label(
            self, text='blackjack'
        )
        self.placeholder.grid(row=0, column=0)
        # if the tkinter event loop is not blocked in the main thread, 
        # the test button can work at any time
        ttk.Button(
            self, text="test button", command=self.print_smth
        ).grid(row=0, column=1)
        ttk.Button(
            self, text="End Game", command=self.exit
        ).grid(row=0, column=2)

        # initialize game state
        self.game_lock = Lock()
        self.game_state = BlackJackGame()
        # tk and asyncio CANNOT exist in the same thread
        # so we create an event loop, and send it to another thread to start
        self.async_loop = asyncio.new_event_loop()
        self.game_loop = BlackJackLoop(
            tk_root=root, loop=self.async_loop, game=self.game_state, game_lock=self.game_lock,
        )
        self.game_loop_thread = threading.Thread(
            name="blackjack_game_loop_thread", target=self.game_loop.main,
            # daemon threads are killed ungracefully on main thread exit.
            # Make sure they get cleaned up nicely instead
            daemon=True
        )
        self.game_loop_thread.start()
        # asyncio thread can only send events to root, so all binds that react to 
        # network or game loop activity must bind to root
        root.bind('<<UpdateDisplay>>', self.draw_game)

    def draw_game(self, *args):
        # acquire lock, then draw the game
        # placeholder code to make sure it works...
        print('Drawing game to display...')
        rand_text = ''.join(random.choices(list('asdfqwertyuiop'), k=9))
        self.placeholder['text'] = rand_text

    def print_smth(self):
        print('This message originated from the tk thread')

    def exit(self):
        #self.async_loop.call_soon_threadsafe(self.game_loop.set_stop_event)
        stop_future = asyncio.run_coroutine_threadsafe(self.game_loop.set_stop_event(), self.async_loop)
        stop_future.result()
        self.game_loop_thread.join()
        self.root.unbind('<<UpdateDisplay>>')
        self.grid_remove()
        self.game_select_frame.grid()
