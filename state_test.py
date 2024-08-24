# counter_app.py

from framework.core import Framework
from framework.widgets import *
from framework.styles import *
from framework.stateful_widget import StatefulWidget, State



# counter_app.py



class CounterState(State):
    def __init__(self, framework):
        super().__init__()
        self.count = 0
        self.framework = framework

    def increment(self):
        self.count += 1
        self.set_state()  # Trigger a rebuild

    def build(self):
        
        return Column(
            children=[
                Text(f'Count: {self.count}'),
                ElevatedButton(
                    child=Text('Increment'),
                    onPressed=self.increment
                )
            ]
        )

class CounterApp(StatefulWidget):
    def __init__(self, framework):
        super().__init__()
        self.framework = framework

    def create_state(self):
        
        return CounterState(self.framework)

class MyApp:
    def __init__(self):
        self.framework = Framework()


    def run(self):
        counter_app = CounterApp(self.framework)
        scaffold = Scaffold(
            body=counter_app.build()  # This calls the build method of the CounterApp
        )
        self.framework.set_root(scaffold)
        self.framework.run(title='CounterApp')



if __name__ == "__main__":
    app = MyApp()
    app.run()
