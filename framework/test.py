class BorderSide:
    def __init__(self, width=None, style=None, color=None, borderRadius=None):
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

class borderStyle:
    NONE = 'none'
    DOTTED = 'dotted'
    DASHED = 'dashed'
    SOLID = 'solid'
    DOUBLE ='double'
    GROOVE = 'groove'
    RIDGE = 'ridge'
    INSET = 'inset'
    OUTSET = 'outset'
    HIDDEN = 'hidden'


print(BorderSide(30, borderStyle.DOUBLE, 'red', 10).to_css())