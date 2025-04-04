# base.py


import weakref



class Widget:
    """
    The Base class for widgets.

    Attributes:
        _framework_ref (weakref.ref): Weak reference to the framework managing the widget.
        _parent (Widget): Reference to the parent widget.
        _children (list): List of child widgets.

    Raises:
        NotImplementedError: Raised when a required method is not implemented.
    """

    _framework_ref = None

    @classmethod
    def set_framework(cls, framework):
        """
        Set the framework reference for the widget class.

        Args:
            framework: The framework instance managing widgets.
        """

        cls._framework_ref = weakref.ref(framework)

    def __init__(self, widget_id=None):
        """
        Initialize a Widget instance.

        Args:
            widget_id (str, optional): The unique ID for the widget. If None, an ID is generated.

        Attributes:
            _id (str): The unique ID for the widget, generated or validated by the framework.
        """


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
        """
        Get the unique ID of the widget.

        Returns:
            str: The unique ID of the widget.
        """
        return self._id

    def to_html(self):
        """
        Generate HTML representation for the widget.

        Raises:
            NotImplementedError: This method must be implemented by derived classes.
        """
        raise NotImplementedError("Each widget must implement the to_html method.")

    def to_css(self):
        """
        Generate CSS styles for this widget and its children.

        Returns:
            str: A combined string of CSS styles for the widget and its children.
        """
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
        """
        Generate JavaScript representation for the widget.

        Returns:
            str: JavaScript representation of the widget.
        """
        return "Each widget should implement the to_js method for scripting."

    def set_parent(self, parent_widget):
        """
        Set the parent of the current widget.

        Args:
            parent_widget (Widget): The parent widget instance.
        """
        self._parent = parent_widget

    def add_child(self, child_widget):
        """
        Add a child widget to the current widget.

        Args:
            child_widget (Widget): The child widget instance to add.
        """
        self._children.append(child_widget)
        child_widget.set_parent(self)

    def get_children(self):
        """
        Get the list of child widgets.

        Returns:
            list: A list of child widgets.
        """
        return self._children 

    def remove_child(self, child_widget):
        """
        Remove a specific child widget.

        Args:
            child_widget (Widget): The child widget instance to remove.
        """
        self._children.remove(child_widget)
        child_widget.set_parent(None)

    def remove_all_children(self):
        """
        Removes all children from the current widget.
        """
        self._children.clear() 

    

    
