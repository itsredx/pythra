# id_manager.py
class IDManager:
    def __init__(self):
        self.ids = {}
        self.counter = 0

    def generate_id(self):
        self.counter += 1
        new_id = f"widget_{self.counter}"
        self.ids[new_id] = True
        return new_id

    def reset(self):
        self.ids.clear()
        self.counter = 0
