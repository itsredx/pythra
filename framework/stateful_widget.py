# stateful_widget.py
from .base import Widget
from .state import State

class StatefulWidget(Widget):
    def __init__(self):
        self._state = self.create_state()
        self._state.attach_widget(self)

    def create_state(self):
        """Override this method to return an instance of the State class."""
        return State()

    def get_state(self):
        return self._state

    def build(self):
        """Override this method to build the widget's UI."""
        raise NotImplementedError("StatefulWidget subclasses must implement the build method.")

    def to_html(self):
        """Generate the HTML representation of the widget."""
        return self.build().to_html()
