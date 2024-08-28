# framework/state.py

import weakref
from .widgets import Widget

# framework/state.py

class State:
    def __init__(self):
        self._widget_id = None  # Store the widget's ID instead of the widget itself
        self.framework = StatefulWidget._framework_ref()

    def setState(self):
        self.update_existing_widget()

    def _set_widget(self, widget):
        self._widget_id = widget.widget_id()

    def build(self):
        raise NotImplementedError("build() method should be implemented by subclasses")

    def update_existing_widget(self):
        widget = self.framework.get_widget(self.widget.widget_id())
        updated_html = widget.to_html()
        widget.update_html_content(updated_html)


# framework/state.py

class StatefulWidget(Widget):
    _framework_ref = None

    @classmethod
    def set_framework(cls, framework):
        cls._framework_ref = weakref.ref(framework)

    def __init__(self, key=None):
        super().__init__(widget_id=None)
        self._state = self.createState()
        self._state._set_widget(self)
        self.framework = self._framework_ref()

    def createState(self):
        raise NotImplementedError("createState() method should be implemented by subclasses")

    def update(self):
        if self.framework:
            # Use the widget's registry to update the correct widget instance
            updated_html = self._state.build().to_html()
            self.framework.update_widget(self.widget_id(), updated_html)

    def to_html(self):
        # Return the widget's HTML representation
        return self._state.build().to_html()

    def update_html_content(self, updated_html):
        if self.framework:
            # Ensure that we update the correct widget instance from the registry
            self.framework.update_widget(self.widget_id(), updated_html)
