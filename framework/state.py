# framework/state.py
from .base import Widget
import weakref
import time
import threading
import asyncio

class State:
    def __init__(self):
        self._widget_id = None  # Store the widget's ID instead of the widget itself
        self._widget_ref = None
        self.framework = StatefulWidget._framework_ref()
        self._cached_widget = None  # Cache the widget
        self._original_widget_id = None  # Store the original ID
        

    #def setState(self):
    #    self.update_existing_widget()
    
    def setState(self):
        widget = self._cached_widget
        if widget:
            # Regenerate the widget tree with the updated state
            self._cached_widget = self.build()
            
            self.update_existing_widget()
            self.framework.delete_widget(self._original_widget_id)
            #print("Size of the registry is: ",self.framework.get_size())
            self._original_widget_id = self._cached_widget.widget_id()
            #print('setState: {',self.build().to_html(), '}')
            #print('setState count: ',self.count)
            #widget.update_content(self.build())
        else:
            raise ValueError("The widget reference is invalid")

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
        self.framework.root_widget.snackBar.toggle(True)

        # Start a thread to hide the SnackBar after the specified duration
        threading.Thread(target=self._auto_hide_snack_bar, daemon=True).start()
        
    def _auto_hide_snack_bar(self):
        
        if self.framework.root_widget.snackBar:
            duration = self.framework.root_widget.snackBar.duration
            time.sleep(duration)
            self.closeSnackBar()
            self.setState()
            
        else:
            print(None)

    def closeSnackBar(self):
        self.framework.root_widget.snackBar.toggle(False)



class StatefulWidget(Widget):
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
