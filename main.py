from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(kwargs)
        self.obj = obj
        self.obj_text = obj.text

        self.text_box = BoxLayout(orientation="vertical")
        self.text_input = TextInput(id="textinput", text=self.obj_text)
        self.save_button = Button(size_hint=(1, 0.2), text="Save changes",
                                  on_release=save_btn_release)
        self.cancel_button = Button(size_hint=(1, 0.2), text="Cancel changes", on_release=self.dismiss())

        self.text_box.add_widget(text_input)
        self.text_box.add_widget(save_button)
        self.add_widget(self.text_box)

    def save_btn_release(instance):
        self.obj.update_changes(self.text_input.text)
        self.dismiss()

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    """Add selection and focus behavior to the view"""

    def __init__(self, **kwargs):
        super(SelectableRecycleGridLayout, self).__init__(kwargs)
        self.cols = 2
        self.default_size = (None, dp(26))
        self.default_size_hint: (1, None)
        self.size_hint = None
        self.height = self.minimum_height
        self.orientation = "vertical"
        self.multiselect = True
        self.touch_multiselect = True

class SelectableButton(RecycleDataViewBehavior, Button):
    """Add selection support to the Button"""
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)

        with self.canvas.before:
            if self.selected:
                Color(.0, 0.9, .1, .3, mode="rgba")
            else:
                Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)

    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes"""
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """Add selection on touch down"""
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view"""
        self.selected = is_selected

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt

class Armory(BoxLayout):
    items = ListProperty([])

    def __init__(self, **kwargs):
        super(Armory, self).__init__(**kwargs)
        self.orientation = "vertical"

        # Item header bar
        item_header = GridLayout(size_hint=(1,None), size_hint_y=None, height=25, cols=2)
        item_name = Label(text="Name")
        item_notes = Label(text="Notes")
        item_header.add_widget(item_name)
        item_header.add_widget(item_notes)

        # Populate table
        self._get_items()

        # Item list
        item_list = BoxLayout()
        recycle_view = RecycleView(data=[{"text": str(x)} for x in self.items])
        #selectable_rgl = SelectableRecycleGridLayout()
        #recycle_view.add_widget(selectable_rgl)
        selectable_button = SelectableButton()
        recycle_view.orientation = "vertical"
        recycle_view.viewclass = selectable_button
        item_list.add_widget(recycle_view)

        self.add_widget(item_header)
        self.add_widget(item_list)

    def _get_items(self):
        # Temporary DB mock data
        rows = [["foo", "bar"], ["baz", "foo"], ["bar", "baz"]]

        for row in rows:
            for col in row:
                self.items.append(col)

class ArmoryApp(App):
    title = "Armory"

    def build(self):
        return Armory()

if __name__ == "__main__":
    ArmoryApp().run()