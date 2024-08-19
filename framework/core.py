# framework/core.py
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



class Framework:
    def __init__(self):
        self.api = Api()
        self.root_widget = None
        self.window = None
        self.drawer = None
        self.end_drawer = None
        self.bottom_sheet = None
        self.snack_bar = None
        self.asset_server = AssetServer(directory='assets', port=8000)
        self.asset_server.start()

    def set_root(self, widget):
        self.root_widget = widget
        if isinstance(widget, Scaffold):
            self.drawer = widget.drawer
            self.end_drawer = widget.endDrawer
            self.bottom_sheet = widget.bottomSheet
            self.snack_bar = widget.snackBar
            self.body = widget.body

        
        self.collect_callbacks(widget)       
        if self.window:
            self.update_content()

    def run(self, title):
        if not self.root_widget:
            raise ValueError("Root widget not set. Use set_root() to define the root widget.")
        
        html_content = self.root_widget.to_html()
        html_file = 'web/index.html'
        os.makedirs('web', exist_ok=True)

        with open(html_file, 'w') as f:
            f.write(f"""
            <html>
            <head>
                <title>{title}</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                <script src="main.js"></script>
            </head>
            <body style="margin: 0px; padding: 0px; display: flex; height: 100vh;">
                {html_content}
            </body>
            </html>
            """)

        self.window = webview.create_window(title, html_file, js_api=self.api)
        webview.start(debug=True)
        

    def collect_callbacks(self, widget):
        
        if hasattr(widget, 'onPressed') and widget.onPressed:
            self.api.register_callback(widget.onPressed, getattr(self, widget.onPressed))
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self.collect_callbacks(child)

    
    def body_margin(self):
        if self.body:
            script_2 = f'document.getElementById("body").style.marginLeft = "-250px";'
            script_1 = f'document.getElementById("body").style.marginRight = "-250px";'
            self.window.evaluate_js(script_1, script_2)
    

    def toggle_drawer(self):
        if self.drawer:
            is_open = self.drawer.toggle()
            drawer_width = self.drawer.width + self.drawer.padding.to_int_horizontal() + self.drawer.borderRight.to_int()
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
            
            self.window.evaluate_js(script_1 + script_2 + script_3 + script_4)

    def show_bottom_sheet(self):
        if self.bottom_sheet:
            self.bottom_sheet.is_open = True
            script = 'document.getElementById("bottomSheet").style.transform = "translateY(0)";'
            self.window.evaluate_js(script)

    def hide_bottom_sheet(self):
        if self.bottom_sheet:
            self.bottom_sheet.is_open = False
            script = f'document.getElementById("bottomSheet").style.transform = "translateY(100%)";'
            self.window.evaluate_js(script)


    def show_snack_bar(self):
        if self.snack_bar:
            self.snack_bar.is_visible = True
            script = 'document.getElementById("snackBar").style.display = "flex";'
            self.window.evaluate_js(script)
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
            self.window.evaluate_js(script)


    def update_content(self):
        if self.window:
            html_content = self.root_widget.to_html()
            script = f'document.body.innerHTML = `{html_content}`;'
            self.window.evaluate_js(script)