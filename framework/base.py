# base.py
import weakref

class Widget:
    _framework_ref = None

    @classmethod
    def set_framework(cls, framework):
        cls._framework_ref = weakref.ref(framework)

    def __init__(self, widget_id=None):
        framework = self._framework_ref()
        #self._key = key
        self._parent = None  # Reference to the parent widget
        self._children = []  # List of child widgets

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

    def to_css(self):
        """Generate CSS styles for this widget and its children."""
        css_styles = []

        # Add styles for the current widget
        current_widget_css = ""
        css_styles.append(current_widget_css)

        # Collect CSS styles from child widgets
        for child in self._children:
            css_styles.append(child.to_css())

        # Combine all styles into a single string
        return "\n".join(css_styles)


    def to_js(self):
        return "Each widget should implement the to_js method for scripting."

    def set_parent(self, parent_widget):
        """Sets the parent of the current widget."""
        self._parent = parent_widget

    def add_child(self, child_widget):
        """Adds a child to the current widget."""
        self._children.append(child_widget)
        child_widget.set_parent(self)

    def get_children(self):
        """Returns the list of child widgets."""
        return self._children 

    def remove_child(self, child_widget):
        """Removes a specific child widget."""
        self._children.remove(child_widget)
        child_widget.set_parent(None)

    def remove_all_children(self):
        """Removes all children from the current widget."""
        self._children.clear() 

    

    
