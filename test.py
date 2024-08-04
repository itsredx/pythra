import inspect
import sys
from framework.api import Api
import main

def register_callbacks_from_module(self, module):
        for name, func in inspect.getmembers(module, inspect.isfunction):
            # Register only if the function is defined in the module and not imported
            if func.__module__ == module.__name__:
                self.framework.api.register_callback(name, func)
                print(f"Registered callback '{name}' from module '{module.__name__}'")



register_callbacks_from_module(sys)
