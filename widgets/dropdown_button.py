"""Customizable Dropdown Button"""

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

class DropdownButton(Button):
    """Dropdown Button to select an element of a list (currently hardcoded)"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()

        parsers = ['Hi', 'Plutus']

        for parser in parsers:
            btn = Button(text=parser, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))

            self.drop_list.add_widget(btn)

        self.bind(on_release=self.drop_list.open)
        self.drop_list.bind(on_select=lambda instance, x: setattr(self, 'text', x))
