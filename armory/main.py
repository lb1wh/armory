#!/usr/bin/env python
"""
Initiate the Kivy main loop.
"""

from typing import final

import storage
import ui
import utils

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty, BooleanProperty

# Debugging
from kivy.logger import Logger


@final
class Armory(BoxLayout):
    """The starting point of the app."""
    items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        config = utils.read_config()

        # Armor item button bar
        armor_button_bar = self._create_button_bar(config["armor"])

        # Weapon button bar
        weapon_button_bar = self._create_button_bar(config["weapons"])

        # Item header bar
        item_header = BoxLayout(size_hint=(1, None), size_hint_y=None, height=25)
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

        # Populate item table - default item view
        armor_button_bar.children[0].trigger_action()

        # Item list
        item_list = BoxLayout()
        recycle_view = RecycleView()
        recycle_view.add_widget(ui.SelectableRecycleGridLayout())
        recycle_view.data=[{"text": str(x)} for x in self.items]
        recycle_view.orientation = "vertical"
        recycle_view.viewclass = "SelectableButton"
        item_list.add_widget(recycle_view)

        self.add_widget(armor_button_bar)
        self.add_widget(weapon_button_bar)
        self.add_widget(item_header)
        self.add_widget(item_list)

    def _get_items(self, instance):
        """Populate the list of items with elements from the DB"""
        item_type = instance.text.lower()

        # Temporary DB mock data
        data = [["foo", "bar"] for x in range(40)]

        for row in data:
            for item in row:
                self.items.append(item)

    def _create_button_bar(self, items):
        """Create a bar with buttons for given item types."""
        item_button_bar = BoxLayout(size_hint=(1, None), size_hint_y=None, height=25)

        for item in items:
            button = Button(text=item.capitalize())
            button.bind(on_press=self._get_items)
            item_button_bar.add_widget(button)

        return item_button_bar

@final
class ArmoryApp(App):
    """Main entry point into the Kivy main loop."""
    title = "Armory v0.1"

    def build(self):
        self.icon = "../assets/shield.ico"
        return Armory()

if __name__ == "__main__":
    ArmoryApp().run()
