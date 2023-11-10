import asyncio

class GameData:
    pass

class GameLoop:
    def __init__(self, tk_root, loop, game, game_lock):
        # needs an event queue for game events
        # and to be aware of the tk root window 
        # so it can send tk events to the main thread
        self.tk_root = tk_root
        self.game = game
        self.game_lock = game_lock
        self.loop = loop
        self.stop_event = asyncio.Event()

    async def run(self):
        while not self.stop_event.is_set():
            self.update_display()
            await asyncio.sleep(1)

    def main(self):
        try:
            self.loop.run_until_complete(self.run())
        finally:
            self.loop.close()

    async def set_stop_event(self):
        self.stop_event.set()

    async def handle_network_events(self):
        pass

    async def update_game_state(self):
        #NOTE: threading.Lock.acquire will block the whole async event loop
        # need to acquire the lock in its own executor:
        # https://stackoverflow.com/questions/63420413/how-to-use-threading-lock-in-async-function-while-object-can-be-accessed-from-mu
        pass

    async def send_network_event(self, socket, message):
        pass

    def update_display(self):
        self.tk_root.event_generate('<<UpdateDisplay>>')