# framework/state.py
from .base import Widget
import weakref
import time
import threading
import asyncio
from PySide6.QtCore import QTimer
import time # Keep for potential use, but not for sleep here

class State:
    """
    A class that manages and updates the state of a widget.

    This class holds the state of a widget, including references to the widget itself, 
    its cached state, and methods to update the widget's content based on changes to 
    its state. It is intended to be used with a `StatefulWidget`.

    Attributes:
        _widget_id (str): The ID of the widget associated with this state.
        _widget_ref (weakref.ref): A weak reference to the widget.
        framework (Framework): A reference to the framework instance managing the widget.
        _cached_widget (Widget): A cached version of the widget's state.
        _original_widget_id (str): The original ID of the widget when it was first created.

    Methods:
        setState():
            Triggers an update to the widget by regenerating the widget tree and applying the new state.
        
        _set_widget(widget):
            Links the state to the provided widget by storing its reference and ID.
        
        widget_id():
            Returns the ID of the widget associated with the state.
        
        buildCache():
            Builds and caches the widget if not already cached.
        
        build():
            Abstract method to be implemented by subclasses to define how to build the widget state.
        
        update_existing_widget():
            Updates the existing widget with the new state and content.
        
        openDrawer():
            Opens the drawer in the root widget.
        
        closeDrawer():
            Closes the drawer in the root widget.
        
        openEndDrawer():
            Opens the end drawer in the root widget.
        
        closeEndDrawer():
            Closes the end drawer in the root widget.
        
        openBottomSheet():
            Opens the bottom sheet in the root widget.
        
        closeBottomSheet():
            Closes the bottom sheet in the root widget.
        
        openSnackBar():
            Opens the snackbar and starts a timer to automatically close it after a duration.
        
        closeSnackBar():
            Closes the snackbar in the root widget.
        
    """
    def __init__(self):
        self._widget_id = None  # Store the widget's ID instead of the widget itself
        self._widget_ref = None
        self.framework = StatefulWidget._framework_ref()
        self._cached_widget = None  # Cache the widget
        self._original_widget_id = None  # Store the original ID
        

    #def setState(self):
    #    self.update_existing_widget()
    
    def setState(self):
        # Get the *current* widget ID before rebuilding
        current_widget_id = self._original_widget_id
        if not current_widget_id:
            print(f"Warning: Original widget ID is missing before update.")
            # Maybe return early if no ID?
            # return

        if self.framework:
            # 1. Build the new widget tree
            new_widget_tree = self.build()
            self._cached_widget = new_widget_tree # Update cache
            new_widget_id = new_widget_tree.widget_id() # ID of the new tree root

            # 2. Call framework update, passing the NEW tree for scanning
            #    and the OLD ID for DOM replacement.
            if current_widget_id:
                self.framework.update_dom_and_css(current_widget_id, new_widget_tree) # Pass new tree
            else:
                print(f"Error: Cannot update DOM as original widget ID '{current_widget_id}' is invalid.")
                # If you reach here, something is wrong with ID tracking.
                return


            # 3. Delete old widget instance from Python registry (as requested)
            if current_widget_id and current_widget_id != new_widget_id:
                # Check if it still exists before trying to delete
                if self.framework.get_widget(current_widget_id):
                    self.framework.delete_widget(current_widget_id)
                #else: # Debugging
                #    print(f"Attempted to delete {current_widget_id}, but it was already gone.")

            print("Original Widget Id: ", current_widget_id, "New Widget Id: ",new_widget_id)
            # 4. Update tracked ID for the *next* update cycle
            self._original_widget_id = new_widget_id

        else:
            raise ValueError("Framework reference is not available in State.")

    def _set_widget(self, widget):
        self._widget_ref = weakref.ref(widget)
        if not self._widget_id:
            self._widget_id = widget.widget_id()
        

    def widget_id(self):
        return self._widget_id

    def buildCache(self):
        if not self._cached_widget:
            self._cached_widget = self.build()
            self._original_widget_id = self._cached_widget.widget_id()
        return self._cached_widget

    def build(self):
        raise NotImplementedError("build() should be implemented by subclasses")

    def update_existing_widget(self):
        widget = self.framework.get_widget(self._widget_id)
        updated_html = self._cached_widget.to_html()
        #print('Original Widget ID:', self._original_widget_id)
        #print('From state.py State.update_existing_widget(){',self._cached_widget.widget_id(),":" ,updated_html,'}')
        self.framework.update_widget(self._original_widget_id, updated_html)


    def openDrawer(self):
        self.framework.root_widget.drawer.toggle(True)
        
    def closeDrawer(self):
        self.framework.root_widget.drawer.toggle(False)
    
    def openEndDrawer(self):
        self.framework.root_widget.endDrawer.toggle(True)
        
    def closeEndDrawer(self):
        self.framework.root_widget.endDrawer.toggle(False)

    def openBottomSheet(self):
        self.framework.root_widget.bottomSheet.toggle(True)

    def closeBottomSheet(self):
        self.framework.root_widget.bottomSheet.toggle(False)

    def openSnackBar(self):
        snack_bar_widget = self.framework.root_widget.snackBar
        if not snack_bar_widget:
            print("Snackbar widget not found in root widget.")
            return

        # 1. Make snackbar visible (assuming this involves JS too)
        snack_bar_widget.toggle(True) # Let the toggle method handle showing it via JS

        # 2. Schedule the hide operation using QTimer
        duration_sec = snack_bar_widget.duration
        duration_ms = int(duration_sec * 1000) # QTimer uses milliseconds

        # Use a lambda or partial to call the hide method later
        # Ensure the framework and snackbar ID are accessible when the timer fires
        snack_bar_id = snack_bar_widget.widget_id() # Get ID now
        if not snack_bar_id:
            print("Error: Snackbar widget ID is missing.")
            return

        print(f"Scheduling snackbar {snack_bar_id} to hide in {duration_ms} ms") # Debug
        QTimer.singleShot(duration_ms, lambda: self._schedule_snackbar_hide(snack_bar_id))

    # Remove the old threaded method
    # def _auto_hide_snack_bar(self):
    #    pass

    def _schedule_snackbar_hide(self, snack_bar_id_to_hide):
        """
        This method is called by QTimer on the main GUI thread.
        It safely calls the framework's hide method.
        """
        print(f"Timer fired: Hiding snackbar {snack_bar_id_to_hide}") # Debug
        if self.framework:
            # Verify the snackbar we intend to hide might still be relevant
            # (Optional check: Is the *current* snackbar still the same one?)
            current_snackbar = self.framework.root_widget.snackBar
            if current_snackbar and current_snackbar.widget_id() == snack_bar_id_to_hide:
                self.framework.hide_snack_bar(snack_bar_id_to_hide)
                self.closeSnackBar()
            else:
                print(f"Snackbar {snack_bar_id_to_hide} is no longer the active snackbar or doesn't exist; not hiding.")
        else:
            print("Framework not available when trying to hide snackbar.")    


    def closeSnackBar(self):
        self.framework.root_widget.snackBar.toggle(False)
        
        print("Snack CLOSED")



class StatefulWidget(Widget):
    """
    A base class for widgets that have a mutable state.

    This class allows widgets to manage their state separately from their UI and 
    rebuild their UI when the state changes. It relies on the `State` class to manage 
    the state and handle updates to the widget content.

    Attributes:
        _framework_ref (weakref.ref): A weak reference to the framework instance.
        _state (State): The state associated with the widget.
    
    Methods:
        set_framework(framework):
            Sets the framework reference for the `StatefulWidget` class.
        
        __init__(key=None):
            Initializes the widget and links it to its state.
        
        createState():
            Abstract method to be implemented by subclasses to create the state for the widget.
        
        update():
            Updates the widget's HTML content with the new state.
        
        set_widget_id(widget_id):
            Sets the widget ID.
        
        widget_id():
            Returns the widget's ID.
        
        to_html():
            Returns the HTML representation of the widget.
        
        update_html_content(updated_html):
            Updates the widget's HTML content in the framework.
    """
    _framework_ref = None

    @classmethod
    def set_framework(cls, framework):
        cls._framework_ref = weakref.ref(framework)

    def __init__(self, key=None):
        super().__init__(widget_id=self.widget_id) # Call the Widget's __init__ method
        self._state = self.createState()
        self._state._set_widget(self) # Link the state to the widget
        self.framework = self._framework_ref()
 

    def createState(self):
        raise NotImplementedError("createState() method should be implemented by subclasses")

    def update(self):
        if self.framework:
            updated_html = self._state.buildCache().to_html()
            self.framework.update_widget(self.widget_id(), updated_html)

    def set_widget_id(self, widget_id):
        self._widget_id = widget_id

    def widget_id(self):
        return self._id  # Use the ID from the Widget base class

    def to_html(self):
        return self._state.buildCache().to_html()

    def update_html_content(self, updated_html):
        if self.framework:
            self.framework.update_widget(self.widget_id(), updated_html)
