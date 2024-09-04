# main.py

from framework.core import Framework
from framework.widgets import *
from framework.styles import *
from framework.state import StatefulWidget, State

class CounterState(State):
    def __init__(self):
        super().__init__()
        self.count = 0

    def increment(self):
        self.count += 1
        print(self.count)
        self.setState()

    def decrement(self):
        self.count -= 1
        print(self.count)
        self.setState()

    def create_widget(self):
        return Column(
            children=[
                Text(f'Count: {self.count}'),
                ElevatedButton(
                    child=Text('Increment'),
                    onPressed=self.increment,
                ),
                
                ElevatedButton(child=Text('Decrement'),onPressed=self.decrement,)
            ]
        )


class CounterWidget(StatefulWidget):
    def createState(self):
        return CounterState()


class MyApp:
    def __init__(self):
        self.framework = Framework()
        self.counter_widget = CounterWidget()

    def update_ui(self):
        scaffold = Scaffold(
            appBar=AppBar(
                title=Text('Counter Example'),
            ),
            body=Body(
                child=self.counter_widget,  # Using the CounterWidget
            ),
        )
        self.framework.set_root(scaffold)
        #print('Debug print from MyApp(){','First ID:', self.counter_widget.widget_id(),'First HTML:', self.counter_widget.to_html(),'}')

    def run(self):
        self.update_ui()
        self.framework.run(title='MyApp')

if __name__ == "__main__":
    app = MyApp()
    app.run()
