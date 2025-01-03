# framework/core.py
from .id_manager import IDManager
import importlib
import time
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
    _instance = None

    config = Config()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


    def __init__(self):
        self.api = webwidget.Api()
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
        self.widgets = []
        self.registry = WidgetRegistry()

    def register_widget(self, widget, parent_widget=None):
        widget_id = widget.widget_id()
        self.registry.add_widget(widget_id, widget)

        if parent_widget:
            parent_widget.add_child(widget)
        else:
            self.root_widget = widget  # This could be your root widget

    def get_widget(self, widget_id):
        return self.registry.get_widget(widget_id)

    def get_all_widgets(self,):
        return self.registry.get_all_widgets()

    def update_widget(self, widget_id, widget):
        self.registry.update_widget(widget_id, widget)

    def delete_widget(self, widget_id):
        #self.registry.delete_widget(widget_id)
        """Deletes the widget and its children recursively from the registry."""
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
        """Recursively deletes the children of a widget."""
        children = widget.get_children() if widget.get_children() else []
        for child in children:
            self._delete_widget_children(child)  # Recursively delete child's children
            self.registry.delete_widget(child.widget_id())  # Delete child from registry
            #print("Child: ", child)
            #print("Widget Id: ",child.widget_id())
        widget.remove_all_children()  # Clear the children list of the widget

    def get_size(self):
        return self.registry.get_size()
  

    def set_root(self, widget):
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
        
        if hasattr(widget, 'onPressed') and widget.onPressed:
            #print(widget.onPressed)
            self.api.register_callback(widget.onPressed, getattr(self, widget.onPressed))
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self.collect_callbacks(child)

    def run(self, title):
        if not self.root_widget:
            raise ValueError("Root widget not set. Use set_root() to define the root widget.")
        
        html_content = self.root_widget.to_html()
        css_content = self.root_widget.to_css()
        #print('From core.py in Framework.run() {HTML From First Run:',html_content, '}')
        html_file = '/home/red-x/Documents/pythra/web/index.html'
        css_file = '/home/red-x/Documents/pythra/web/styles.css'
        os.makedirs('web', exist_ok=True)


        if self.frameless:
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
            c.close()

        else:
            with open(html_file, 'w') as f:
                f.write(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{title}</title>
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                    <link type="text/css" rel="stylesheet" href="styles.css">
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
            c.close()

        self.window = webwidget.create_window(title, self.id, html_file=html_file, js_api=self.api, width=800, height=600,)
        #print("Debug:", 'True' )
        
        webwidget.start(window=self.window, debug=bool(config.get("Debug")))
        

    
    def body_margin(self):
        if self.body:
            script_2 = f'document.getElementById("body").style.marginLeft = "-250px";'
            script_1 = f'document.getElementById("body").style.marginRight = "-250px";'
            self.window.evaluate_js(self.id, script_1, script_2)
    

    

    def toggle_drawer(self):
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
        if self.bottom_sheet:
            self.bottom_sheet.is_open = True
            script = 'document.getElementById("bottomSheet").style.transform = "translateY(0)";'
            self.window.evaluate_js(self.id, script)

    def hide_bottom_sheet(self):
        if self.bottom_sheet:
            self.bottom_sheet.is_open = False
            script = f'document.getElementById("bottomSheet").style.transform = "translateY(100%)";'
            self.window.evaluate_js(self.id, script)


    def show_snack_bar(self):
        if self.snack_bar:
            self.snack_bar.is_visible = True
            script = 'document.getElementById("snackBar").style.display = "flex";'
            self.window.evaluate_js(self.id, script)
            # Start a thread to hide the SnackBar after the specified duration
            threading.Thread(target=self._auto_hide_snack_bar, daemon=True).start()

    def _auto_hide_snack_bar(self):
        if self.snack_bar:
            time.sleep(self.snack_bar.duration / 1000)
            self.hide_snack_bar()

    def hide_snack_bar(self):
        if self.snack_bar and self.snack_bar.is_visible:
            self.snack_bar.is_visible = False
            script = 'document.getElementById("snackBar").style.display = "none";'
            self.window.evaluate_js(self.id, script)


    def update_content(self):
        
        if self.window:
            html_content = self.root_widget.to_html()
            script = f'document.body.innerHTML = `{html_content}`;'
            self.window.evaluate_js(self.id, script)

    def update_widget_dub(self, widget_id, html_content):
        # Update the widget's HTML representation based on its ID
        if widget_id in self.get_all_widgets():
            widget = self.get_widget(widget_id=widget_id)
            widget._update_html(html_content)
            #print(widget_id)

    def update_widget(self, widget_id, html_content):
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
