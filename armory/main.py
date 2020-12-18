#!/usr/bin/env python
"""
Initiate the Kivy main loop.
"""

from typing import final

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader

# Debugging
from kivy.logger import Logger

@final
class TextInputPopup(Popup):
    """Popup that is created when clicking an inventory element."""
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super().__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text

        self.title = ""
        self.text_box = BoxLayout(orientation="vertical")
        self.text_input = TextInput(text=self.obj_text)

        self.buttons_box = BoxLayout(orientation="horizontal")

        self.save_button = Button(size_hint=(1, 0.2), text="Save changes")
        self.save_button.bind(on_press=self.save_button_press)
        self.cancel_button = Button(size_hint=(1, 0.2), text="Cancel changes")
        self.cancel_button.bind(on_press=self.dismiss)

        self.buttons_box.add_widget(self.save_button)
        self.buttons_box.add_widget(self.cancel_button)

        self.text_box.add_widget(self.text_input)
        self.text_box.add_widget(self.buttons_box)
        self.add_widget(self.text_box)

    def save_button_press(self, instance):
        """Called when clicking the save button."""
        self.obj.update_changes(self.text_input.text)
        self.dismiss()

@final
class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    """Add selection and focus behavior to the view"""

    def __init__(self, **kwargs):
        super(SelectableRecycleGridLayout, self).__init__(
            default_size=(0, 28), default_size_hint=(1, None),
            touch_multiselect=True, multiselect=True, cols=5,
            height=self.minimum_height, **kwargs)

@final
class SelectableButton(RecycleDataViewBehavior, Button):
    """Add selection support to the Button"""
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Truncate the text that is displayed on buttons
        self.text_size = (200, None)
        self.halign = "center"
        self.shorten_from = "right"
        self.shorten = True

        with self.canvas.before:
            if self.selected:
                Color(.0, 0.9, .1, .3, mode="rgba")
            else:
                Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)

    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes"""
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """Add selection on touch down"""
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
        return False

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view"""
        self.selected = is_selected

    def on_press(self):
        """Call when button is pressed."""
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, text):
        """Call when saving."""
        self.text = text

@final
class Armory(BoxLayout):
    """The starting point of the app."""
    items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Item header bar
        item_header = GridLayout(size_hint=(1, None), size_hint_y=None, height=25, cols=5)
        item_name = Label(text="Name", bold=True)
        item_reqs = Label(text="Requirements", bold=True)
        item_quality = Label(text="Quality", bold=True)
        item_location = Label(text="Location", bold=True)
        item_notes = Label(text="Notes", bold=True)
        item_header.add_widget(item_name)
        item_header.add_widget(item_reqs)
        item_header.add_widget(item_quality)
        item_header.add_widget(item_location)
        item_header.add_widget(item_notes)

        # Populate table
        self._get_items()

        # Item list
        item_list = BoxLayout()
        recycle_view = RecycleView()
        recycle_view.add_widget(SelectableRecycleGridLayout())
        recycle_view.data=[{"text": str(x)} for x in self.items]
        recycle_view.orientation = "vertical"
        recycle_view.viewclass = "SelectableButton"
        item_list.add_widget(recycle_view)

        self.add_widget(item_header)
        self.add_widget(item_list)

    def _get_items(self):
        """Populate the list of items with elements from the DB"""
        # Temporary DB mock data
        data = [["foo", "bar"] for x in range(40)]

        for row in data:
            for item in row:
                self.items.append(item)

@final
class TabbedArmory(TabbedPanel):
    """Create a tab per item type."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ring_tab = self._add_tab("Ring", Armory(), self)

        self._add_tab("Amulet", Armory(), self)
        self._add_tab("Badge", Armory(), self)
        self._add_tab("Cloak", Armory(), self)
        self._add_tab("Plate", Armory(), self)
        self._add_tab("Helmet", Armory(), self)
        self._add_tab("Gloves", Armory(), self)
        self._add_tab("Boots", Armory(), self)
        self._add_tab("Belt", Armory(), self)
        self._add_tab("Bracelets", Armory(), self)
        self._add_tab("Trousers", Armory(), self)
        self._add_tab("Shield", Armory(), self)
        self._add_tab("Skins", Armory(), self)

        self.default_tab = ring_tab

    def _add_tab(self, label, content, parent_widget):
        """Add a tab to the top panel."""
        new_tab = TabbedPanelHeader(text=label)
        new_tab.content = content
        parent_widget.add_widget(new_tab)
        return new_tab

@final
class ArmoryApp(App):
    """Main entry point into the Kivy main loop."""
    title = "Armory v0.1"

    def build(self):
        self.icon = "../assets/shield.ico"
        return TabbedArmory()

if __name__ == "__main__":
    ArmoryApp().run()
