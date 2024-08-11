import yaml
import os
from .base import Widget
from framework.styles import *
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
        padding_str = f'padding: {self.padding.to_css()};' if self.padding else ''
        margin_str = f'margin: {self.margin.to_css()};' if self.margin else ''
        width_str = f'width: {self.width}px;' if self.width else ''
        height_str = f'height: {self.height}px;' if self.height else ''
        color_str = f'background-color: {self.color};' if self.color else ''
        decoration_str = self.decoration.to_css() if self.decoration else ''
        foregroundDecoration_str = self.foregroundDecoration.to_css() if self.foregroundDecoration else ''
        alignment_str = self.alignment.to_css() if self.alignment else ''
        clip_str = f'overflow: hidden;' if self.clipBehavior else ''

        child_html = self.child.to_html() if self.child else ''

        return f"""
        <div style='position: relative; {self.constraints.to_css()} {alignment_str} {padding_str} {margin_str} {width_str} {height_str} {color_str} {decoration_str} {clip_str}'>
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
        text_align_str = self.textAlign if self.textAlign else ''

        if self.textAlign:
            style += f"text-align: {text_align_str};"
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
        onClick = f"onclick='handleClick(\"{self.onPressed}\")'" if self.onPressed else ""
        return f"""
        <button style="position: fixed; bottom: 16px; right: 16px; border-radius: 50%; width: 56px; height: 56px; background-color: #f50057; color: white; border: none; display: flex; justify-content: center; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.2);" {onClick}>
            {self.child.to_html() if self.child else ''}
        </button>
        """
 

class Column(Widget):
    def __init__(self, children=[], key=None, mainAxisAlignment=MainAxisAlignment.START, mainAxisSize= MainAxisSize.MAX, crossAxisAlignment=CrossAxisAlignment.CENTER, textDirection=TextDirection.LTR, verticalDirection= VerticalDirection.DOWN, textBaseline=TextBaseline.alphabetic):
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
        elif self.mainAxisSize == 'max':
            styles += "width: 100%;"

        return f"<div style='{styles}'>{children_html}</div>"



class Row(Widget):
    def __init__(self, children=[], key=None, mainAxisAlignment=MainAxisAlignment.START, mainAxisSize=MainAxisSize.MAX, crossAxisAlignment=CrossAxisAlignment.CENTER, textDirection=TextDirection.LTR, verticalDirection= VerticalDirection.DOWN, textBaseline = TextBaseline.alphabetic):
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
        elif self.mainAxisSize == 'max':
            styles += "width: 100%;"

        return f"<div style='{styles}'>{children_html}</div>"
        

class Image(Widget):
    def __init__(self, image, width=None, height=None, fit=ImageFit.CONTAIN, alignment='center'):
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
    def __init__(self, icon_name=None, custom_icon=None, size=24, color=None):
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
            color = f"color: {self.color};" if self.color != None else ''
            return f"<i class='fa fa-{self.icon_name}' style='font-size: {self.size}px; {color}'></i>"



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
    def __init__(self, title=None, actions=None, leading=None, backgroundColor=None, elevation=None, centerTitle=None, titleSpacing=None, pinned=False, bottom=None, shadowColor=Colors.rgba(0,0,0,0.2)):
        self.title = title
        self.actions = actions or []
        self.leading = leading
        self.backgroundColor = backgroundColor
        self.elevation = elevation
        self.centerTitle = centerTitle
        self.titleSpacing = titleSpacing
        self.shadowColor = shadowColor
        self.pinned = pinned
        self.bottom = bottom

    def to_html(self):
        pinned_style = 'position: fixed; width: 100%;' if self.pinned else 'position: relative;'
        app_bar_style = ""
        if self.backgroundColor:
            app_bar_style += f"background-color: {self.backgroundColor};"
        if self.elevation:
            app_bar_style += f"box-shadow: 0 {self.elevation}px 5px {self.shadowColor};"
        
        # Define height and ensure it affects layout
        app_bar_style += f"box-shadow: 0 6px 5px rgba(0, 0, 0, 0.2); height: 56px; display: flex; align-items: center; position: relative; z-index: 1;"

        leading_html = self.leading.to_html() if self.leading else ""
        title_html = self.title.to_html() if self.title else ""
        center_title = self.centerTitle.to_html() if self.centerTitle else ""
        actions_html = ''.join([action.to_html() for action in self.actions])

        bottom_html = self.bottom.to_html() if self.bottom else ""

        leading_css = f'margin-left: 16px;' if self.leading else ""
        action_css = f'margin-right: 16px;' if self.actions else ""
        title_spacing = self.titleSpacing if self.titleSpacing else 10

        return f"""
        <header style="{app_bar_style}">
            <div style="{leading_css}">{leading_html}</div>
            <div style="flex: 1; margin-left: {title_spacing}px;">{title_html}</div>
            <div style="flex: 1; text-align: center;">{center_title}</div>
            <div style="{action_css}">{actions_html}</div>
            {bottom_html}
        </header>
        """


class BottomNavigationBar(Widget):
    def __init__(self, 
                 items, 
                 onTap=None, 
                 currentIndex=0, 
                 fixedColor=None, 
                 backgroundColor= Colors.color("white"), 
                 elevation=10, 
                 iconSize=30, 
                 selectedFontSize=18, 
                 unselectedFontSize=14, 
                 selectedItemColor= Colors.color("blue"), 
                 unselectedItemColor=Colors.color("grey"), 
                 showSelectedLabels=True, 
                 showUnselectedLabels=False, 
                 landscapeLayout="centered"):
        self.items = items
        self.onTap = onTap
        self.currentIndex = currentIndex
        self.fixedColor = fixedColor
        self.backgroundColor = backgroundColor
        self.elevation = elevation
        self.iconSize = iconSize
        self.selectedFontSize = selectedFontSize
        self.unselectedFontSize = unselectedFontSize
        self.selectedItemColor = selectedItemColor
        self.unselectedItemColor = unselectedItemColor
        self.showSelectedLabels = showSelectedLabels
        self.showUnselectedLabels = showUnselectedLabels
        self.landscapeLayout = landscapeLayout

    def to_html(self):
        items_html = ''
        for index, item in enumerate(self.items):
            selected = index == self.currentIndex
            color = self.selectedItemColor if selected else self.unselectedItemColor
            font_size = self.selectedFontSize if selected else self.unselectedFontSize

            item.icon.size = self.iconSize

            item_html = item.to_html(selected=selected, showSelectedLabels = self.showSelectedLabels, showUnselectedLabels= self.showUnselectedLabels, fixedColor=self.fixedColor)
            item_style = f"color: {color}; font-size: {font_size}px; cursor: pointer; flex: 1;"
            items_html += f"<div onclick='handleClickOnTap(\"{self.onTap}\", {index})' style='{item_style}'>{item_html}</div>"

        return f"""
        <div id="bottomNav" style='height: 60px; background-color: {self.backgroundColor}; box-shadow: 0 -2px 10px rgba(0,0,0,0.2); display: flex; justify-content: center; align-items: center;  position: relative; z-index: 1;'>
            {items_html}
        </div>
        """


class BottomNavigationBarItem:
    def __init__(self, icon, label):
        self.icon = icon
        self.label = label

    def to_html(self, selected=False, showSelectedLabels=True, showUnselectedLabels=False, iconSize=30, fixedColor=None):
        # Set the color to fixedColor if provided, otherwise use default behavior
        color = fixedColor if fixedColor else None
        self.icon.color = color
        
        icon_html = self.icon.to_html()
        should_show_label = (selected and showSelectedLabels) or (not selected and showUnselectedLabels)
        should_color_label = (fixedColor and selected) or (not fixedColor and selected)
        label_color = fixedColor if should_color_label else '#aaa'
        label_html = f"<div style='color: {label_color};'>{self.label}</div>" if should_show_label else ''

        return f"<div style='text-align: center; '>{icon_html}{label_html}</div>"

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
                 backgroundColor=Colors.color('white'),
                 resizeToAvoidBottomInset=True,
                 extendBody=False,
                 extendBodyBehindAppBar=False,
                 drawerDragStartBehavior=None,
                 drawerEdgeDragWidth=None,
                 drawerEnableOpenDragGesture=True,
                 endDrawerEnableOpenDragGesture=True,
                 drawerScrimColor=Colors.rgba(0, 0, 0, 0.5),
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
        extend_body_style = "position: absolute; top: 56; bottom: 0; left: 0; right: 0;" if self.extendBody or self.extendBodyBehindAppBar else ""
        body_margin_top = "margin-top: 0px;" if self.appBar and not self.extendBodyBehindAppBar else ""

        
        if body_html != '':
            if drawer_html != '':
                drawer_width = self.drawer.width + self.drawer.padding.to_int_horizontal() + self.drawer.borderRight.to_int()
                
                margin_left = f'-{drawer_width}px'
                
            else:
                margin_left = '0px'

            if end_drawer_html != '':
                end_drawer_width = self.endDrawer.width + self.endDrawer.padding.to_int_horizontal() + self.endDrawer.borderLeft.to_int()
                margin_right = f'-{end_drawer_width}px'
        
            else:
                margin_right = '0px'


        return f"""
        <div id="scaffold" style="flex: 1; display: flex; flex-direction: column; height: 100vh; {background_color_style}">
            {appBar_html}
            <div id="container" style="flex: 1; display: flex; overflow: hidden; position: relative; ">
            {drawer_html}
            <div id="body" style='flex: 1; overflow-y: auto; padding: 20px; margin-left: {margin_left}; margin-right: {margin_right}; transition: margin-left 0.3s ease;'>
            {body_html}
            </div>
            {end_drawer_html}
            </div>
            {floating_action_button_html}
            {bottom_sheet_html}
            <div style="position: absolute; bottom: 0; width: 100%; display: flex; justify-content: {self.persistentFooterAlignment};">
                {footer_buttons_html}
            </div>
            {bottom_navigation_bar_html}
        </div>
        
        """

class Body(Widget):
    def __init__(self, child=None):
        self.child = child

    def to_html(self):
        child_html = self.child.to_html() if self.child else ''
        
        return f"{child_html}"



class Divider(Widget):
    def __init__(self, height=1, margin=EdgeInsets.symmetric(8,0), color=Colors.hex('#ccc'), border=BorderStyle.NONE):
        self.height = height
        self.margin = margin
        self.color = color
        self.border = border
    def to_html(self):
        return f"""
        <hr style="height: {self.height}px; background-color: {self.color}; border: {self.border}; margin: {self.margin.to_css()};">
        """

class Drawer(Widget):
    def __init__(self, child, width=250, divider=None, borderRight= BorderSide(width=0.1, style=BorderStyle.SOLID), elevation='', padding=EdgeInsets.all(20), backgroundColor=Colors.color('white')):
        self.child = child
        self.width = width
        self.padding = padding
        self.borderRight = borderRight
        self.elevation = elevation
        self.divider = divider
        self.backgroundColor = backgroundColor
        self.is_open = False

    def to_html(self):
        divider = self.divider.to_html() if self.divider else ''
        drawer_width = self.width + self.padding.to_int_horizontal() + self.borderRight.to_int()
        border = self.borderRight.border_to_css() if self.borderRight else ''

        return f"""
        <div id="drawer" style="width: {self.width}px; padding: {self.padding.to_css()}; height: 100%; background: {self.backgroundColor}; box-shadow:{self.elevation}; overflow-y: auto; border-right: {border}; transform: translateX(-{drawer_width}px); transition: transform 0.3s ease;">
            {self.child.to_html()}{divider}
        </div>
        """

    def toggle(self):
        self.is_open = not self.is_open
        return self.is_open



class EndDrawer(Widget):
    def __init__(self, child, width=250, divider=None, borderLeft= BorderSide(width=0.1, style=BorderStyle.SOLID), elevation='', padding=EdgeInsets.all(20), backgroundColor=Colors.color('white')):
        self.child = child
        self.width = width
        self.padding = padding
        self.borderLeft = borderLeft
        self.elevation = elevation
        self.divider = divider
        self.backgroundColor = backgroundColor
        self.is_open = False

    def to_html(self):
        divider = self.divider.to_html() if self.divider else ''
        end_drawer_width = self.width + self.padding.to_int_horizontal() + self.borderLeft.to_int()
        border = self.borderLeft.border_to_css() if self.borderLeft else ''
        return f"""
        <div id="endDrawer" style="width: {self.width}px; padding: {self.padding.to_css()}; height: 100%; background: {self.backgroundColor}; overflow-y: auto; box-shadow:{self.elevation}; border-left: {border}; transform: translateX({end_drawer_width}px); transition: transform 0.3s ease;">
            {self.child.to_html()}{divider}
        </div>
        """

    def toggle(self):
        self.is_open = not self.is_open
        return self.is_open



class ListTile(Widget):
    def __init__(self, leading=None, title=None, subtitle=None, onTap=None):
        self.leading = leading
        self.title = title
        self.subtitle = subtitle
        self.onTap = onTap

    def to_html(self):
        leading_html = self.leading.to_html() if self.leading else ""
        title_html = self.title.to_html() if self.title else ""
        subtitle_html = self.subtitle.to_html() if self.subtitle else ""
        onClick = f'onclick="handleClick(\'{self.onTap}\')"' if self.onTap else ""

        return f"""
        <div class="list-tile" style="display: flex; align-items: center; padding: 10px; cursor: pointer;" {onClick}>
            <div style="margin-right: 10px;">{leading_html}</div>
            <div>
                <div>{title_html}</div>
                <div style="color: grey;">{subtitle_html}</div>
            </div>
        </div>
        """

