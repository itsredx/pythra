#import uuid

class Widget:
    def to_html(self):
        raise NotImplementedError("You must implement the to_html method")
        
    #def __init__(self):
        #self._id = str(uuid.uuid4())

