# base.py
import weakref

class Widget:
    _framework_ref = None

    @classmethod
    def set_framework(cls, framework):
        cls._framework_ref = weakref.ref(framework)

    def __init__(self, widget_id=None):
        framework = self._framework_ref()
        if framework:
            # Use the framework's IDManager to generate or validate the widget ID
            if widget_id and widget_id in framework.widget_registry:
                self._id = widget_id
            else:
                self._id = framework.id_manager.generate_id()
                framework.register_widget(self)  # Register the widget with the framework
        else:
            self._id = None  # In case the framework is not set, set ID to None

    def widget_id(self):
        return self._id

    def to_html(self):
        raise NotImplementedError("Each widget must implement the to_html method.")
