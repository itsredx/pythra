class Drawer(Widget):
    def __init__(self, children, key=None):
        self.children = children
        self.key = key

    def to_html(self, drawer_open=False):
        children_html = ''.join([child.to_html() for child in self.children])
        drawer_class = "drawer-open" if drawer_open else "drawer-closed"
        return f"""
        <div id="drawer" class="{drawer_class}" style="position: fixed; top: 0; left: 0; width: 250px; height: 100%; background-color: #ffffff; box-shadow: 2px 0 5px rgba(0,0,0,0.5); transition: transform 0.3s ease;">
            {children_html}
        </div>
        <style>
            .drawer-closed {{
                transform: translateX(-100%);
            }}
            .drawer-open {{
                transform: translateX(0);
            }}
            .scrim-hidden {{
                display: none;
            }}
            .scrim-visible {{
                display: block;
            }}
        </style>
        """