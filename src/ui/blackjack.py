import asyncio
import threading
from tkinter import ttk
from threading import Lock

from src.game.blackjack_new import BlackJackGame, BlackJackLoop

class BlackJackUI(ttk.Frame):

    name = 'BlackJack'

    def __init__(self, root, game_select_frame):
        super().__init__(root)
        self.game_select_frame = game_select_frame
        self.grid(row=0, column=0)
        
        # draw some placeholder stuff. These likely removed later for real drawing
        placeholder = ttk.Label(
            self, text='blackjack'
        ).grid(row=0, column=0)
        # if the tkinter event loop is not blocked in the main thread, 
        test_button = ttk.Button(
            self, text="test btuton", command=self.print_smth
        ).grid(row=0, column=1)
        stop_event_loop_button = ttk.Button(
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

    def draw_game(self):
        # acquire lock, then draw the game
        pass

    def print_smth(self):
        print('This message originated from the tk thread')

    def exit(self):
        #self.async_loop.call_soon_threadsafe(self.game_loop.set_stop_event)
        stop_future = asyncio.run_coroutine_threadsafe(self.game_loop.set_stop_event(), self.async_loop)
        stop_future.result()
        self.game_loop_thread.join()
        self.grid_remove()
        self.game_select_frame.grid()
