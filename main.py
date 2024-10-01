# main.py needs refactoring

# main.py refactored with StatefulWidget and State management

from framework.core import Framework
from framework.widgets import *
from framework.styles import *
from framework.state import StatefulWidget, State


class MyAppState(State):
    def __init__(self):
        super().__init__()
        self.currentIndex = 0
        self.bottom_sheet_visible = False
        self.snack_bar_visible = False
        self.drawer_visible = False
        self.end_drawer_visible = False

    def on_tab_selected(self, index):
        self.currentIndex = index
        self.setState()  # Update the UI when the tab is selected

    def toggle_drawer(self):
        self.drawer_visible = not self.drawer_visible
        self.setState()

    def toggle_end_drawer(self):
        self.end_drawer_visible = not self.end_drawer_visible
        self.setState()

    def show_bottom_sheet(self):
        self.bottom_sheet_visible = True
        self.setState()

    def hide_bottom_sheet(self):
        self.bottom_sheet_visible = False
        self.setState()

    def show_snack_bar(self):
        self.snack_bar_visible = True
        self.setState()

    def hide_snack_bar(self):
        self.snack_bar_visible = False
        self.setState()

    def undo(self):
        print("Undo action")
        self.hide_snack_bar()

    def build(self):
        # Define the content for each tab
        content = [
            Container(
                child=Column(
                    children=[
                        Text('Welcome to the Home Page!'),
                        IconButton(
                            icon=Icon('plus'),
                            onPressed=self.show_bottom_sheet
                        ),
                        IconButton(
                            icon=Icon('flask'),
                            onPressed=self.show_snack_bar
                        ),
                    ]
                ),
                padding=EdgeInsets.all(20),
                margin=EdgeInsets.all(20),
                constraints=BoxConstraints(max_width=300, max_height=300),
                decoration=BoxDecoration(
                    color=Colors.color('lightblue'),
                    borderRadius=25,
                )
            ),
            Container(
                child=Text('Settings Page'),
                padding=EdgeInsets.all(20),
                margin=EdgeInsets.all(20),
                constraints=BoxConstraints(max_width=300, max_height=300),
                decoration=BoxDecoration(
                    color=Colors.color('lightblue'),
                    borderRadius=25,
                )
            )
        ]

        # Set the content based on the current index
        body_content = content[self.currentIndex]

        drawer = Drawer(
            child=Text('Hello'),
            width=300,
            divider=Divider(
                margin=EdgeInsets.symmetric(8, 0)
            ),
        ) if self.drawer_visible else None

        end_drawer = EndDrawer(
            child=Text('Hello End'),
            width=250,
            divider=Divider(
                margin=EdgeInsets.symmetric(8, 0)
            ),
        ) if self.end_drawer_visible else None

        snack_bar_action = SnackBarAction(
            label=Text("UNDO"),
            onPressed=self.undo
        )

        snack_bar = SnackBar(
            content=Text("Item deleted"),
            action=snack_bar_action,
            duration=5000,
            backgroundColor=Colors.color("darkgrey"), 
        ) if self.snack_bar_visible else None

        scaffold = Scaffold(
            appBar=AppBar(
                title=Text('Bottom Navigation Example'),
                elevation=2,
                shadowColor=Colors.rgba(0, 0, 0, 0.2),
                leading=IconButton(
                    icon=Icon('bars'),
                    onPressed=self.toggle_drawer
                ),
                actions=[
                    IconButton(
                        icon=Icon('bars'),
                        onPressed=self.toggle_end_drawer
                    ),
                ],
            ) if self.currentIndex == 0 else None,

            body=Body(
                child=body_content,
            ),  # Use the selected content
            drawer=drawer,
            endDrawer=end_drawer,
            bottomNavigationBar=BottomNavigationBar(
                items=[
                    BottomNavigationBarItem(icon=Icon('home'), label=Text('Home')),
                    BottomNavigationBarItem(icon=Icon('gear'), label=Text('Settings')),
                ],
                onTap=self.on_tab_selected,
                currentIndex=self.currentIndex,
                backgroundColor=Colors.color('white'),
                elevation=10,
                iconSize=30,
                selectedFontSize=18,
                unselectedFontSize=14,
                selectedItemColor=Colors.color('blue'),
                unselectedItemColor=Colors.color('grey'),
                showSelectedLabels=True,
                showUnselectedLabels=True,
            ),
            bottomSheet=BottomSheet(
                child=Column(
                    children=[
                        Text("This is a BottomSheet"),
                        IconButton(
                            icon=Icon('minus'),
                            onPressed=self.hide_bottom_sheet
                        ),
                    ]
                ),
                height=300,
                backgroundColor=Colors.color("lightgrey"),
                enableDrag=True
            ) if self.bottom_sheet_visible else None,
            snackBar=snack_bar
        )

        return scaffold


class MyApp(StatefulWidget):
    def createState(self):
        return MyAppState()


# The main application class to run the framework
class Application:
    def __init__(self):
        self.framework = Framework()
        self.my_app = MyApp()

    def run(self):
        self.framework.set_root(self.my_app)
        self.framework.run(title='MyApp')


if __name__ == "__main__":
    app = Application()
    app.run()


"""
from framework.core import Framework
from framework.widgets import *
from framework.styles import *
from framework.widgets import Widget


class MyApp:
    def __init__(self):
        self.framework = Framework()
        self.currentIndex = 0

    def on_tab_selected(self, index):
        print(f"Tab {index} selected")
        self.currentIndex = index
        self.update_ui()
        
    def toggle_drawer(self):
        self.framework.toggle_drawer()

    def toggle_end_drawer(self):
        self.framework.toggle_end_drawer()

    def show_bottom_sheet(self):
        self.framework.show_bottom_sheet()

    def hide_bottom_sheet(self):
        self.framework.hide_bottom_sheet()

    def show_snack_bar(self):
        self.framework.show_snack_bar()
    
    def hide_snack_bar(self):
        self.framework.hide_snack_bar()

    def undo(self):
        print("Undo action")

    def update_ui(self):
        # Define the content for each tab
        content = [
            Container(
                child=Column(
                children=[
                    Text('Welcome to the Home Page!'),
                    IconButton(
                        icon=Icon('plus'),
                        onPressed= self.show_bottom_sheet),
                    IconButton(
                        icon=Icon('flask'),
                        onPressed= self.show_snack_bar),
                ]
            ),
                padding=EdgeInsets.all(20),
                margin=EdgeInsets.all(20),
                constraints= BoxConstraints(max_width= 300, max_height=300),
                decoration=BoxDecoration(
                    color=Colors.color('lightblue'),
                    borderRadius=25,
                )
                ),
            Container(
                child=Text('Settings Page'),
                padding=EdgeInsets.all(20),
                margin=EdgeInsets.all(20),
                constraints= BoxConstraints(max_width= 300, max_height=300),
                decoration=BoxDecoration(
                    color=Colors.color('lightblue'),
                    borderRadius=25,
                )
                )
        ]

        column = Column(
            children=[
                Text('Welcome to the Home Page!'),
                IconButton(
                    icon=Icon('plus'),
                    onPressed= self.show_bottom_sheet
                    ),
            ]
        )

        # Set the content based on the current index
        body_content = content[self.currentIndex]

        drawer = Drawer(
            child=Text('Hello'),
            width=300,
            divider=Divider(
                margin=EdgeInsets.symmetric(8,0)
            ),
        )

        end_drawer = EndDrawer(
            child=Text('Hello End'),
            width=250,
            divider=Divider(
                margin=EdgeInsets.symmetric(8,0)
            ),
        )

        snack_bar_action = SnackBarAction(
            label="UNDO",
            onPressed=self.undo
        )

        snack_bar = SnackBar(
            content=Text("Item deleted"),
            action=snack_bar_action,
            duration=5000,
            backgroundColor=Colors.color("darkgrey"),
        )

        scaffold = Scaffold(
            appBar= AppBar(
                title=Text('Bottom Navigation Example'),
                elevation=2,
                shadowColor=Colors.rgba(0,0,0,0.2), 
                leading=IconButton(
                    icon=Icon('bars'),
                    onPressed= self.toggle_drawer),
                actions=[
                IconButton(
                    icon=Icon('bars'),
                    onPressed= self.toggle_end_drawer),
            ],
            ) if self.currentIndex == 0 else None,
            
            body=Body(
                child=body_content,
                ),  # Use the selected content
            drawer= drawer,
            endDrawer= end_drawer,
            bottomNavigationBar=BottomNavigationBar(
                items=[
                    BottomNavigationBarItem(icon=Icon('home'), label='Home'),
                    BottomNavigationBarItem(icon=Icon('gear'), label='Settings'),
                ],
                onTap= self.on_tab_selected,
                currentIndex=self.currentIndex,
                #fixedColor=Colors.color('blue'),
                backgroundColor=Colors.color('white'),
                elevation=10,
                iconSize=30,
                selectedFontSize=18,
                unselectedFontSize=14,
                selectedItemColor=Colors.color('blue'),
                unselectedItemColor=Colors.color('grey'),
                showSelectedLabels=True,
                showUnselectedLabels=False,
            ),
            bottomSheet=BottomSheet(
                child=Column(
                    children=[
                        Text("This is a BottomSheet"),
                        IconButton(
                            icon=Icon('minus'),
                            onPressed= self.hide_bottom_sheet
                            ),
                    ]
                ),
                height=300,
                backgroundColor=Colors.color("lightgrey"),
                enableDrag=True
            ),
            snackBar=snack_bar
        )

        self.framework.set_root(scaffold)

    def run(self):
        self.update_ui()
        self.framework.run(title='MyApp')
        Widget(framework= self.framework)

if __name__ == "__main__":
    app = MyApp()
    app.run()
"""