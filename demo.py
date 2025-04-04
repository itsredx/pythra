def scafold(drawer_width, end_drawer_width):
    left_drawer_width = drawer_width
    right_drawer_width = end_drawer_width

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Standard Drawers</title>
    <style>{css(left_drawer_width, right_drawer_width)}</style>
</head>
<body>
    <div class="body">
        <div class="app-bar">
            <button onclick="toggleDrawer('left')">Left Drawer</button>
            <button onclick="toggleDrawer('right')">Right Drawer</button>
        </div>

        <div class="drawer left" id="leftDrawer">
            <p>Left Drawer Content</p>
        </div>

        <div class="drawer right" id="rightDrawer">
            <p>Right Drawer Content</p>
        </div>

        <div class="content" id="content">
            <p>This is the main content area.This is the main content area.This is the main content area.This is the main content area.This is the main content area.This is the main content area.</p>
        </div>

        <div class="bottom-nav" id="bottomNav">
            <button>Home</button>
            <button>Search</button>
            <button>Profile</button>
        </div>
    </div>
    <script>
        const leftDrawer = document.getElementById('leftDrawer');
        const rightDrawer = document.getElementById('rightDrawer');
        const content = document.getElementById('content');
        const bottomNav = document.getElementById('bottomNav');
        const appBar = document.querySelector('.app-bar');

        function toggleDrawer(side) {{
            const drawer = side === 'left' ? leftDrawer : rightDrawer;
            const isOpen = drawer.classList.contains('open');

            if (isOpen) {{
                drawer.classList.remove('open');
                updateLayout();
            }} else {{
                drawer.classList.add('open');
                bottomNav.classList.add('hidden');
                updateLayout();
            }}

            if (!leftDrawer.classList.contains('open') && !rightDrawer.classList.contains('open')) {{
                bottomNav.classList.remove('hidden');
            }}
        }}

        function updateLayout() {{
            const leftOpen = leftDrawer.classList.contains('open');
            const rightOpen = rightDrawer.classList.contains('open');

            content.style.marginLeft = leftOpen ? '{left_drawer_width}px' : '0';
            content.style.marginRight = rightOpen ? '{right_drawer_width}px' : '0';
            appBar.style.marginLeft = leftOpen ? '{left_drawer_width}px' : '0';
            appBar.style.marginRight = rightOpen ? '{right_drawer_width}px' : '0';
        }}
    </script>
</body>
</html>
    """

def css(drawer_width, end_drawer_width):
    left_drawer_width = drawer_width
    right_drawer_width = end_drawer_width

    return f"""
    * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
        }}
        
        .body {{
            overflow: clip;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            height: 100vh;
            position: relative;
        }}

        .app-bar {{
            height: 60px;
            background-color: #6200ee;
            color: white;
            display: flex;
            align-items: center;
            padding: 0 20px;
            position: relative;
            transition: margin-left 0.3s, margin-right 0.3s;
        }}

        .drawer {{
            position: absolute;
            top: 0;
            bottom: 0;
            width: 250px;
            background-color: lightblue;
            z-index: 10;
            transition: transform 0.3s;
        }}

        .drawer.left {{
            left: 0;
            width: {left_drawer_width}px;
            transform: translateX(-100%);
            border-right: black;
            border-right-style: solid;
            border-right-width: 0.3px;
        }}

        .drawer.right {{
            right: 0;
            width: {right_drawer_width}px;
            transform: translateX(100%);
            border-left: black;
            border-left-style: solid;
            border-left-width: 0.3px;
        }}

        .drawer.open {{
            transform: translateX(0);
        }}

        .content {{
            flex: 1;
            padding: 20px;
            background-color: #f0f0f0;
            transition: margin-left 0.3s, margin-right 0.3s;
            overflow-y: auto;
        }}

        .bottom-nav {{
            height: 60px;
            background-color: #6200ee;
            position: absolute;
            left: 0px;
            right: 0px;
            bottom: 0px;
            color: white;
            display: flex;
            justify-content: space-around;
            align-items: center;
            transition: transform 0.3s;
        }}

        .bottom-nav.hidden {{
            transform: translateY(100%);
        }}
    """
html_file = '/home/red-x/Documents/pythra/web/demo.html'

print(scafold(300, 290))

with open(html_file, 'w') as f:
    f.write(scafold(300, 290))
    f.close()