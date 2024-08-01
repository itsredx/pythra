import yaml
import os
from .base import Widget
from framework.styles import EdgeInsets, Alignment, BoxConstraints, Colors, BoxDecoration, ClipBehavior, MainAxisAlignment, CrossAxisAlignment, TextStyle, ButtonStyle, Axis, ScrollPhysics, Overflow, StackFit, TextDirection
from framework.config import Config

config = Config()
assets_dir = config.get('assets_dir', 'assets')

class Widget:
    def to_html(self):
        raise NotImplementedError("Each widget must implement the to_html method.")


# framework/widgets.py

class Container(Widget):
    def __init__(self, child=None, padding=None, color=None, decoration=None, foregroundDecoration=None, width=None, height=None, constraints=None, margin=None, transform=None, alignment=None, clipBehavior=None):
        self.child = child
        self.padding = padding
        self.color = color
        self.decoration = decoration
        self.foregroundDecoration = foregroundDecoration
        self.width = width
        self.height = height
        self.constraints = constraints
        self.margin = margin
        self.transform = transform
        self.alignment = alignment
        self.clipBehavior = clipBehavior

    def to_html(self):
        padding_str = self.padding.to_css() if self.padding else ''
        margin_str = self.margin.to_css() if self.margin else ''
        width_str = f'width: {self.width}px;' if self.width else ''
        height_str = f'height: {self.height}px;' if self.height else ''
        color_str = f'background-color: {self.color};' if self.color else ''
        decoration_str = self.decoration.to_css() if self.decoration else ''
        foregroundDecoration_str = self.foregroundDecoration.to_css() if self.foregroundDecoration else ''
        alignment_str = self.alignment.to_css() if self.alignment else ''
        
        clip_str = f'overflow: hidden;' if self.clipBehavior else ''

        child_html = self.child.to_html() if self.child else ''

        return f"""
        <div style='position: relative; {alignment_str} {padding_str} {margin_str} {width_str} {height_str} {color_str} {decoration_str} {clip_str}'>
            {child_html}
            <div style='{foregroundDecoration_str} position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none;'></div>
        </div>
        """


class Text(Widget):
    def __init__(self, data, key=None, style=None, textAlign=None, overflow=None):
        self.data = data
        self.key = key
        self.style = style or TextStyle()
        self.textAlign = textAlign
        self.overflow = overflow

    def to_html(self):
        style = self.style.to_css()

        if self.textAlign:
            style += f"text-align: {self.textAlign};"
        if self.overflow:
            style += f"overflow: {self.overflow};"

        return f"<p style='{style}'>{self.data}</p>"



class TextButton(Widget):
    def __init__(self, child, onPressed=None, style=None):
        self.child = child
        self.onPressed = onPressed
        self.style = style or ButtonStyle()

    def to_html(self):
        style = self.style.to_css()
        button_id = f'text_button_{id(self)}'
        return f"<button id='{button_id}' style='{style}' onclick='handleClick(\"{self.onPressed}\")'>{self.child.to_html()}</button>"


class ElevatedButton(Widget):
    def __init__(self, child, onPressed=None, style=None):
        self.child = child
        self.onPressed = onPressed
        self.style = style or ButtonStyle()

    def to_html(self):
        style = self.style.to_css()
        button_id = f'elevated_button_{id(self)}'
        return f"<button id='{button_id}' style='{style}' onclick='handleClick(\"{self.onPressed}\")'>{self.child.to_html()}</button>"


class IconButton(Widget):
    def __init__(self, child, onPressed=None, style=None):
        self.child = child
        self.onPressed = onPressed
        self.style = style or ButtonStyle()

    def to_html(self):
        button_id = f"icon_button_{id(self)}"
        style = self.style.to_css()
        child_html = self.child.to_html() if isinstance(self.child, Widget) else self.child

        return f"""
        <button id='{button_id}' style='{style}' onclick='handleClick("{self.onPressed}")'>
            {child_html}
        </button>
        """

class FloatingActionButton(Widget):
    def __init__(self, child=None, onPressed=None, key=None):
        self.child = child
        self.onPressed = onPressed
        self.key = key

    def to_html(self):
        onClick = f"onclick='{self.onPressed}'" if self.onPressed else ""
        return f"""
        <button style="position: fixed; bottom: 16px; right: 16px; border-radius: 50%; width: 56px; height: 56px; background-color: #f50057; color: white; border: none; display: flex; justify-content: center; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.2); {onClick}">
            {self.child.to_html() if self.child else ''}
        </button>
        """
 

class Column(Widget):
    def __init__(self, children=[], key=None, mainAxisAlignment=MainAxisAlignment.START, mainAxisSize='max', crossAxisAlignment=CrossAxisAlignment.CENTER, textDirection='ltr', verticalDirection='down', textBaseline='alphabetic'):
        self.children = children
        self.key = key
        self.mainAxisAlignment = mainAxisAlignment
        self.mainAxisSize = mainAxisSize
        self.crossAxisAlignment = crossAxisAlignment
        self.textDirection = textDirection
        self.verticalDirection = verticalDirection
        self.textBaseline = textBaseline

    def to_html(self):
        children_html = ''.join([child.to_html() for child in self.children])

        # CSS styles based on properties
        styles = (
            f"display: flex; flex-direction: column; "
            f"justify-content: {self.mainAxisAlignment}; "
            f"align-items: {self.crossAxisAlignment}; "
            f"direction: {self.textDirection}; "
            f"vertical-align: {self.textBaseline};"
        )

        if self.mainAxisSize == 'min':
            styles += "height: auto;"

        return f"<div style='{styles}'>{children_html}</div>"



class Row(Widget):
    def __init__(self, children=[], key=None, mainAxisAlignment=MainAxisAlignment.START, mainAxisSize='max', crossAxisAlignment=CrossAxisAlignment.CENTER, textDirection='ltr', verticalDirection='down', textBaseline='alphabetic'):
        self.children = children
        self.key = key
        self.mainAxisAlignment = mainAxisAlignment
        self.mainAxisSize = mainAxisSize
        self.crossAxisAlignment = crossAxisAlignment
        self.textDirection = textDirection
        self.verticalDirection = verticalDirection
        self.textBaseline = textBaseline

    def to_html(self):
        children_html = ''.join([child.to_html() for child in self.children])

        # CSS styles based on properties
        styles = (
            f"display: flex; flex-direction: row; "
            f"justify-content: {self.mainAxisAlignment}; "
            f"align-items: {self.crossAxisAlignment}; "
            f"direction: {self.textDirection}; "
            f"vertical-align: {self.textBaseline};"
        )

        if self.mainAxisSize == 'min':
            styles += "width: auto;"

        return f"<div style='{styles}'>{children_html}</div>"
        

class Image(Widget):
    def __init__(self, image, width=None, height=None, fit='contain', alignment='center'):
        self.image = image
        self.width = width
        self.height = height
        self.fit = fit
        self.alignment = alignment

    def to_html(self):
        src = self.image.get_source()
        style = f"object-fit: {self.fit}; width: {self.width}px; height: {self.height}px; display: flex; justify-content: center; align-items: center;"
        return f"<img src='{src}' style='{style}' />"

class AssetImage:
    def __init__(self, file_name):
        # Use the local server to serve assets
        self.src = f'http://localhost:8000/{assets_dir}/{file_name}'

    def get_source(self):
        return self.src

class NetworkImage:
    def __init__(self, url):
        self.src = url

    def get_source(self):
        return self.src


class Icon(Widget):
    def __init__(self, icon_name=None, custom_icon=None, size=24, color='black'):
        self.icon_name = icon_name
        self.custom_icon = custom_icon
        self.size = size
        self.color = color

    def to_html(self):
        if self.custom_icon:
            src = AssetImage(self.custom_icon).get_source()
            return f"<img src='{src}' style='width: {self.size}px; height: {self.size}px; color: {self.color};' />"
        else:
            # Use a CDN for predefined icons, e.g., FontAwesome
            return f"<i class='fa fa-{self.icon_name}' style='font-size: {self.size}px; color: {self.color};'></i>"



class ListView(Widget):
    def __init__(self, children, padding=None, scrollDirection=Axis.VERTICAL, reverse=False, primary=True, physics=ScrollPhysics.ALWAYS_SCROLLABLE, shrinkWrap=False, itemExtent=None, cacheExtent=None, semanticChildCount=None):
        self.children = children
        self.padding = padding or EdgeInsets.all(0)
        self.scrollDirection = scrollDirection
        self.reverse = reverse
        self.primary = primary
        self.physics = physics
        self.shrinkWrap = shrinkWrap
        self.itemExtent = itemExtent
        self.cacheExtent = cacheExtent
        self.semanticChildCount = semanticChildCount

    def to_html(self):
        scroll_direction_style = "flex-direction: column;" if self.scrollDirection == Axis.VERTICAL else "flex-direction: row;"
        reverse_style = "flex-direction: column-reverse;" if self.reverse else ""
        primary_style = "overflow-y: auto;" if self.scrollDirection == Axis.VERTICAL and self.primary else "overflow-x: auto;" if self.scrollDirection == Axis.HORIZONTAL and self.primary else ""
        padding_style = f"padding: {self.padding.to_css()};"
        
        physics_style = ""
        if self.physics == ScrollPhysics.BOUNCING:
            physics_style = "overflow: scroll; -webkit-overflow-scrolling: touch;"
        elif self.physics == ScrollPhysics.CLAMPING:
            physics_style = "overflow: hidden;"

        item_extent_style = f"flex-basis: {self.itemExtent}px;" if self.itemExtent else ""
        cache_extent_style = f"scroll-margin-top: {self.cacheExtent}px;" if self.cacheExtent else ""

        children_html = ''.join([f"<div style='flex: none; {item_extent_style}'>{child.to_html()}</div>" for child in self.children])

        semantic_child_count_attr = f"aria-setsize='{self.semanticChildCount}'" if self.semanticChildCount else ""

        return f"""
        <div style="display: flex; {scroll_direction_style} {reverse_style} {primary_style} {padding_style} {physics_style} {cache_extent_style}; height: 100%; width: 100%;" {semantic_child_count_attr}>
            {children_html}
        </div>
        """

class GridView(Widget):
    def __init__(self, children, padding=None, scrollDirection=Axis.VERTICAL, reverse=False, primary=True, physics=ScrollPhysics.ALWAYS_SCROLLABLE, shrinkWrap=False, crossAxisCount=2, mainAxisSpacing=0, crossAxisSpacing=0, childAspectRatio=1.0):
        self.children = children
        self.padding = padding or EdgeInsets.all(0)
        self.scrollDirection = scrollDirection
        self.reverse = reverse
        self.primary = primary
        self.physics = physics
        self.shrinkWrap = shrinkWrap
        self.crossAxisCount = crossAxisCount
        self.mainAxisSpacing = mainAxisSpacing
        self.crossAxisSpacing = crossAxisSpacing
        self.childAspectRatio = childAspectRatio

    def to_html(self):
        scroll_direction_style = "flex-direction: column;" if self.scrollDirection == Axis.VERTICAL else "flex-direction: row;"
        reverse_style = "flex-direction: column-reverse;" if self.reverse else ""
        primary_style = "overflow-y: auto;" if self.scrollDirection == Axis.VERTICAL and self.primary else "overflow-x: auto;" if self.scrollDirection == Axis.HORIZONTAL and self.primary else ""
        padding_style = f"padding: {self.padding.to_css()};"
        grid_template_columns = f"repeat({self.crossAxisCount}, 1fr)"
        grid_gap = f"{self.mainAxisSpacing}px {self.crossAxisSpacing}px"
        
        # Apply scroll physics styles
        physics_style = ""
        if self.physics == ScrollPhysics.BOUNCING:
            physics_style = "overflow: scroll; -webkit-overflow-scrolling: touch;"
        elif self.physics == ScrollPhysics.CLAMPING:
            physics_style = "overflow: hidden;"

        children_html = ''.join([f"<div style='flex: 1; aspect-ratio: {self.childAspectRatio};'>{child.to_html()}</div>" for child in self.children])

        return f"""
        <div style="display: flex; {scroll_direction_style} {reverse_style} {primary_style} {padding_style} {physics_style}; height: 100%; width: 100%;">
            <div style="display: grid; grid-template-columns: {grid_template_columns}; gap: {grid_gap}; width: 100%;">
                {children_html}
            </div>
        </div>
        """
          
class Stack(Widget):
    def __init__(self, children, alignment=Alignment.top_left(), textDirection=TextDirection.LTR, fit=StackFit.loose, clipBehavior=ClipBehavior.NONE, overflow=Overflow.VISIBLE, key=None):
        self.children = children
        self.alignment = alignment
        self.textDirection = textDirection
        self.fit = fit
        self.clipBehavior = clipBehavior
        self.overflow = overflow
        self.key = key

    def to_html(self):
        alignment_style = self.alignment.to_css()
        text_direction_style = f"direction: {self.textDirection};"
        fit_style = "width: 100%; height: 100%;" if self.fit == StackFit.expand else ""
        clip_style = ""
        if self.clipBehavior == ClipBehavior.HARD_EDGE:
            clip_style = "overflow: hidden;"
        elif self.clipBehavior == ClipBehavior.ANTI_ALIAS or self.clipBehavior == ClipBehavior.ANTI_ALIAS_WITH_SAVE_LAYER:
            clip_style = "overflow: hidden; clip-path: inset(0% round 0.5%);"

        overflow_style = f"overflow: {self.overflow.value};"

        children_html = ''.join([child.to_html() for child in self.children])

        return f"""
        <div style="position: relative; {alignment_style} {text_direction_style} {fit_style} {clip_style} {overflow_style}">
            {children_html}
        </div>
        """
        
class Positioned(Widget):
    def __init__(self, child, top=None, right=None, bottom=None, left=None):
        self.child = child
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def to_html(self):
        top_style = f"top: {self.top}px;" if self.top is not None else ""
        right_style = f"right: {self.right}px;" if self.right is not None else ""
        bottom_style = f"bottom: {self.bottom}px;" if self.bottom is not None else ""
        left_style = f"left: {self.left}px;" if self.left is not None else ""

        return f"""
        <div style="position: absolute; {top_style} {right_style} {bottom_style} {left_style}">
            {self.child.to_html()}
        </div>
        """
        

class Expanded(Widget):
    def __init__(self, child, flex=1, key=None):
        self.child = child
        self.flex = flex
        self.key = key

    def to_html(self):
        return f"<div style='flex: {self.flex};'>{self.child.to_html()}</div>"



class Spacer(Widget):
    def __init__(self, flex=1, key=None):
        self.flex = flex
        self.key = key

    def to_html(self):
        return f"<div style='flex: {self.flex};'></div>"
        
        

class AppBar(Widget):
    def __init__(self, title=None, actions=None, leading=None, backgroundColor=None, elevation=None, bottom=None):
        self.title = title
        self.actions = actions or []
        self.leading = leading
        self.backgroundColor = backgroundColor
        self.elevation = elevation
        self.bottom = bottom

    def to_html(self):
        app_bar_style = ""
        if self.backgroundColor:
            app_bar_style += f"background-color: {self.backgroundColor};"
        if self.elevation:
            app_bar_style += f"box-shadow: 0 {self.elevation}px 5px rgba(0, 0, 0, 0.2);"
        
        # Define height and ensure it affects layout
        app_bar_style += "height: 56px; display: flex; align-items: center;"

        leading_html = self.leading.to_html() if self.leading else ""
        title_html = self.title.to_html() if self.title else ""
        actions_html = ''.join([action.to_html() for action in self.actions])

        bottom_html = self.bottom.to_html() if self.bottom else ""

        return f"""
        <header style="{app_bar_style}">
            <div style="margin-left: 16px;">{leading_html}</div>
            <div style="flex: 1; text-align: center;">{title_html}</div>
            <div style="margin-right: 16px;">{actions_html}</div>
            {bottom_html}
        </header>
        """


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
        
        # Placeholder for drawer handling logic (e.g., show/hide behavior, drawer edge drag width)
        
        # Placeholder for background color handling
        background_color_style = f"background-color: {self.backgroundColor};"

        # Handling body extension behind app bar or body
        extend_body_style = "position: absolute; top: 0; bottom: 0; left: 0; right: 0;" if self.extendBody or self.extendBodyBehindAppBar else ""

        # Adjust body margin if AppBar is present and not extending body behind it
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
        """


class Body(Widget):
    def __init__(self, child=None):
        self.child = child

    def to_html(self):
        return f"<div style='flex: 1;'>{self.child.to_html() if self.child else ''}</div>"

        

class Drawer(Widget):
    def __init__(self, children, key=None):
        self.children = children
        self.key = key

    def to_html(self):
        children_html = ''.join([child.to_html() for child in self.children])
        return f"""
        <div style="position: fixed; top: 0; left: 0; width: 250px; height: 100%; background-color: #ffffff; box-shadow: 2px 0 5px rgba(0,0,0,0.5);">
            {children_html}
        </div>
        """
