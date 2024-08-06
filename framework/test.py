class BoxShadow:
    def __init__(self, color, offset, blurRadius, spreadRadius):
        self.color = color
        self.offset = offset
        self.blurRadius =blurRadius
        self.spreadRadius =spreadRadius

    def to_css(self):
        return f'{self.offset} {self.blurRadius} {self.spreadRadius} {self.color}'

def Offset(x, y):
    offset_x = x
    offset_y = y

    return f'{offset_x} {offset_y}'
    		
    		

print(BoxShadow(color='blue', offset=Offset(0,1), blurRadius=10, spreadRadius=10).to_css())