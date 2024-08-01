# framework/api.py

class Api:
    def __init__(self):
        self.callbacks = {}

    def register_callback(self, name, callback):
        self.callbacks[name] = callback

    def on_pressed(self, callback_name):
        if callback_name in self.callbacks:
            self.callbacks[callback_name]()
            return f"Callback '{callback_name}' executed successfully."
        else:
            return f"Callback '{callback_name}' not found."

