# base.py
import uuid
import weakref

class Widget:
    _framework_ref = None

    @classmethod
    def set_framework(cls, framework):
        cls._framework_ref = weakref.ref(framework)

    def __init__(self, widget_id=None):
        self._id = str(uuid.uuid4()) if widget_id is None else widget_id
        framework = self._framework_ref()
        if framework:
            framework.register_widget(self)

    def widget_id(self):
        return self._id

    def to_html(self):
        raise NotImplementedError("Each widget must implement the to_html method.")
