"""Main GUI application to create chainreport files"""

import os

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.uix.screenmanager import ScreenManager, Screen

from chainreport_converter import ChainreportConverter
from widgets.dropdown_button import DropdownButton

class DropdownButton():
    pass

class MainScreen(Screen):
    """Main screen for the application"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = ""
        self.input_file = ""
        self.output_file = "Test.csv"

    def open(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            print(f.read())

    def selected(self, filename):
        self.input_file = filename[0]
        print("selected: %s" % filename[0])

    def set_parser(self, parserstring):
        self.parser = parserstring
        print(parserstring)

    def start_conversion(self):
        self.input_file = "/home/michael/Finance/Crypto/Hi-statement-2.csv"
        self.output_file = "Test.csv"
        self.converter = ChainreportConverter(self.parser, self.input_file, self.output_file)
        self.converter.convert()

class ChainreportConverterTool(ScreenManager):
    """Extensible screen manager implementation"""
    pass

class ChainreportConverterApp(App):
    """Main application"""
    def build(self):
        return ChainreportConverterTool()

if __name__ == '__main__':
    ChainreportConverterApp().run()
