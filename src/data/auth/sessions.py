from time import time


class Session:
    def __init__(self):
        self.session = {}
        self.is_alive = True
        self.time_started = time()

    def refresh(self):
        self.time_started = time()

    def update(self):
        if time() - self.time_started > 30 * 60:
            self.is_alive = False

    def add(self, key: str, val):
        self.session[key] = val
        self.refresh()

    def delete(self, key):
        self.session.pop(key)


class SessionLoop:
    def __init__(self):
        self.sessions = {}

    def add_session(self, username):
        self.sessions[username] = Session()

    def get_session(self, username) -> Session:
        return self.sessions[username]

    def update(self):
        for session in self.sessions.values():
            session.update()
