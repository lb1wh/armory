"""
UI elements
"""

from typing import final

from kivy.uix.popup import Popup
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.graphics import Color, Rectangle


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
        self.text_size = (100, None) # TODO: Make this auto-scale
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
        popup = ui.TextInputPopup(self)
        popup.open()

    def update_changes(self, text):
        """Call when saving."""
        self.text = text
