# stateful_widget.py

from framework.widgets import Widget

class StatefulWidget(Widget):
    def __init__(self):
        super().__init__()
        self._state = None

    def create_state(self):
        raise NotImplementedError("create_state() must be implemented by subclasses")

    def _initialize_state(self):
        self._state = self.create_state()
        self._state._set_widget(self)

    def build(self):
        if self._state is None:
            self._initialize_state()
        return self._state.build()

class State:
    def __init__(self):
        self._widget = None

    def _set_widget(self, widget):
        self._widget = widget

    def set_state(self, fn=None):
        if fn:
            fn()
        self._widget.framework.update_widget(self.build())  # Trigger a rebuild of the widget tree

    def build(self):
        raise NotImplementedError("build() must be implemented by subclasses")
