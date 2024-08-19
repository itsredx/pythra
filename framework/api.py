# framework/api.py

class Api:
    def __init__(self):
        self.callbacks = {}

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Api, cls).__new__(cls)
        return cls._instance

    def register_callback(self, name, callback):
        self.callbacks[name] = callback

    def on_pressed(self, callback_name, index=None):
        if callback_name in self.callbacks:
            if index is not None:
                self.callbacks[callback_name](index)
            else:
                self.callbacks[callback_name]()
            return f"Callback '{callback_name}' executed successfully."
        else:
            return f"Callback '{callback_name}' not found."

