class BorderSide:
    def __init__(self, width=0, style=None, color=None, borderRadius=0):
        self.width = width
        self.style = style
        self.color = color
        self.borderRadius = borderRadius

    def to_css(self):
        
        width = f"border-width: {self.width}px;" if self.width else ''
        style = f"border-style: {self.style};" if self.style else ''
        color = f"border-color: {self.color};" if self.color else ''
        radius = f"border-radius: {self.borderRadius}px;" if self.borderRadius else ''
        return f"{width} {style} {color} {radius}"

    def to_int(self):
        return self.width

print(BorderSide.__name__)