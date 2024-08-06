# framework/api.py

class Api:
    def __init__(self):
        self.callbacks = {}

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
