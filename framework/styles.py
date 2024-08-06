#framework/styles.py
from enum import Enum


class EdgeInsets:
    def __init__(self, left=0, top=0, right=0, bottom=0):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @staticmethod
    def all(value):
        return EdgeInsets(left=value, top=value, right=value, bottom=value)

    @staticmethod
    def symmetric(horizontal=0, vertical=0):
        return EdgeInsets(left=horizontal, right=horizontal, top=vertical, bottom=vertical)

    def to_css(self):
        return f"{self.top}px {self.right}px {self.bottom}px {self.left}px"

class Alignment:
    def __init__(self, justify_content, align_items):
        self.justify_content = justify_content
        self.align_items = align_items

    @staticmethod
    def center():
        return Alignment('center', 'center')

    @staticmethod
    def top_left():
        return Alignment('flex-start', 'flex-start')

    @staticmethod
    def top_center():
        return Alignment('center', 'flex-start')

    @staticmethod
    def top_right():
        return Alignment('flex-end', 'flex-start')

    @staticmethod
    def center_left():
        return Alignment('flex-start', 'center')

    @staticmethod
    def center_right():
        return Alignment('flex-end', 'center')

    @staticmethod
    def bottom_left():
        return Alignment('flex-start', 'flex-end')

    @staticmethod
    def bottom_center():
        return Alignment('center', 'flex-end')

    @staticmethod
    def bottom_right():
        return Alignment('flex-end', 'flex-end')

    def to_css(self):
        return f"display: flex; justify-content: {self.justify_content}; align-items: {self.align_items};"

class TextAlign:
    def __init__(self, text_align):
        self.text_align = text_align

    @staticmethod
    def center():
        return TextAlign('center')

    @staticmethod
    def left():
        return TextAlign('flex-start')

    @staticmethod
    def right():
        return TextAlign('flex-end')

    def to_css(self):
        return f"{self.text_align};"

class BoxConstraints:
    def __init__(self, min_width=None, max_width=None, min_height=None, max_height=None):
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height

    def to_css(self):
        styles = []
        if self.min_width is not None:
            styles.append(f"min-width: {self.min_width}px;")
        if self.max_width is not None:
            styles.append(f"max-width: {self.max_width}px;")
        if self.min_height is not None:
            styles.append(f"min-height: {self.min_height}px;")
        if self.max_height is not None:
            styles.append(f"max-height: {self.max_height}px;")
        return " ".join(styles)

class Colors:
    @staticmethod
    def color(color_name):
        return color_name

    @staticmethod
    def hex(hex_code):
        if not hex_code.startswith("#"):
            raise ValueError("Hex code should start with #")
        return hex_code

    @staticmethod
    def rgba(red, blue, green, alpha):
        return f"rgba({red}, {blue}, {green}, {alpha})"

    

class BoxShadow:
    def __init__(self, color, offset, blurRadius, spreadRadius):
        self.color = color
        self.offset = offset
        self.blurRadius =blurRadius
        self.spreadRadius =spreadRadius

    def to_css(self):
        return f'{self.offset} {self.blurRadius}px {self.spreadRadius}px {self.color}'


def Offset(x, y):
    offset_x = x
    offset_y = y

    return f'{offset_x}px {offset_y}px'


class BoxDecoration:
    def __init__(self, color=None, border=None, borderRadius=None, boxShadow=None, transform=None):
        if color:
            self.color = Colors.color(color) if isinstance(color, str) and not color.startswith("#") else Colors.hex(color)
        else:
            self.color = None
        self.border = border
        self.borderRadius = borderRadius
        self.boxShadow = boxShadow
        self.transform = transform

    def to_css(self):
        styles = []
        if self.color:
            styles.append(f"background-color: {self.color};")
        if self.border:
            styles.append(f"border: {self.border};")
        if self.borderRadius:
            styles.append(f"border-radius: {self.borderRadius}px;")
        if self.boxShadow:
            styles.append(f"box-shadow: {self.boxShadow.to_css()};")
        if self.transform:
            styles.append(f"transform: {self.transform};")
        return ' '.join(styles)

class ClipBehavior(Enum):
    NONE = 'none'
    HARD_EDGE = 'hardEdge'
    ANTI_ALIAS = 'antiAlias'
    ANTI_ALIAS_WITH_SAVE_LAYER = 'antiAliasWithSaveLayer'
 
class ImageFit():
    CONTAIN = 'contain'
    COVER = 'cover'
    FILL = 'fill'
    NONE = 'none'
    SCALE_DOWN = 'scale-down'

class MainAxisSize:
    MIN = 'min'
    MAX = 'max'

class MainAxisAlignment:
    START = 'flex-start'
    END = 'flex-end'
    CENTER = 'center'
    SPACE_BETWEEN = 'space-between'
    SPACE_AROUND = 'space-around'
    SPACE_EVENLY = 'space-evenly'

class CrossAxisAlignment:
    START = 'flex-start'
    END = 'flex-end'
    CENTER = 'center'
    STRETCH = 'stretch'
    BASELINE = 'baseline'
    
class Axis:
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'
    
class TextStyle:
    def __init__(self, color=None, fontSize=None, fontWeight=None, fontStyle=None, letterSpacing=None, wordSpacing=None, textDecoration=None):
        self.color = color
        self.fontSize = fontSize
        self.fontWeight = fontWeight
        self.fontStyle = fontStyle
        self.letterSpacing = letterSpacing
        self.wordSpacing = wordSpacing
        self.textDecoration = textDecoration

    def to_css(self):
        style = ""
        if self.color:
            style += f"color: {self.color};"
        if self.fontSize:
            style += f"font-size: {self.fontSize}px;"
        if self.fontWeight:
            style += f"font-weight: {self.fontWeight};"
        if self.fontStyle:
            style += f"font-style: {self.fontStyle};"
        if self.letterSpacing:
            style += f"letter-spacing: {self.letterSpacing}px;"
        if self.wordSpacing:
            style += f"word-spacing: {self.wordSpacing}px;"
        if self.textDecoration:
            style += f"text-decoration: {self.textDecoration};"
        return style


class BorderStyle:
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

class ButtonStyle:
    def __init__(self, backgroundColor=None, foregroundColor=None, overlayColor=None, shadowColor=None,
                 elevation=None, padding=None, minimumSize=None, side=None, shape=None, 
                 textStyle=None, alignment=None, icon=None):
        self.backgroundColor = backgroundColor
        self.foregroundColor = foregroundColor
        self.overlayColor = overlayColor
        self.shadowColor = shadowColor
        self.elevation = elevation
        self.padding = padding
        self.minimumSize = minimumSize
        self.side = side
        self.shape = shape
        self.textStyle = textStyle
        self.alignment = alignment
        self.icon = icon

    def to_css(self):
        styles = []
        if self.backgroundColor:
            styles.append(f"background-color: {Colors.color(self.backgroundColor)};")
        if self.foregroundColor:
            styles.append(f"color: {Colors.color(self.foregroundColor)};")
        if self.shadowColor:
            styles.append(f"box-shadow: 0px 0px {self.elevation or 0}px {Colors.color(self.shadowColor)};")
        if self.padding:
            styles.append(f"padding: {self.padding.to_css()};")
        if self.minimumSize:
            styles.append(f"min-width: {self.minimumSize[0]}px; min-height: {self.minimumSize[1]}px;")
        if self.side:
            styles.append(f"{self.side.to_css()}")
        if self.shape:
            styles.append(f"border-radius: {self.shape};")
        if self.textStyle:
            styles.append(self.textStyle.to_css())
        if self.alignment:
            styles.append(self.alignment.to_css())
        if self.icon:
            styles.append(f"background-image: url({self.icon}); background-size: contain; background-repeat: no-repeat;")
        return ' '.join(styles)

class ScrollPhysics:
    BOUNCING = 'bouncing'
    CLAMPING = 'clamping'
    ALWAYS_SCROLLABLE = 'alwaysScrollable'
    NEVER_SCROLLABLE = 'neverScrollable'
    
class Overflow(Enum):
    VISIBLE = 'visible'
    HIDDEN = 'hidden'
    SCROLL = 'scroll'
    AUTO = 'auto'    

class StackFit(Enum):
    loose = 'loose'
    expand = 'expand'
    passthrough = 'passthrough'

class TextDirection(Enum):
    LTR = 'ltr'
    RTL = 'rtl'

class TextBaseline():
    alphabetic = 'text-bottom'
    ideographic = 'middle'

class VerticalDirection():
    DOWN = 'down'
    UP = 'up'
