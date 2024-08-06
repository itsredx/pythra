# framework/core.py
import importlib
import os
import inspect
import sys
import webview
from .widgets import Container, Column, IconButton, Icon, Text, Scaffold
from .api import Api
from .config import Config
from .server import AssetServer



class Framework:
    def __init__(self):
        self.api = Api()
        self.root_widget = None
        self.window = None
        self.drawer = None
        self.asset_server = AssetServer(directory='assets', port=8000)
        self.asset_server.start()

    def set_root(self, widget):
        self.root_widget = widget
        if isinstance(widget, Scaffold):
            self.drawer = widget.drawer


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

    def toggle_drawer(self):
        if self.drawer:
            is_open = self.drawer.toggle()
            drawer_transform = 'translateX(0)' if is_open else 'translateX(-100%)'
            body_width = 'calc(100% - 250px)' if is_open else '100%'
            margin_left = '' if is_open else '-250px'
            script_1 = f'document.getElementById("drawer").style.transform = "{drawer_transform}";'
            script_2 = f'document.getElementById("body").style.width = "{body_width}";'
            script_3 = f'document.getElementById("body").style.marginLeft = "{margin_left}"'
            self.window.evaluate_js(script_1 + script_2 + script_3)
            #script1_2 = f'document.getElementById("body").style.paddingLeft = "{scaffold_position}";'
            #script1_2 = f'document.getElementById("body").style.paddingLeft = "{scaffold_position}";'
            
            

    def update_content(self):
        if self.window:
            html_content = self.root_widget.to_html()
            script = f'document.body.innerHTML = `{html_content}`;'
            self.window.evaluate_js(script)



