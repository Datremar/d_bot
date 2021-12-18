from src.auth.sessions import SessionLoop


class App:
    def __init__(self):
        self.sessions = SessionLoop()


app = App()
