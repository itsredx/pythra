# base.py
import uuid
import weakref

class Widget:
    _framework_ref = None

    @classmethod
    def set_framework(cls, framework):
        cls._framework_ref = weakref.ref(framework)

    def __init__(self, widget_id=None):
        framework = self._framework_ref()
        if framework:
            # Check if the widget ID already exists in the registry
            if widget_id and widget_id in framework.widget_registry:
                self._id = widget_id
            else:
                # Generate a new ID if not provided or not in the registry
                self._id = str(uuid.uuid4())
                framework.register_widget(self)
        else:
            self._id = str(uuid.uuid4())

    def widget_id(self):
        return self._id

    def to_html(self):
        raise NotImplementedError("Each widget must implement the to_html method.")
