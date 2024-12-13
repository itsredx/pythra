# framework/api.py
# Import the Api class from webwidget
from .window.webwidget import Api as WebWidgetApi

# Extend the WebWidgetApi class
class Api(WebWidgetApi):
    def __init__(self):
        # Initialize the parent class
        super().__init__()

    # Add any additional methods or overrides as needed
    def custom_method(self):
        print("This is a custom method in the extended API.")
