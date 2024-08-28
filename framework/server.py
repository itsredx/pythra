import http.server
import socketserver
import threading
import time

class AssetServer(threading.Thread):
    def __init__(self, directory, port=8000):
        super().__init__()
        self.directory = directory
        self.port = port
        self.server = None

    def run(self):
        handler = http.server.SimpleHTTPRequestHandler
        handler.directory = self.directory
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            self.server = httpd
            httpd.serve_forever()

    def stop(self):
        if self.server:
            self.server.shutdown()




