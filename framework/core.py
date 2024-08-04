# framework/core.py
import importlib
import os
import inspect
import sys
import webview
from .widgets import Container, Column, IconButton, Icon, Text
from .api import Api
from .config import Config
from .server import AssetServer



class Framework:
    def __init__(self):
        self.api = Api()
        self.root_widget = None
        self.window = None
        self.asset_server = AssetServer(directory='assets', port=8000)
        self.asset_server.start()

    def set_root(self, widget):
        self.root_widget = widget
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
            <body style="margin: 0px; padding: 0px;">
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

    def update_content(self):
        if self.window:
            html_content = self.root_widget.to_html()
            script = f'document.body.innerHTML = `{html_content}`;'
            self.window.evaluate_js(script)



