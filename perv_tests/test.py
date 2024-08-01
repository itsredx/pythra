class Scaffold(Widget):
    def __init__(self, 
                 appBar=None, 
                 body=None, 
                 floatingActionButton=None, 
                 bottomNavigationBar=None, 
                 drawer=None, 
                 endDrawer=None, 
                 bottomSheet=None, 
                 persistentFooterButtons=None,
                 backgroundColor='white',
                 resizeToAvoidBottomInset=True,
                 extendBody=False,
                 extendBodyBehindAppBar=False,
                 drawerDragStartBehavior=None,
                 drawerEdgeDragWidth=None,
                 drawerEnableOpenDragGesture=True,
                 endDrawerEnableOpenDragGesture=True,
                 drawerScrimColor='rgba(0, 0, 0, 0.5)',
                 onDrawerChanged=None,
                 onEndDrawerChanged=None,
                 persistentFooterAlignment=MainAxisAlignment.CENTER,
                 primary=True,
                 key=None):
        self.appBar = appBar
        self.body = body
        self.floatingActionButton = floatingActionButton
        self.bottomNavigationBar = bottomNavigationBar
        self.drawer = drawer
        self.endDrawer = endDrawer
        self.bottomSheet = bottomSheet
        self.persistentFooterButtons = persistentFooterButtons
        self.backgroundColor = backgroundColor
        self.resizeToAvoidBottomInset = resizeToAvoidBottomInset
        self.extendBody = extendBody
        self.extendBodyBehindAppBar = extendBodyBehindAppBar
        self.drawerDragStartBehavior = drawerDragStartBehavior
        self.drawerEdgeDragWidth = drawerEdgeDragWidth
        self.drawerEnableOpenDragGesture = drawerEnableOpenDragGesture
        self.endDrawerEnableOpenDragGesture = endDrawerEnableOpenDragGesture
        self.drawerScrimColor = drawerScrimColor
        self.onDrawerChanged = onDrawerChanged
        self.onEndDrawerChanged = onEndDrawerChanged
        self.persistentFooterAlignment = persistentFooterAlignment
        self.primary = primary
        self.key = key

    def to_html(self):
        appBar_html = self.appBar.to_html() if self.appBar else ""
        body_html = self.body.to_html() if self.body else ""
        floating_action_button_html = self.floatingActionButton.to_html() if self.floatingActionButton else ""
        bottom_navigation_bar_html = self.bottomNavigationBar.to_html() if self.bottomNavigationBar else ""
        drawer_html = self.drawer.to_html() if self.drawer else ""
        end_drawer_html = self.endDrawer.to_html() if self.endDrawer else ""
        bottom_sheet_html = self.bottomSheet.to_html() if self.bottomSheet else ""
        footer_buttons_html = ''.join([button.to_html() for button in (self.persistentFooterButtons or [])])

        background_color_style = f"background-color: {self.backgroundColor};"
        extend_body_style = "position: absolute; top: 0; bottom: 0; left: 0; right: 0;" if self.extendBody or self.extendBodyBehindAppBar else ""
        body_margin_top = "margin-top: 0px;" if self.appBar and not self.extendBodyBehindAppBar else ""

        return f"""
        <div style="position: relative; height: 100%; width: 100%; {background_color_style}">
            {drawer_html}
            {appBar_html}
            <div style="position: relative; {extend_body_style} {body_margin_top}">
                {body_html}
            </div>
            {floating_action_button_html}
            {bottom_sheet_html}
            <div style="position: absolute; bottom: 0; width: 100%; display: flex; justify-content: {self.persistentFooterAlignment};">
                {footer_buttons_html}
            </div>
            {bottom_navigation_bar_html}
            {end_drawer_html}
        </div>
        <script>
            function toggleDrawer() {
                var drawer = document.getElementById("drawer");
                var scrim = document.getElementById("drawer-scrim");
                if (drawer.classList.contains("drawer-closed")) {
                    drawer.classList.remove("drawer-closed");
                    drawer.classList.add("drawer-open");
                    scrim.classList.remove("scrim-hidden");
                    scrim.classList.add("scrim-visible");
                } else {
                    drawer.classList.remove("drawer-open");
                    drawer.classList.add("drawer-closed");
                    scrim.classList.remove("scrim-visible");
                    scrim.classList.add("scrim-hidden");
                }
            }

            document.getElementById("drawer-scrim").addEventListener("click", toggleDrawer);
        </script>
        <style>
            .drawer-closed {
                transform: translateX(-100%);
            }
            .drawer-open {
                transform: translateX(0);
            }
            .scrim-hidden {
                display: none;
            }
            .scrim-visible {
                display: block;
            }
        </style>
        """