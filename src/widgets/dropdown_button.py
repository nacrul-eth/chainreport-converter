"""Customizable Dropdown Button"""

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

# pylint: disable=no-name-in-module
from kivy.properties import StringProperty

class DropdownButton(Button):
    """Dropdown Button to select an element of a list (currently hardcoded)"""

    selected_parser =  StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()

        parsers = ['Hi', 'Plutus', 'Coinbase Pro']

        for parser in parsers:
            btn = Button(text=parser, size_hint_y=None, height=50)
            # pylint: disable=E1101
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))

            self.drop_list.add_widget(btn)

        # pylint: disable=E1101
        self.bind(on_release=self.drop_list.open)

        self.drop_list.bind(on_select=lambda instance, parserstring: setattr(self, 'text', parserstring))
        self.drop_list.bind(on_select=self.change_parser)

    def change_parser(self, instance, parserstring):
        """Change the parser proporty and the corresponding button text"""
        del instance
        # Change string property for external notification
        # pylint: disable=E1101
        self.selected_parser = parserstring
