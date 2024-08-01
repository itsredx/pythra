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



print(Alignment.center().to_css())