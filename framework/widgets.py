# framework/widgets.py
import uuid
import yaml
import os
from .api import Api
from .base import Widget
from .styles import *
from .config import Config

config = Config()
assets_dir = config.get('assets_dir', 'assets')
port = config.get('assets_server_port')
Colors = Colors()



class Container(Widget):
    def __init__(self, child=None, padding=None, color=None, decoration=None, foregroundDecoration=None, width=None, height=None, constraints=None, margin=None, transform=None, alignment=None, clipBehavior=None):
        super().__init__(widget_id=None)
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
        
  
    
        self.add_child(self.child) if self.child else None # Register the child widget with the framework


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
        <div id="{self.widget_id()}" style='position: relative; {self.constraints.to_css()} {alignment_str} {padding_str} {margin_str} {width_str} {height_str} {color_str} {decoration_str} {clip_str}'>
            {child_html}
            <div style='{foregroundDecoration_str} position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none;'></div>
        </div>
        """

class Text(Widget):
    def __init__(self, data, key=None, style=None, textAlign=None, overflow=None, widget_id=None):
        super().__init__(widget_id)
        self.data = data
        self.key = key
        self.style = style or TextStyle()
        self.textAlign = textAlign
        self.overflow = overflow

    
    def get_children(self):
        return []  # SizedBox doesn't have children, so return an empty list

    def remove_all_children(self):
        pass


    def to_html(self):
        style = self.style.to_css()
        text_align_str = self.textAlign if self.textAlign else ''

        if self.textAlign:
            style += f"text-align: {text_align_str};"
        if self.overflow:
            style += f"overflow: {self.overflow};"

        return f"<p id='{self.widget_id()}' style='{style} margin-top: 0px; margin-bottom: 0px;'>{self.data}</p>"



class TextButton(Widget):
    def __init__(self, child, onPressed=None, style=None):
        super().__init__(widget_id=None)
        self.child = child
        self.onPressed = onPressed
        self.style = style or ButtonStyle()

        self.api = Api()
        self.onPressedName = self.onPressed.__name__ if self.onPressed else ''

        self.add_child(self.child) if self.child else None # Register the child widget with the framework    

    def to_html(self):
        style = self.style.to_css()
        button_id = f'{self.widget_id()}'
        self.api.register_callback(self.onPressedName, self.onPressed)
        return f"<button id='{button_id}' style='{style}' onclick='handleClick(\"{self.onPressedName}\")'>{self.child.to_html()}</button>"


class ElevatedButton(Widget):
    def __init__(self, child, onPressed=None, style=None):
        super().__init__(widget_id=None)
        self.child = child
        self.onPressed = onPressed
        self.style = style or ButtonStyle()

        self.api = Api()
        self.onPressedName = self.onPressed.__name__ if self.onPressed else ''

        self.add_child(self.child) if self.child else None # Register the child widget with the framework
   

    def to_html(self):
        style = self.style.to_css()
        button_id = f'{self.widget_id()}'
        self.api.register_callback(self.onPressedName, self.onPressed)
        return f"<button id='{button_id}' style='{style}' onclick='handleClick(\"{self.onPressedName}\")'>{self.child.to_html()}</button>"


class IconButton(Widget):
    def __init__(self, icon, onPressed=None, iconSize=None, style=None):
        super().__init__(widget_id=None)
        self.child = icon
        self.onPressed = onPressed
        self.iconSize = iconSize
        self.style = style or ButtonStyle()
        self.api = Api()

        

        self.onPressedName = self.onPressed.__name__ if self.onPressed else ''

        self.add_child(self.child) if self.child else None # Register the child widget with the framework
    


    def to_html(self):
        button_id = f"{self.widget_id()}"
        style = self.style.to_css()
        self.child.size = self.iconSize if self.iconSize and isinstance(self.child, Widget) else 16
        child_html = self.child.to_html() if isinstance(self.child, Widget) else self.child

        
        self.api.register_callback(self.onPressedName, self.onPressed)

        return f"""
        <button id='{button_id}' style='{style} background-color: transparent;' onclick='handleClick("{self.onPressedName}")'>
            {child_html}
        </button>
        """

class FloatingActionButton(Widget):
    def __init__(self, child=None, onPressed=None, key=None):
        super().__init__(widget_id=None)
        self.child = child
        self.onPressed = onPressed
        self.key = key

        self.api = Api()
        self.onPressedName = self.onPressed.__name__ if self.onPressed else ''

        self.add_child(self.child) if self.child else None # Register the child widget with the framework

    def to_html(self):
        self.api.register_callback(self.onPressedName, self.onPressed)

        onClick = f"onclick='handleClick(\"{self.onPressedName}\")'" if self.onPressed else ""
        
        return f"""
        <button id='{self.widget_id()}' style="position: fixed; bottom: 16px; right: 16px; border-radius: 50%; width: 56px; height: 56px; background-color: #f50057; color: white; border: none; display: flex; justify-content: center; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.2);" {onClick}>
            {self.child.to_html() if self.child else ''}
        </button>
        """
 

class Column(Widget):
    def __init__(self, children=[], key=None, mainAxisAlignment=MainAxisAlignment.START, mainAxisSize= MainAxisSize.MAX, crossAxisAlignment=CrossAxisAlignment.CENTER, textDirection=TextDirection.LTR, verticalDirection= VerticalDirection.DOWN, textBaseline=TextBaseline.alphabetic, widget_id=None):
        self.children = children
        super().__init__(widget_id=None)
        self.key = key
        self.mainAxisAlignment = mainAxisAlignment
        self.mainAxisSize = mainAxisSize
        self.crossAxisAlignment = crossAxisAlignment
        self.textDirection = textDirection
        self.verticalDirection = verticalDirection
        self.textBaseline = textBaseline

        

        # Loop over self.children and add them to the widget tree
        for child in self.children:
            self.add_child(child) if child else None # Use the add_child method to manage parent-child relationships

        #("The list of added children: ", self.get_children())  # Check if children were added properly
       

    

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

        return f"<div id='{self.widget_id()}' style='{styles}'>{children_html}</div>"



class Row(Widget):
    def __init__(self, children=[], key=None, mainAxisAlignment=MainAxisAlignment.START, mainAxisSize=MainAxisSize.MAX, crossAxisAlignment=CrossAxisAlignment.CENTER, textDirection=TextDirection.LTR, verticalDirection= VerticalDirection.DOWN, textBaseline = TextBaseline.alphabetic):
        super().__init__(widget_id=None)
        self.children = children
        self.key = key
        self.mainAxisAlignment = mainAxisAlignment
        self.mainAxisSize = mainAxisSize
        self.crossAxisAlignment = crossAxisAlignment
        self.textDirection = textDirection
        self.verticalDirection = verticalDirection
        self.textBaseline = textBaseline


        # Loop over self.children and add them to the widget tree
        for child in self.children:
            self.add_child(child) if child else None # Use the add_child method to manage parent-child relationships

        #print("The list of added children: ", self.get_children())  # Check if children were added properly

    

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

        return f"<div id='{self.widget_id()}' style='{styles}'>{children_html}</div>"
        

class Image(Widget):
    def __init__(self, image, width=None, height=None, fit=ImageFit.CONTAIN, alignment='center'):
        super().__init__(widget_id=None)
        self.image = image
        self.width = width
        self.height = height
        self.fit = fit
        self.alignment = alignment


        self.add_child(self.image) if self.image else None

    

    def to_html(self):
        src = self.image.get_source()
        style = f"object-fit: {self.fit}; width: {self.width}px; height: {self.height}px; display: flex; justify-content: center; align-items: center;"
        return f"<img id='{self.widget_id()}' src='{src}' style='{style}' />"

class AssetImage:
    
    def __init__(self, file_name):
        # Use the local server to serve assets
        self.src = f'http://localhost:{port}/{assets_dir}/{file_name}'

    def get_source(self):
        return self.src

class NetworkImage:
    def __init__(self, url):
        self.src = url

    def get_source(self):
        return self.src


class Icon(Widget):
    def __init__(self, icon_name=None, custom_icon=None, size=16, color=None):
        super().__init__(widget_id=None)
        self.icon_name = icon_name
        self.custom_icon = custom_icon
        self.size = size
        self.color = color
        
    def get_children(self):
        return []  # Icon doesn't have children, so return an empty list

    def remove_all_children(self):
        pass


    def to_html(self):
        if self.custom_icon:
            src = AssetImage(self.custom_icon).get_source()
            return f"<img src='{src}' style='width: {self.size}px; height: {self.size}px; color: {self.color};' />"
        else:
            # Use a CDN for predefined icons, e.g., FontAwesome
            color = f"color: {self.color};" if self.color != None else ''
            return f"<i id='{self.widget_id()}' class='fa fa-{self.icon_name}' style='font-size: {self.size}px; {color}'></i>"



class ListView(Widget):
    def __init__(self, children, padding=None, scrollDirection=Axis.VERTICAL, reverse=False, primary=True, physics=ScrollPhysics.ALWAYS_SCROLLABLE, shrinkWrap=False, itemExtent=None, cacheExtent=None, semanticChildCount=None):
        super().__init__(widget_id=None)
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

        # Loop over self.children and add them to the widget tree
        for child in self.children:
            self.add_child(child) if child else None  # Use the add_child method to manage parent-child relationships

        #print("The list of added children: ", self.get_children())  # Check if children were added properly



    


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
        <div id="{self.widget_id()}" style="display: flex; {scroll_direction_style} {reverse_style} {primary_style} {padding_style} {physics_style} {cache_extent_style}; height: 100%; width: 100%;" {semantic_child_count_attr}>
            {children_html}
        </div>
        """

class GridView(Widget):
    def __init__(self, children, padding=None, scrollDirection=Axis.VERTICAL, reverse=False, primary=True, physics=ScrollPhysics.ALWAYS_SCROLLABLE, shrinkWrap=False, crossAxisCount=2, mainAxisSpacing=0, crossAxisSpacing=0, childAspectRatio=1.0):
        super().__init__(widget_id=None)
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


    
        # Loop over self.children and add them to the widget tree
        for child in self.children:
            self.add_child(child) if child else None  # Use the add_child method to manage parent-child relationships

        #print("The list of added children: ", self.get_children())  # Check if children were added properly



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
        <div id="{self.widget_id()}" style="display: flex; {scroll_direction_style} {reverse_style} {primary_style} {padding_style} {physics_style}; height: 100%; width: 100%;">
            <div style="display: grid; grid-template-columns: {grid_template_columns}; gap: {grid_gap}; width: 100%;">
                {children_html}
            </div>
        </div>
        """
          
class Stack(Widget):
    def __init__(self, children, alignment=Alignment.top_left(), textDirection=TextDirection.LTR, fit=StackFit.loose, clipBehavior=ClipBehavior.NONE, overflow=Overflow.VISIBLE, key=None):
        super().__init__(widget_id=None)
        self.children = children
        self.alignment = alignment
        self.textDirection = textDirection
        self.fit = fit
        self.clipBehavior = clipBehavior
        self.overflow = overflow
        self.key = key


        # Loop over self.children and add them to the widget tree
        for child in self.children:
            self.add_child(child)  if child else None # Use the add_child method to manage parent-child relationships

        #print("The list of added children: ", self.get_children())  # Check if children were added properly
    


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
        <div id="{self.widget_id()}" style="position: relative; {alignment_style} {text_direction_style} {fit_style} {clip_style} {overflow_style}">
            {children_html}
        </div>
        """
        
class Positioned(Widget):
    def __init__(self, child, top=None, right=None, bottom=None, left=None):
        super().__init__(widget_id=None)
        self.child = child
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


        self.add_child(self.child) if self.child else None # Use the add_child method to manage parent-child relationships

    


    def to_html(self):
        top_style = f"top: {self.top}px;" if self.top is not None else ""
        right_style = f"right: {self.right}px;" if self.right is not None else ""
        bottom_style = f"bottom: {self.bottom}px;" if self.bottom is not None else ""
        left_style = f"left: {self.left}px;" if self.left is not None else ""

        return f"""
        <div id='{self.widget_id()}' style="position: absolute; {top_style} {right_style} {bottom_style} {left_style}">
            {self.child.to_html()}
        </div>
        """
        

class Expanded(Widget):
    def __init__(self, child, flex=1, key=None):
        super().__init__(widget_id=None)
        self.child = child
        self.flex = flex
        self.key = key


        self.add_child(self.child) if self.child else None# Register the child widget with the framework



    def to_html(self):
        return f"<div id='{self.widget_id()}' style='flex: {self.flex};'>{self.child.to_html()}</div>"



class Spacer(Widget):
    def __init__(self, flex=1, key=None):
        super().__init__(widget_id=None)
        self.flex = flex
        self.key = key
    
    def get_children(self):
        return []  # SizedBox doesn't have children, so return an empty list

    def remove_all_children(self):
        pass


    def widget_id(self):
        return 'spacer'


    def to_html(self):
        return f"<div id='{self.widget_id()}' style='flex: {self.flex};'></div>"
        
class SizedBox(Widget):
    def __init__(self, height=0, width=0):
        super().__init__(widget_id=None)
        self.height = height
        self.width = width

    def get_children(self):
        return []  # SizedBox doesn't have children, so return an empty list

    def remove_all_children(self):
        pass

    def widget_id(self):
        return 'sizedBox'

    def to_html(self):
        return f"<div id='{self.widget_id()}' style='height: {self.height}px; width: {self.width}px;'></div>"

class AppBar(Widget):
    def __init__(self, title=None, actions=None, leading=None, backgroundColor=None, elevation=None, centerTitle=None, titleSpacing=None, pinned=False, bottom=None, shadowColor=Colors.rgba(0,0,0,0.2)):
        super().__init__(widget_id=None)
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
        
        self.add_child(self.title) if self.title else None
        self.add_child(self.leading) if self.leading else None

        for action in self.actions:
            self.add_child(action) if action else None
    



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
        <header id="{self.widget_id()}" style="{app_bar_style}">
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
                 backgroundColor= Colors.white , 
                 elevation=10, 
                 iconSize=30, 
                 selectedFontSize=18, 
                 unselectedFontSize=14, 
                 selectedItemColor= Colors.blue , 
                 unselectedItemColor= Colors.grey ,
                 showSelectedLabels=True, 
                 showUnselectedLabels=False, 
                 landscapeLayout="centered"):
        super().__init__(widget_id=None)
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

        self.api = Api()
        self.onTapName = self.onTap.__name__ if self.onTap else ''



        for item in self.items:
            self.add_child(item) if item else None


    def to_html(self):
        self.api.register_callback(self.onTapName, self.onTap)
        items_html = ''
        for index, item in enumerate(self.items):
            selected = index == self.currentIndex
            color = self.selectedItemColor if selected else self.unselectedItemColor
            font_size = self.selectedFontSize if selected else self.unselectedFontSize

            item.icon.size = self.iconSize
            

            item_html = item.to_html(selected=selected, showSelectedLabels = self.showSelectedLabels, showUnselectedLabels= self.showUnselectedLabels, fixedColor=self.fixedColor)
            item_style = f"color: {color}; font-size: {font_size}px; cursor: pointer; flex: 1;"
            items_html += f"<div onclick='handleClickOnTap(\"{self.onTapName}\", {index})' style='{item_style}'>{item_html}</div>"

        return f"""
        <div id="{self.widget_id()}" style='height: 60px; background-color: {self.backgroundColor}; box-shadow: 0 -2px 10px rgba(0,0,0,0.2); display: flex; justify-content: center; align-items: center;  position: relative; z-index: 1;'>
            {items_html}
        </div>
        """


class BottomNavigationBarItem(Widget):
    def __init__(self, icon, label):
        
        super().__init__(widget_id=None)
        self.icon = icon
        self.label = label


        self.add_child(self.icon) if self.icon else None
        self.add_child(self.label) if self.label else None
    


    def to_html(self, selected=False, showSelectedLabels=True, showUnselectedLabels=False, iconSize=30, fixedColor=None):
        # Set the color to fixedColor if provided, otherwise use default behavior
        color = fixedColor if fixedColor else None
        self.icon.color = color
        
        icon_html = self.icon.to_html()
        should_show_label = (selected and showSelectedLabels) or (not selected and showUnselectedLabels)
        should_color_label = (fixedColor and selected) or (not fixedColor and selected)
        label_color = fixedColor if should_color_label else '#aaa'
        label = self.label
        #label.style()
        label_html = f"<div style='color: {label_color};'>{self.label.to_html()}</div>" if should_show_label else ''

        return f"<div id='{self.widget_id()}' style='text-align: center; '>{icon_html}{label_html}</div>"

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
                 snackBar=None,
                 backgroundColor=Colors.white,
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
        super().__init__(widget_id=None)
        self.appBar = appBar
        self.body = body
        self.floatingActionButton = floatingActionButton
        self.bottomNavigationBar = bottomNavigationBar
        self.drawer = drawer
        self.endDrawer = endDrawer
        self.bottomSheet = bottomSheet
        self.persistentFooterButtons = persistentFooterButtons
        self.snackBar = snackBar
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


        children = [
            self.appBar, 
            self.body, 
            self.floatingActionButton,
            self.bottomNavigationBar,
            self.drawer,
            self.endDrawer,
            self.bottomSheet,
            self.snackBar
            ]

        for child in children:
            self.add_child(child) if child else None
        
        
        


    def to_html(self):
        appBar_html = self.appBar.to_html() if self.appBar else ""
        body_html = self.body.to_html() if self.body else ""
        body_id = self.body._id if self.body else ""
        floating_action_button_html = self.floatingActionButton.to_html() if self.floatingActionButton else ""
        bottom_navigation_bar_html = self.bottomNavigationBar.to_html() if self.bottomNavigationBar else ""
        drawer_html = self.drawer.to_html() if self.drawer else ""
        end_drawer_html = self.endDrawer.to_html() if self.endDrawer else ""
        bottom_sheet_html = self.bottomSheet.to_html() if self.bottomSheet else ""
        snack_bar_html = self.snackBar.to_html() if self.snackBar else ""
        footer_buttons_html = ''.join([button.to_html() for button in (self.persistentFooterButtons or [])])

        background_color_style = f"background-color: {self.backgroundColor};"
        extend_body_style = "position: absolute; top: 56; bottom: 0; left: 0; right: 0;" if self.extendBody or self.extendBodyBehindAppBar else ""
        body_margin_top = "margin-top: 0px;" if self.appBar and not self.extendBodyBehindAppBar else ""

        
        if body_html != '':
            if drawer_html != '':
                drawer_width = self.drawer.width + self.drawer.padding.to_int_horizontal() + self.drawer.borderRight.to_int()
                if self.drawer.is_open:
                    margin_left = '0px'
                else:
                    margin_left = f'-{drawer_width}px'

            else:
                margin_left = '0px'
                print("Drawer is None")

            if end_drawer_html != '':
                end_drawer_width = self.endDrawer.width + self.endDrawer.padding.to_int_horizontal() + self.endDrawer.borderLeft.to_int()
                
                if self.endDrawer.is_open:
                    margin_right = '0px'
                else:
                    margin_right = f'-{end_drawer_width}px'

            else:
                margin_right = '0px'

        


        return f"""
        <div id="{self.widget_id()}" style="flex: 1; display: flex; flex-direction: column; height: 100vh; {background_color_style}">
            {appBar_html}
            <div id="container" style="flex: 1; display: flex; overflow: hidden; position: relative; ">
            {drawer_html}
            <div id="{body_id}" style='flex: 1; overflow-y: auto; padding: 20px; margin-left: {margin_left}; margin-right: {margin_right}; transition: margin-left 0.3s ease;'>
            {body_html}
            </div>
            {end_drawer_html}
            </div>
            {floating_action_button_html}
            {bottom_sheet_html}
            {snack_bar_html}
            <div style="position: absolute; bottom: 0; width: 100%; display: flex; justify-content: {self.persistentFooterAlignment};">
                {footer_buttons_html}
            </div>
            {bottom_navigation_bar_html}
        </div>
        
        """

class Body(Widget):
    def __init__(self, child=None):
        super().__init__(widget_id=None)
        self.child = child
        self.id = self.widget_id()

        self.add_child(self.child) if self.child else None # Register the child widget with the framework
        
    def id(self):
        #print("Body: ", self.widget_id())
        return self.widget_id()

    def to_html(self):
        child_html = self.child.to_html() if self.child else ''
        
        return f"{child_html}"



class Divider(Widget):
    def __init__(self, height=1, margin=EdgeInsets.symmetric(8,0), color=Colors.hex('#ccc'), border=BorderStyle.NONE):
        super().__init__(widget_id=None)
        self.height = height
        self.margin = margin
        self.color = color
        self.border = border

    def get_children(self):
        return []  # SizedBox doesn't have children, so return an empty list

    def remove_all_children(self):
        pass

    


    def to_html(self):
        return f"""
        <hr  id="{self.widget_id()}" style="height: {self.height}px; background-color: {self.color}; border: {self.border}; margin: {self.margin.to_css()};">
        """

class Drawer(Widget):

    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If an instance doesn't exist, create one
            cls._instance = super(Drawer, cls).__new__(cls)
        return cls._instance  # Return the singleton instance

    def __init__(self, child, width=250, divider=None, borderRight= BorderSide(width=0.1, style=BorderStyle.SOLID), elevation='', padding=EdgeInsets.all(20), backgroundColor=Colors.white):
        # Only initialize the instance once
        if not hasattr(self, 'initialized'):
            super().__init__(widget_id=None)
            self.child = child
            self.width = width
            self.padding = padding
            self.borderRight = borderRight
            self.elevation = elevation
            self.divider = divider
            self.backgroundColor = backgroundColor
            self.is_open = False
            self.add_child(self.child) if self.child else None
            self.initialized = True  # Mark the instance as initialized


        self.add_child(self.child) if self.child else None# Register the child widget with the framework
    


    def to_html(self):
        
        divider = self.divider.to_html() if self.divider else ''
        drawer_width = self.width + self.padding.to_int_horizontal() + self.borderRight.to_int()
        border = self.borderRight.border_to_css() if self.borderRight else ''
        drawer_width = '0px' if self.is_open else f'-{drawer_width}' 
        #print(drawer_width, self.is_open)

        return f"""
        <div id="{self.widget_id()}" style="width: {self.width}px; padding: {self.padding.to_css()}; height: 100%; background: {self.backgroundColor}; box-shadow:{self.elevation}; overflow-y: auto; border-right: {border}; transform: translateX({drawer_width}px); transition: transform 0.3s ease;">
            {self.child.to_html()}{divider}
        </div>
        """

    def toggle(self, bool=False):
        self.is_open = bool

        return self.is_open



class EndDrawer(Widget):
    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If an instance doesn't exist, create one
            cls._instance = super(EndDrawer, cls).__new__(cls)
        return cls._instance  # Return the singleton instance

    def __init__(self, child, width=250, divider=None, borderLeft= BorderSide(width=0.1, style=BorderStyle.SOLID), elevation='', padding=EdgeInsets.all(20), backgroundColor=Colors.white):
        # Only initialize the instance once
        if not hasattr(self, 'initialized'):
            super().__init__(widget_id=None)
            self.child = child
            self.width = width
            self.padding = padding
            self.borderLeft = borderLeft
            self.elevation = elevation
            self.divider = divider
            self.backgroundColor = backgroundColor
            self.is_open = False
            self.initialized = True  # Mark the instance as initialized


        self.add_child(self.child) if self.child else None# Register the child widget with the framework
    


    def to_html(self):
        divider = self.divider.to_html() if self.divider else ''
        end_drawer_width = self.width + self.padding.to_int_horizontal() + self.borderLeft.to_int()
        end_drawer_width = '0px' if self.is_open else end_drawer_width
        border = self.borderLeft.border_to_css() if self.borderLeft else ''
        return f"""
        <div id="{self.widget_id()}" style="width: {self.width}px; padding: {self.padding.to_css()}; height: 100%; background: {self.backgroundColor}; overflow-y: auto; box-shadow:{self.elevation}; border-left: {border}; transform: translateX({end_drawer_width}px); transition: transform 0.3s ease;">
            {self.child.to_html()}{divider}
        </div>
        """

    def toggle(self, bool=False):
        self.is_open = bool
        
        return self.is_open



class BottomSheet(Widget):
    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If an instance doesn't exist, create one
            cls._instance = super(BottomSheet, cls).__new__(cls)
        return cls._instance  # Return the singleton instance
        
    def __init__(self, child, height=300, backgroundColor=Colors.white, elevation='', padding=EdgeInsets.all(20), enableDrag=True):
         # Only initialize the instance once
        if not hasattr(self, 'initialized'):
            super().__init__(widget_id=None)
            self.child = child
            self.height = height
            self.backgroundColor = backgroundColor
            self.elevation = elevation
            self.padding = padding
            self.enableDrag = enableDrag
            self.is_open = False
            self.show_barrier = False
            self.barrier_color = Colors.rgba(0, 0, 0, 0.5) # Modal barrier color (overlay)
            self.initialized = True  # Mark the instance as initialized



            self.add_child(self.child) if self.child else None# Register the child widget with the framework


    def to_html(self):
        # Barrier for background dimming (optional)
        barrier_html = f'<div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: {self.barrier_color}; z-index: 899;"></div>' if self.is_open else ''
        barrier_html = barrier_html if self.show_barrier else ''
        drag_behavior = 'cursor: grab;' if self.enableDrag else ''
        translate = '0px' if self.is_open else '100%'
        return f"""
        {barrier_html} 
        <div id="{self.widget_id()}" style="position: fixed; left: 0; bottom: 0; z-index: 900; width: 100%; height: {self.height}px; padding: {self.padding.to_css()}; background-color: {self.backgroundColor}; box-shadow:{self.elevation}; transform: translateY({translate}); transition: transform 0.3s ease; {drag_behavior}">
            {self.child.to_html()}
        </div>
        """


    def toggle(self, bool=False):
        self.is_open = bool
        
        return self.is_open

class Center(Widget):
    def __init__(self, child):
        super().__init__(widget_id=None)
        self.child = child



        self.add_child(self.child) if self.child else None# Register the child widget with the framework    


    def to_html(self):
        return f"""
        <div id="{self.widget_id()}" style="display: flex; justify-content: center; align-items: center; height: 100%;">
            {self.child.to_html()}
        </div>
        """



class ListTile(Widget):
    def __init__(self, leading=None, title=None, subtitle=None, onTap=None):
        super().__init__(widget_id=None)
        self.leading = leading
        self.title = title
        self.subtitle = subtitle
        self.onTap = onTap

        self.api = Api()
        self.onTapName = self.onTap.__name__ if self.onTap else ''



        children = [
            self.leading,
            self.title,
            self.subtitle
        ]

        for child in children:
            self.add_child(child) if child else None# Register the child widget with the framework

    def to_html(self):
        self.api.register_callback(self.onTapName, self.onTap)

        leading_html = self.leading.to_html() if self.leading else ""
        title_html = self.title.to_html() if self.title else ""
        subtitle_html = self.subtitle.to_html() if self.subtitle else ""
        onClick = f'onclick="handleClick(\'{self.onTapName}\')"' if self.onTap else ""

        return f"""
        <div id="{self.widget_id()}" class="list-tile" style="display: flex; align-items: center; padding: 10px; cursor: pointer;" {onClick}>
            <div style="margin-right: 10px;">{leading_html}</div>
            <div>
                <div>{title_html}</div>
                <div style="color: grey;">{subtitle_html}</div>
            </div>
        </div>
        """




class SnackBar(Widget):
    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If an instance doesn't exist, create one
            cls._instance = super(SnackBar, cls).__new__(cls)
        return cls._instance  # Return the singleton instance


    def __init__(self, content, action=None, duration=3000, backgroundColor=Colors.grey, padding=EdgeInsets.symmetric(horizontal=24, vertical=16)):
         # Only initialize the instance once
        if not hasattr(self, 'initialized'):    
            super().__init__(widget_id=None)
            self.content = content
            self.action = action
            self.duration = duration
            self.backgroundColor = backgroundColor
            self.padding = padding
            self.is_open = False
            self.initialized = True  # Mark the instance as initialized


            children = [
                self.content,
                self.action,
            ]
        
            for child in children:
                self.add_child(child) if child else None# Register the child widget with the framework

    def to_html(self):
        action_html = self.action.to_html() if self.action else ""
        display_style = "flex" if self.is_open else "none"
        return f"""
        <div id="{self.widget_id()}" 
        style="display: {display_style}; 
        position: fixed; 
        bottom: 0; left: 0; 
        width: calc(100% - 48px); 
        padding: {self.padding.to_css()}; 
        background-color: {self.backgroundColor}; 
        box-shadow: 0px -2px 10px rgba(0, 0, 0, 0.3); 
        z-index: 999; 
        justify-content: space-between; 
        align-items: center;">
            <div>{self.content.to_html()}</div>
            {action_html}
        </div>
        """


    def toggle(self, bool=False):
        self.is_open = bool
        
        return self.is_open

class SnackBarAction(Widget):
    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If an instance doesn't exist, create one
            cls._instance = super(SnackBarAction, cls).__new__(cls)
        return cls._instance  # Return the singleton instance


    def __init__(self, label, onPressed, textColor=Colors.blue):
        # Only initialize the instance once
        if not hasattr(self, 'initialized'): 
            super().__init__(widget_id=None)
            self.label = label
            self.onPressed = onPressed
            self.textColor = textColor

            self.api = Api()
            self.onPressedName = self.onPressed.__name__ if self.onPressed else ''

            self.add_child(self.label) if self.label else None

    

    def to_html(self):
        self.api.register_callback(self.onPressedName, self.onPressed)

        return f"""
        <button id="{self.widget_id()}" 
        onclick="handleClick(\'{self.onPressedName}\')" 
        style="background: none; 
        border: none; 
        color: {self.textColor}; 
        font-size: 14px; 
        cursor: pointer;">
            {self.label.to_html()}
        </button>
        """


class Placeholder(Widget):
    def __init__(self, 
                 color=Colors.gray, 
                 stroke_width=2, 
                 height=100, 
                 width=100, 
                 child=None):
        super().__init__(widget_id=None)
        self.color = color
        self.stroke_width = stroke_width
        self.height = height
        self.width = width
        self.child = child

        if self.child:
            self.add_child(self.child)

    def to_html(self):
        if self.child:
            return self.child.to_html()
        else:
            return f"""
            <div id="{self.widget_id()}" style="
                height: {self.height}px;
                width: {self.width}px;
                border: {self.stroke_width}px dashed {self.color};
                display: flex;
                justify-content: center;
                align-items: center;
            ">
                <p style="
                color: {self.color};
                 font-size: 12px;
                 ">Placeholder</p>
            </div>
            """

class Padding(Widget):
    def __init__(self, padding=EdgeInsets.all(10), child=None):
        super().__init__(widget_id=None)
        self.padding = padding
        self.child = child

        if self.child:
            self.add_child(self.child)

    def to_html(self):
        child_html = self.child.to_html() if self.child else ''
        return f"""
        <div id="{self.widget_id()}" 
        style="padding: {self.padding.to_css()};">
            {child_html}
        </div>
        """

class Align(Widget):
    def __init__(self, alignment=Alignment.center(), child=None):
        super().__init__(widget_id=None)
        self.alignment = alignment
        self.child = child

        if self.child:
            self.add_child(self.child)

    def to_html(self):
        child_html = self.child.to_html() if self.child else ''
        return f"""
        <div id="{self.widget_id()}" 
        style="display: flex; 
        justify-content: {self.alignment.horizontal}; 
        align-items: {self.alignment.vertical}; 
        height: 100%; 
        width: 100%;">
            {child_html}
        </div>
        """


class AspectRatio(Widget):
    def __init__(self, aspect_ratio, child=None):
        super().__init__(widget_id=None)
        self.aspect_ratio = aspect_ratio
        self.child = child

        if self.child:
            self.add_child(self.child)

    def to_html(self):
        child_html = self.child.to_html() if self.child else ''
        
        # Aspect ratio calculation for CSS: padding-bottom is used to maintain aspect ratio
        padding_bottom = 100 / self.aspect_ratio

        return f"""
        <div id="{self.widget_id()}" 
        style="position: relative; 
        width: 100%; 
        padding-bottom: {padding_bottom}%; 
        height: 0; overflow: hidden;">
            <div style="position: absolute; 
            top: 0; left: 0; width: 100%; height: 100%;">
                {child_html}
            </div>
        </div>
        """

class FittedBox(Widget):
    def __init__(self, fit=BoxFit.CONTAIN, alignment=Alignment.center(), child=None):
        super().__init__(widget_id=None)
        self.fit = fit
        self.alignment = alignment
        self.child = child

        if self.child:
            self.add_child(self.child)

    def to_html(self):
        alignment_css = self.alignment.to_css()
        child_html = self.child.to_html() if self.child else ''

        # Using BoxFit values directly
        object_fit = self.fit

        return f"""
        <div id="{self.widget_id()}" 
        style="width: 100%; height: 100%; {alignment_css};">
            <div style="flex: 0 0 auto; object-fit: {object_fit};">
                {child_html}
            </div>
        </div>
        """

class FractionallySizedBox(Widget):
    def __init__(self, widthFactor=None, heightFactor=None, alignment=Alignment.center(), child=None):
        super().__init__(widget_id=None)
        self.widthFactor = widthFactor
        self.heightFactor = heightFactor
        self.alignment = alignment
        self.child = child

        if self.child:
            self.add_child(self.child)

    def to_html(self):
        alignment_css = self.alignment.to_css()

        # Calculate the width and height percentages based on the factors
        width = f"{self.widthFactor * 100}%" if self.widthFactor is not None else 'auto'
        height = f"{self.heightFactor * 100}%" if self.heightFactor is not None else 'auto'
        
        child_html = self.child.to_html() if self.child else ''

        return f"""
        <div id="{self.widget_id()}" 
        style="display: flex; 
        {alignment_css}; 
        width: 100%; height: 100%;">
            <div style="width: {width}; height: {height};">
                {child_html}
            </div>
        </div>
        """


class Flex(Widget):
    def __init__(self, 
                 direction=Axis.HORIZONTAL, 
                 mainAxisAlignment=MainAxisAlignment.START, 
                 crossAxisAlignment=CrossAxisAlignment.START, 
                 children=None, 
                 padding=None):
        super().__init__()
        self.direction = direction
        self.mainAxisAlignment = mainAxisAlignment
        self.crossAxisAlignment = crossAxisAlignment
        self.children = children if children is not None else []
        self.padding = padding if padding is not None else EdgeInsets.all(0)

        if self.children:
            for child in self.children:
                self.add_child(child)
        
    def to_html(self):
        direction_css = 'row' if self.direction == Axis.HORIZONTAL else 'column'
        
        # CSS for main axis and cross axis alignment
        justify_content = self.mainAxisAlignment
        align_items = self.crossAxisAlignment
        
        # Add padding to the Flex container
        padding_css = self.padding.to_css()
        
        # Generate the CSS for the Flex container
        container_css = f"""display: flex; 
        flex-direction: {direction_css}; 
        justify-content: {justify_content}; 
        align-items: {align_items}; 
        padding: {padding_css};"""
        
        # Build HTML for each child
        children_html = ''.join([child.render() for child in self.children])
        
        return f'<div style="{container_css}">{children_html}</div>'


class Wrap(Widget):
    def __init__(self, 
                 direction=Axis.HORIZONTAL, 
                 alignment=MainAxisAlignment.START, 
                 crossAxisAlignment=CrossAxisAlignment.START,
                 runAlignment=MainAxisAlignment.START,
                 spacing=0,
                 runSpacing=0,
                 clipBehavior=ClipBehavior.NONE,
                 children=None):
        self.direction = direction
        self.alignment = alignment
        self.crossAxisAlignment = crossAxisAlignment
        self.runAlignment = runAlignment
        self.spacing = spacing
        self.runSpacing = runSpacing
        self.clipBehavior = clipBehavior
        self.children = children or []


        if self.children:
            for child in self.children:
                self.add_child(child)
    
   

    def to_html(self):
        styles = []
        # Flex properties for wrapping
        flex_direction = 'row' if self.direction == Axis.HORIZONTAL else 'column'
        styles.append(f"display: flex; flex-wrap: wrap; flex-direction: {flex_direction};")
        
        # Main Axis Alignment
        styles.append(f"justify-content: {self.alignment};")
        
        # Cross Axis Alignment
        styles.append(f"align-items: {self.crossAxisAlignment};")
        
        # Run Alignment (applies to multi-row or multi-column layout)
        # In CSS, justify-content applies similarly to the "runAlignment"
        styles.append(f"align-content: {self.runAlignment};")
        
        # Spacing (gap between items)
        styles.append(f"gap: {self.spacing}px;")
        
        # Run Spacing (spacing between lines or rows of items)
        # CSS does not directly support run-spacing, so we may have to adjust for this manually later
        styles.append(f"row-gap: {self.runSpacing}px;" if self.direction == Axis.HORIZONTAL else f"column-gap: {self.runSpacing}px;")
        
        # Clip Behavior
        if self.clipBehavior:
            overflow_css = "overflow: hidden;" if self.clipBehavior != ClipBehavior.NONE else ""
            styles.append(overflow_css)
        
        css = " ".join(styles)
        children_html = "".join([child.to_html() for child in self.children])
        return f'<div style="{css}">{children_html}</div>'



class Dialog(Widget):

    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If an instance doesn't exist, create one
            cls._instance = super(Dialog, cls).__new__(cls)
        return cls._instance  # Return the singleton instance

    def __init__(self,
                 title=None,
                 content=None,
                 actions=None,
                 title_alignment=TextAlign.center(),  # Allows title alignment customization
                 title_padding=EdgeInsets.all(10),  # Padding around the title
                 content_padding=EdgeInsets.all(5),  # Padding around the content
                 dialog_shape=BorderRadius.all(10),  # Custom shape (border radius)
                 elevation=8,  # Shadow depth for elevation
                 background_color=Colors.hex("#fff"),  # Background color
                 barrier_color=Colors.rgba(0, 0, 0, 0.5),  # Modal barrier color (overlay)
                 padding=EdgeInsets.all(20)):  # Padding inside the dialog

        # Only initialize the instance once
        if not hasattr(self, 'initialized'):
            super().__init__(widget_id=None)
            self.title = title
            self.content = content
            self.actions = actions or []
            self.title_alignment = title_alignment
            self.title_padding = title_padding
            self.content_padding = content_padding
            self.dialog_shape = dialog_shape
            self.elevation = elevation
            self.background_color = background_color
            self.barrier_color = barrier_color
            self.padding = padding

            if self.content:
                self.add_child(self.content)
                self.add_child(self.title)
            for action in self.actions:
                self.add_child(action)

            self.initialized = True  # Mark the instance as initialized

    def to_html(self):
        # Title HTML
        title_html = f'<div style="text-align: {self.title_alignment.to_css()}; padding: {self.title_padding.to_css()};">{self.title.to_html()}</div>' if self.title else ""
        
        # Content HTML
        content_html = f'<div style="padding: {self.content_padding.to_css()}; margin-top: 4px;">{self.content.to_html()}</div>' if self.content else ""
        
        # Actions (buttons, etc.)
        actions_html = "".join([action.to_html() for action in self.actions])

        # Calculate box-shadow based on elevation for the dialog
        box_shadow = f"0 {self.elevation}px {self.elevation * 2}px rgba(0, 0, 0, 0.2)"
        
        # Dialog CSS
        dialog_css = (
            f"{self.dialog_shape.to_css()}"  # Dialog shape (border-radius)
            f"background-color: {self.background_color};"
            f"padding: {self.padding.to_css()};"
            f"position: fixed; top: 50%; left: 50%;"
            f"transform: translate(-50%, -50%);"
            f"box-shadow: {box_shadow};"  # Elevation (shadow)
            f"max-width: 330px; min-width: 180px;"
            f"z-index: 1000;"
        )

        # Barrier for background dimming (optional)
        barrier_html = f'''<div style="position: fixed; 
        top: 0; left: 0; width: 100vw; 
        height: 100vh; background-color: {self.barrier_color}; 
        z-index: 999;"></div>'''

        # Full dialog HTML
        return f'''
        {barrier_html}  <!-- Barrier to block interaction outside the dialog -->
        <div style="{dialog_css}">
            {title_html}
            {content_html}
            <div class="dialog-actions" 
            style="margin-top: 20px;">
            {actions_html}
            </div>
        </div>
        '''



"""
class Dialog(Widget):

    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If an instance doesn't exist, create one
            cls._instance = super(Dialog, cls).__new__(cls)
        return cls._instance  # Return the singleton instance
    def __init__(
            self,
            title=None, 
            content=None, 
            actions=None, 
            ):
         # Only initialize the instance once
        if not hasattr(self, 'initialized'):    
            super().__init__(widget_id=None)
            self.title = title
            self.content = content
            self.actions = actions or []
            self.color = color=Colors.hex("#fff")
            self.border = BorderSide(color=Colors.hex("#000"), style=BorderStyle.SOLID, width=1, borderRadius=5)
            self.initialized = True  # Mark the instance as initialized

            if self.content:
                self.add_child(self.content)
                self.add_child(self.title)
            for action in self.actions:
                self.add_child(action)

    def css(self):
        
        
        # Additional CSS for modal display
        modal_css = (
            f"{self.border.to_css()}"
            f"background-color: {self.color};"
            "padding: 15px;"
            "position: fixed; "
            "top: 50%; left: 50%; "
            "transform: translate(-50%, -50%); "
            "box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); "
            "z-index: 1000;"
        )
        
        return f"{modal_css}"

    def to_html(self):
        # Title HTML
        title_html = self.title.to_html() if self.title else ""
        
        # Content HTML
        content_html = f'<div style="margin-top: 4px;">{self.content.to_html()}</div>' if self.content else ""
        
        # Actions (buttons, etc.)
        actions_html = "".join([action.to_html() for action in self.actions])

        # Full dialog HTML
        dialog_css = self.css()
        return f'''
        <div style="{dialog_css}">
            {title_html}
            {content_html}
            <div class="dialog-actions">{actions_html}</div>
        </div>
        '''


"""