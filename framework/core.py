# framework/core.py
from .id_manager import IDManager
import importlib
import time # Needed for timestamp cache busting
import threading
import os
import inspect
import sys
import webview
from .widgets import *
from .api import Api
from .config import Config
from .server import AssetServer
from .base import Widget
from .state import StatefulWidget
from .pyx.widget_registry import WidgetRegistry
from .window import webwidget
#import webview
import weakref




class Framework:
    """
    Framework is a singleton class that manages the overall structure and operation of the widget-based GUI framework. 
    It handles widget registration, updates, deletions, and the management of the application window. 

    Attributes:
    ----------
    api : Api
        An instance of the API class to interact with webview API for callbacks and communication.
    root_widget : Widget
        The root widget of the framework's widget tree.
    id : str
        An identifier for the framework instance.
    window : webview
        The webview window object for rendering the framework's interface.
    frameless : bool
        Indicates if the window is frameless or not.
    scaffold : Scaffold
        The main container widget that holds the layout and content.
    drawer : Drawer
        A drawer widget for side navigation in the UI.
    end_drawer : Drawer
        A drawer widget that appears from the end of the screen.
    bottom_sheet : BottomSheet
        A widget that can be slid up from the bottom of the screen.
    snack_bar : SnackBar
        A widget that displays temporary messages at the bottom of the screen.
    asset_server : AssetServer
        A server to serve static assets (like images or files) from the specified directory.
    id_manager : IDManager
        A manager for generating and managing unique widget IDs.
    widget_registry : dict
        A registry that stores and manages all widgets by their IDs.
    widgets : list
        A list of all widgets that have been registered.
    registry : WidgetRegistry
        A registry object that organizes widgets within the framework.

    Methods:
    --------
    instance():
        Returns the singleton instance of the Framework class.
    
    __init__():
        Initializes the framework with the necessary components like the API, asset server, ID manager, etc.

    register_widget(widget, parent_widget=None):
        Registers a widget into the framework, optionally under a parent widget.

    get_widget(widget_id):
        Retrieves a widget from the registry by its widget ID.

    get_all_widgets():
        Returns a list of all registered widgets in the framework.

    update_widget(widget_id, widget):
        Updates the widget in the registry by its widget ID.

    delete_widget(widget_id):
        Deletes a widget (and its children recursively) from the registry.

    _delete_widget_children(widget):
        Recursively deletes the children of a widget.

    get_size():
        Returns the total number of widgets currently registered.

    set_root(widget):
        Sets the root widget for the framework and initializes specific components like drawers and snack bars.

    collect_callbacks(widget):
        Collects and registers callback functions (like onPressed) for widgets and their children.
    """
    _instance = None

    config = Config()

    @classmethod
    def instance(cls):
        """
        Returns the singleton instance of the Framework class.
        If the instance doesn't exist, a new one is created and returned.

        Returns:
        --------
        Framework
            The singleton instance of the Framework class.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


    def __init__(self):
        """
        Initializes the framework with the necessary components:
        - API instance for handling callbacks.
        - Asset server to serve static files.
        - IDManager for generating unique widget IDs.
        - WidgetRegistry to store registered widgets.
        - Sets the framework as a singleton and links it to the Widget and StatefulWidget classes.
        """
        self.api = webwidget.Api()
        self.css_file_path = os.path.abspath('web/styles.css') # Store absolute path
        self.css_version = int(time.time()) # Initial CSS version/timestamp
        self.root_widget = None
        self.id = 'id'
        self.window = None
        self.frameless = True
        self.scaffold = None
        self.drawer = None
        self.end_drawer = None
        self.bottom_sheet = None
        self.snack_bar = None
        self.asset_server = AssetServer(directory='assets', port=config.get('assets_server_port'))
        self.asset_server.start()
        self.id_manager = IDManager()  # Initialize IDManager
        self.widget_registry = {} # Initialize the widget registry
        if Framework._instance is not None:
            raise Exception("This class is a singleton!")
        Framework._instance = self
        Widget.set_framework(self)  # Set the framework in Widget
        StatefulWidget.set_framework(self)
        # Ensure web directory exists
        os.makedirs('web', exist_ok=True)
        self.widgets = []
        self.registry = WidgetRegistry()
        
        
    def default_css(self, drawer_width, end_drawer_width):
        print(drawer_width,' ||| ', end_drawer_width)
        return f"""
* {{
    box-sizing: border-box;
}}
body {{
    margin: 0;
    font-family: Arial, sans-serif;
    display: flex;
    flex-direction: column;
}}

.body {{
    overflow: clip;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    height: 100vh;
    position: relative;
}}

.app-bar {{
    height: 60px;
    background-color: #6200ee;
    color: white;
    display: flex;
    align-items: center;
    padding: 0 20px;
    position: relative;
    transition: margin-left 0.3s, margin-right 0.3s;
}}

.drawer {{
    position: absolute;
    top: 0;
    bottom: 0;
    width: 250px;
    background-color: lightblue;
    z-index: 10;
    transition: transform 0.3s;
}}

.drawer.left {{
    left: 0;
    width: {drawer_width}px;
    transform: translateX(-100%);
    border-right: black;
    border-right-style: solid;
    border-right-width: 0.3px;
}}

.drawer.right {{
    right: 0;
    width: {end_drawer_width}px;
    transform: translateX(100%);
    border-left: black;
    border-left-style: solid;
    border-left-width: 0.3px;
}}

.drawer.open {{
    transform: translateX(0);
}}

.content {{
    flex: 1;
    padding: 20px;
    background-color: #f0f0f0;
    transition: margin-left 0.3s, margin-right 0.3s;
    overflow-y: auto;
}}

.bottom-nav {{
    height: 60px;
    background-color: #6200ee;
    position: absolute;
    left: 0px;
    right: 0px;
    bottom: 0px;
    color: white;
    display: flex;
    justify-content: space-around;
    align-items: center;
    transition: transform 0.3s;
}}

.bottom-nav.hidden {{
    transform: translateY(100%);
}}
        """
        

    def register_widget(self, widget, parent_widget=None):
        """
        Registers a widget into the framework and optionally assigns it a parent widget.

        Parameters:
        -----------
        widget : Widget
            The widget to be registered.
        parent_widget : Widget, optional
            The parent widget to which the new widget will be added (default is None).
        """
        widget_id = widget.widget_id()
        self.registry.add_widget(widget_id, widget)

        if parent_widget:
            parent_widget.add_child(widget)
        else:
            self.root_widget = widget  # This could be your root widget

    def get_widget(self, widget_id):
        """
        Retrieves a widget from the registry by its ID.

        Parameters:
        -----------
        widget_id : str
            The ID of the widget to retrieve.

        Returns:
        --------
        Widget
            The widget associated with the provided ID, or None if not found.
        """
        return self.registry.get_widget(widget_id)

    def get_all_widgets(self,):
        """
        Returns a list of all widgets currently registered in the framework.

        Returns:
        --------
        list of Widget
            A list containing all registered widgets.
        """
        return self.registry.get_all_widgets()

    def update_widget(self, widget_id, widget):
        """
        Updates a widget in the registry by its ID.

        Parameters:
        -----------
        widget_id : str
            The ID of the widget to update.
        widget : Widget
            The new widget object to update the registry with.
        """
        self.registry.update_widget(widget_id, widget)

    def delete_widget(self, widget_id):
        #self.registry.delete_widget(widget_id)
        """
        Deletes a widget from the registry, including all of its children.

        Parameters:
        -----------
        widget_id : str
            The ID of the widget to delete.
        """
        widget = self.get_widget(widget_id)
        if widget:
            # Recursively delete all children first
            self._delete_widget_children(widget)
            # Now delete the widget itself
            self.registry.delete_widget(widget_id)
            #print(f"Widget {widget_id} and its children deleted.")
        else:
            print(f"Widget with ID {widget_id} not found.")

    def _delete_widget_children(self, widget):
        """
        Recursively deletes the children of a widget.

        Parameters:
        -----------
        widget : Widget
            The widget whose children will be deleted.
        """
        children = widget.get_children() if widget.get_children() else []
        for child in children:
            self._delete_widget_children(child)  # Recursively delete child's children
            self.registry.delete_widget(child.widget_id())  # Delete child from registry
            #print("Child: ", child)
            #print("Widget Id: ",child.widget_id())
        widget.remove_all_children()  # Clear the children list of the widget

    def get_size(self):
        """
        Returns the total number of widgets currently registered.

        Returns:
        --------
        int
            The number of registered widgets.
        """
        return self.registry.get_size()
  

    def set_root(self, widget):
        """
        Sets the root widget for the framework. Initializes components like drawers and snack bars if the root widget is a Scaffold.

        Parameters:
        -----------
        widget : Widget
            The widget to be set as the root of the framework.
        """
        self.root_widget = widget
        
        if isinstance(widget, Scaffold):
            self.drawer = widget.drawer
            self.end_drawer = widget.endDrawer
            self.bottom_sheet = widget.bottomSheet
            self.snack_bar = widget.snackBar
            self.body = widget.body

        
        #self.collect_callbacks(widget)       
        if self.window:
            pass
            #self.update_content()

    def collect_callbacks(self, widget):
        """
        Collects and registers callback functions (like onPressed) for widgets and their children.

        Parameters:
        -----------
        widget : Widget
            The widget from which to collect callback functions.
        """
        
        if hasattr(widget, 'onPressed') and widget.onPressed:
            #print(widget.onPressed)
            self.api.register_callback(widget.onPressed, getattr(self, widget.onPressed))
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self.collect_callbacks(child)


    def _recursive_collect_classes(self, widget, active_classes):
        """Recursively traverses the widget tree and collects css_class attributes."""
        if widget is None:
            return

        # --- Check for the specific attribute holding the shared class ---
        # Adjust this if different widgets store their class name differently
        if hasattr(widget, 'css_class') and widget.css_class:
            active_classes.add(widget.css_class)
        # Example: if Text widget used 'text_css_class':
        # elif hasattr(widget, 'text_css_class') and widget.text_css_class:
        #     active_classes.add(widget.text_css_class)

        # --- Recursively check children ---
        if hasattr(widget, 'get_children'): # Standard way from Base Widget
            for child in widget.get_children():
                self._recursive_collect_classes(child, active_classes)
        elif hasattr(widget, 'child') and widget.child: # For single child widgets like Container
            self._recursive_collect_classes(widget.child, active_classes)
        elif hasattr(widget, 'children') and widget.children: # For multi-child widgets like Column/Row
            for child in widget.children:
                self._recursive_collect_classes(child, active_classes)
        # Add checks for other child attributes if necessary (e.g., appBar, drawer)
        if hasattr(widget, 'appBar') and widget.appBar:
            self._recursive_collect_classes(widget.appBar, active_classes)
        if hasattr(widget, 'drawer') and widget.drawer:
            self._recursive_collect_classes(widget.drawer, active_classes)
        # ... add other potential widget containers ...


    def _collect_active_css_classes(self, root_widget):
        """Starts the recursive collection of active CSS classes."""
        active_classes = set()
        self._recursive_collect_classes(root_widget, active_classes)
        # print(f"Active CSS classes found: {active_classes}") # Debug
        return active_classes

    def _generate_css_for_active_classes(self, active_classes):
        """Generates CSS rules only for the classes found in the active tree."""
        all_css_rules = []
        widget_classes_with_shared_styles = [Container, Text, Column, IconButton, Icon] # Maintain this list

        # Create reverse lookup dictionaries for efficiency (class_name -> style_key)
        reverse_lookups = {}
        for widget_cls in widget_classes_with_shared_styles:
            if hasattr(widget_cls, 'shared_styles') and isinstance(widget_cls.shared_styles, dict):
                reverse_lookups[widget_cls] = {v: k for k, v in widget_cls.shared_styles.items()}

        # Generate rules only for active classes
        for css_class in active_classes:
            generated = False
            for widget_cls in widget_classes_with_shared_styles:
                if widget_cls in reverse_lookups and css_class in reverse_lookups[widget_cls]:
                    style_key = reverse_lookups[widget_cls][css_class]
                    rule = None
                    # Call the appropriate generator based on the class type
                    if widget_cls == Container:
                        rule = self._create_container_css_rule(style_key, css_class)
                    # Add elif for Text, Column etc.
                    # elif widget_cls == Text:
                    #     rule = self._create_text_css_rule(style_key, css_class)

                    if rule:
                        all_css_rules.append(rule)
                        generated = True
                        break # Found the generator for this class, move to next active class
            # if not generated: # Debugging if a class isn't found
            #    print(f"Warning: No generator found for active CSS class: {css_class}")


        # --- Handle Instance-Specific Styles ---
        # Instance-specific styles (like Container foreground) CANNOT be cleaned up
        # this way easily because they aren't in the shared dicts.
        # These might need dedicated handling (e.g., inline styles, unique non-shared classes per instance).
        # For now, the overwrite will remove old foreground rules correctly IF they follow
        # a predictable pattern based on widget ID and IF the generator only creates them
        # for widgets currently in the tree (which the scan implicitly ensures).

        return "\n".join(all_css_rules)


    def _get_all_current_shared_css(self):
        """Collects CSS rules from ALL known shared style dictionaries."""
        all_css_rules = []
        # --- Centralized CSS Generation (Simplified) ---
        # This is where you'd ideally have a more robust way to find
        # all widget classes with shared styles.
        widget_classes_with_shared_styles = [Container, Text, Column, IconButton, Icon] # Add others as needed

        for widget_cls in widget_classes_with_shared_styles:
            if hasattr(widget_cls, 'shared_styles') and isinstance(widget_cls.shared_styles, dict):
                # Need a way to generate the rule string from the key/class
                # This requires refactoring the generation logic out of `to_css` methods
                for style_key, css_class in widget_cls.shared_styles.items():
                     # Assume a helper method exists per widget type or a general one
                     # For now, let's reuse the Container example logic if possible
                    if widget_cls == Container:
                        rule = self._create_container_css_rule(style_key, css_class)
                        if rule:
                            all_css_rules.append(rule)
                    # Add similar 'elif widget_cls == Text:' etc. using specific helpers
                    # elif widget_cls == Text:
                    #     rule = self._create_text_css_rule(style_key, css_class) # Example
                    #     if rule: all_css_rules.append(rule)

            # Handle instance-specific CSS if needed (like Container's foreground)
            # This part is tricky with a full file overwrite. Instance-specific
            # styles might be better handled inline or via dedicated classes added
            # directly to the element, not in the shared file.
            # Let's ignore foreground for this file-based approach for simplicity now.

        return "\n".join(all_css_rules)

    # Helper function (as before, needs refinement/expansion for other types)
    def _create_container_css_rule(self, style_key, css_class):
        try:
            # Simplified access - real implementation might need more robust key unpacking
            padding, color, decoration, width, height, margin, alignment, clipBehavior = style_key

            padding_str = f'padding: {padding.to_css()};' if hasattr(padding, 'to_css') else (f'padding: {padding};' if padding else '')
            margin_str = f'margin: {margin.to_css()};' if hasattr(margin, 'to_css') else (f'margin: {margin};' if margin else '')
            width_str = f'width: {width}px;' if width is not None else ''
            height_str = f'height: {height}px;' if height is not None else ''
            color_str = f'background-color: {color};' if color else ''
            decoration_str = decoration.to_css() if hasattr(decoration, 'to_css') else ''
            clip_str = f'overflow: hidden;' if clipBehavior else '' # Assuming bool or similar
            alignment_str = alignment.to_css() if hasattr(alignment, 'to_css') else ''

            rule = f"""
            .{css_class} {{
                position: relative;
                {padding_str}
                {margin_str}
                {width_str}
                {height_str}
                {color_str}
                {decoration_str}
                {alignment_str}
                {clip_str}
                box-sizing: border-box;
            }}
            """
            return rule
        except Exception as e:
            # Log the error properly in a real app
            print(f"Error generating CSS for {css_class} with key {style_key}: {e}")
            return ""


    def run(self, title):
        """
        Starts the framework and launches the webview window with the root widget. This method generates the HTML and 
        CSS content for the root widget.

        Args:
            title (str): The title to display in the browser tab.
        
        Raises:
            ValueError: If the root widget is not set.
        """
        if not self.root_widget:
            raise ValueError("Root widget not set. Use set_root() to define the root widget.")
        
        html_content = self.root_widget.to_html()
        print("ROOT DRAWERWIDTH: ",self.root_widget.drawer.width)
        # --- Initial Generation ---
        active_classes = self._collect_active_css_classes(self.root_widget)
        css_content = self._generate_css_for_active_classes(active_classes)
        #print('From core.py in Framework.run() {HTML From First Run:',html_content, '}')
        html_file = os.path.abspath('web/index.html')
        css_file = self.css_file_path # Use the stored path


        if not self.frameless:
            with open(html_file, 'w') as f:
                f.write(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{title}</title>
                    <link type="text/css" rel="stylesheet" href="styles.css">
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">      
                    <script src="qwebchannel.js"></script>
                    <script src="main.js"></script>
                    <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
                </head>
                <body>
                        {html_content}
                </body>
                </html>
                """)

            f.close()

            with open(css_file, 'a') as c:
                c.write(css_content)
                print(f"Initial styles written to {css_file}")
            c.close()

        else:
            # Write initial CSS file
            try:
                with open(css_file, 'w') as c:
                    c.write(f"""
                    {self.default_css(self.root_widget.drawer.width, self.root_widget.endDrawer.width)}
                    {css_content}
                    """)
                print(f"Initial styles written to {css_file}")
            except IOError as e:
                print(f"Error writing initial CSS file: {e}")
                # Decide how to handle this - maybe raise exception?

            # Write initial HTML file, including the versioned CSS link
            try:
                with open(html_file, 'w') as f:
                    f.write(f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>{title}</title>
                        <link id="main-stylesheet" type="text/css" rel="stylesheet" href="styles.css?v={self.css_version}">
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                        <script src="qwebchannel.js"></script>
                        <script src="main.js"></script>
                        <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
                    </head>
                    <body>
                            {html_content}
                    </body>
                    </html>
                    """)
                print(f"Initial HTML written to {html_file}")
            except IOError as e:
                print(f"Error writing initial HTML file: {e}")
                # Handle error

            

        self.window = webwidget.create_window(title, self.id, html_file=html_file, js_api=self.api, width=800, height=600,)
        #print("Debug:", 'True' )
        
        webwidget.start(window=self.window, debug=bool(config.get("Debug")))
        
    def body_margin(self):
        """
        Adjusts the margin of the body element to hide/show the side drawer based on its state.
        """
        if self.body:
            script_2 = f'document.getElementById("body").style.marginLeft = "-250px";'
            script_1 = f'document.getElementById("body").style.marginRight = "-250px";'
            self.window.evaluate_js(self.id, script_1, script_2)
        
    def toggle_drawer(self):
        """
        Toggles the state of the side drawer (open/close).
        """
        if self.drawer:
            self.drawer().toggle_true()
            print(self.drawer.is_open)
            #is_open = self.drawer.toggle()
            """drawer_width = self.drawer.width + self.drawer.padding.to_int_horizontal() + self.drawer.borderRight.to_int()
            drawer_transform = 'translateX(0)' if is_open else f'translateX(-{drawer_width}px)'
            body_width = f'calc(100% - {drawer_width}px)' if is_open else '100%'
            margin_left = '' if is_open else f'-{drawer_width}px' 
            end_drawer_width = self.end_drawer.width + self.end_drawer.padding.to_int_horizontal() + self.end_drawer.borderLeft.to_int()
            margin_right = '0px' if self.end_drawer.is_open else f'-{end_drawer_width}px'            
            script_1 = f'document.getElementById("drawer").style.transform = "{drawer_transform}";'
            script_2 = f'document.getElementById("body").style.width = "{body_width}";'
            script_3 = f'document.getElementById("body").style.marginLeft = "{margin_left}";'
            script1_4 = f'document.getElementById("body").style.marginRight = "{margin_right}";'
            self.window.evaluate_js(script_1 + script_2 + script_3 + script1_4)
            
            #script1_2 = f'document.getElementById("body").style.paddingLeft = "{scaffold_position}";'
            """
    def toggle_end_drawer(self):
        """
        Toggles the state of the end drawer (open/close).
        """
        if self.end_drawer:
            is_open = self.end_drawer.toggle()
            end_drawer_width = self.end_drawer.width + self.end_drawer.padding.to_int_horizontal() + self.end_drawer.borderLeft.to_int()
            drawer_transform = 'translateX(0)' if is_open else f'translateX({end_drawer_width}px)'
            body_width = f'calc(100% - {end_drawer_width}px)' if is_open else '100%'
            margin_left = f'-{end_drawer_width}px' if is_open else f'-{end_drawer_width}px'
            if self.drawer.is_open:
                margin_left = '0px'
            else:
                drawer_width = self.drawer.width + self.drawer.padding.to_int_horizontal() + self.drawer.borderRight.to_int()
                margin_left = f'-{drawer_width}px'
            margin_right = '0px' if is_open else f'-{end_drawer_width}px'
            script_1 = f'document.getElementById("endDrawer").style.transform = "{drawer_transform}";'
            script_2 = f'document.getElementById("body").style.width = "{body_width}";'
            script_3 = f'document.getElementById("body").style.marginRight = "{margin_right}";'
            script_4 = f'document.getElementById("body").style.marginLeft = "{margin_left}"'
            
            self.window.evaluate_js(self.id, script_1 + script_2 + script_3 + script_4)

    def show_bottom_sheet(self):
        """
        Displays the bottom sheet widget.
        """
        if self.bottom_sheet:
            self.bottom_sheet.is_open = True
            script = 'document.getElementById("bottomSheet").style.transform = "translateY(0)";'
            self.window.evaluate_js(self.id, script)

    def hide_bottom_sheet(self):
        """
        Hides the bottom sheet widget.
        """
        if self.bottom_sheet:
            self.bottom_sheet.is_open = False
            script = f'document.getElementById("bottomSheet").style.transform = "translateY(100%)";'
            self.window.evaluate_js(self.id, script)


    def show_snack_bar(self):
        """
        Displays the snack bar widget with a message. The snack bar is auto-hidden after a delay.
        """
        if self.snack_bar:
            self.snack_bar.is_visible = True
            script = 'document.getElementById("snackBar").style.display = "flex";'
            self.window.evaluate_js(self.id, script)
            # Start a thread to hide the SnackBar after the specified duration
            threading.Thread(target=self._auto_hide_snack_bar, daemon=True).start()

    def _auto_hide_snack_bar(self):
        """
        Helper function that waits for the snack bar's duration and hides it automatically.
        """
        if self.snack_bar:
            time.sleep(self.snack_bar.duration / 1000)
            self.hide_snack_bar()

    def hide_snack_bar(self, widget_id=''):
        """
        Hides the snack bar widget.
        """
        
        if self.root_widget.snackBar:
            
            #self.root_widget.snackBar.is_open = False
            script = f"""document.getElementById('{widget_id}').style.display = 'none';"""
            
            self.window.evaluate_js(self.id, script)
    


    def update_content(self):
        """
        Updates the HTML content of the window by regenerating the root widget's HTML and re-rendering it in the window.
        """
        
        if self.window:
            html_content = self.root_widget.to_html()
            script = f'document.body.innerHTML = `{html_content}`;'
            self.window.evaluate_js(self.id, script)

    def update_widget_dub(self, widget_id, html_content):
        """
        Updates a widget's HTML content using its widget ID.

        Args:
            widget_id (str): The ID of the widget to update.
            html_content (str): The new HTML content for the widget.
        """
        # Update the widget's HTML representation based on its ID
        if widget_id in self.get_all_widgets():
            widget = self.get_widget(widget_id=widget_id)
            widget._update_html(html_content)
            #print(widget_id)

    def update_widget(self, widget_id, html_content):
        """
        Updates a widget's HTML content in the window using JavaScript.

        Args:
            widget_id (str): The ID of the widget to update.
            html_content (str): The new HTML content for the widget.
        """
        if self.window:
            html_widget = html_content
            #widget_id = widget.widget_id()
            #print(self.get_all_widgets())
            if widget_id in self.get_all_widgets():
                
                #widget = self.widget_registry[widget_id]
                script = f'''
                            if (document.getElementById("{widget_id}")) {{
                                document.getElementById("{widget_id}").outerHTML = `{html_content}`;
                            }} else {{
                                console.log("Element with ID {widget_id} not found.");
                            }}
                            '''
                self.window.evaluate_js(self.id, script)
            else:
                print('Widget With ID: {widget_id} Not In Registry')


    # Rename update_widget_and_css for clarity
    def update_dom_and_css(self, widget_id_to_replace, new_widget_tree):
        """
        Updates CSS file based *only* on classes in new_widget_tree,
        triggers browser reload, and updates HTML.
        """
        if not self.window:
            print(f"Window not available for update {widget_id_to_replace}")
            return

        # --- 1. Scan New Tree and Generate Filtered CSS ---
        active_classes = self._collect_active_css_classes(new_widget_tree)
        filtered_css_content = self._generate_css_for_active_classes(active_classes)

        # --- 2. Overwrite CSS File ---
        try:
            with open(self.css_file_path, 'w') as c:
                c.write(f"""
                    {self.default_css(self.root_widget.drawer.width, self.root_widget.endDrawer.width)}
                    {filtered_css_content}
                    """)
            # print(f"CSS file updated with active styles: {self.css_file_path}") # Debug
        except IOError as e:
            print(f"Error updating CSS file: {e}")
            # Handle error

        # --- 3. Increment CSS Version for Cache Busting ---
        self.css_version = int(time.time())

        # --- 4. Generate HTML for the new tree ---
        # NOTE: Ensure to_html() is called on the NEW tree passed in
        new_html_content = new_widget_tree.to_html()
        print("New html Content: ", new_html_content)

        # --- 5. Prepare and Execute JavaScript (Cache Bust + HTML Update) ---
        escaped_html = new_html_content.replace('\\', '\\\\').replace('`', '\\`')
        new_css_href = f"styles.css?v={self.css_version}"
        print("Escaped html Content: ", escaped_html)
        print("Widget to replace: ", widget_id_to_replace)

        script = f'''
            // Update CSS Link
            var linkElement = document.getElementById('main-stylesheet');
            if (linkElement) {{
                linkElement.href = '{new_css_href}';
            }} else {{
                console.warn('Stylesheet link element "main-stylesheet" not found.');
            }}

            // Update HTML Element
            var elementToUpdate = document.getElementById("{widget_id_to_replace}");
            if (elementToUpdate) {{
                console.log(`{escaped_html}`);
                elementToUpdate.outerHTML = `{escaped_html}`;
            }} else {{
                // This might happen if the ID itself changed AND the old element was removed by parent update
                console.warn("Element with ID {widget_id_to_replace} not found for HTML update.");
            }}
        '''
        self.window.evaluate_js(self.id, script)