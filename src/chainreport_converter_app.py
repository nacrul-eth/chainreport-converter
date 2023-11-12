"""Main GUI application to create chainreport files"""

import os
import sys

# kivy dependencies
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
# pylint: disable=no-name-in-module
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.resources import resource_add_path

# program dependencies
from chainreport_converter import ChainreportConverter

class LoadDialog(BoxLayout):
    """Load screen for the input file"""
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(BoxLayout):
    """Save screen for the chain.report file"""
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MainWindow(BoxLayout):
    """Main screen for the application"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = ""
        self.input_file = ""
        self.output_file = ""
        self.converter_object = ""
        self._popup = ""

    def set_parser(self, parserstring):
        """Set the parser for the conversion"""
        self.parser = parserstring
        self.log_action("You selected the parser: " + self.parser)

    def dismiss_popup(self):
        """Close popup"""
        self._popup.dismiss()

    def show_load(self):
        """Show the load file screen"""
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        """Show the save file screen"""
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        """Store the full input filename (including path) in local variable"""
        self.input_file = os.path.join(path, filename[0])
        self.log_action("You chose to open the following file: " + self.input_file)

        self.dismiss_popup()

    def save(self, path, filename):
        """Set the full output filname (including path) in local variable"""
        self.output_file = os.path.join(path, filename)
        self.log_action("You chose to write to the following file: " + self.output_file)

        self.dismiss_popup()

    def start_conversion(self):
        """Start the conversion process, if all parameters are set"""
        if self.parser and self.input_file and self.output_file:
            self.converter_object = ChainreportConverter(self.parser, self.input_file, self.output_file)
            self.log_action("Converting " + self.input_file + " to " +
                            self.output_file + " using the Parser for " +
                            self.parser)
            self.converter_object.convert(self.log_action)
            self.log_action("Conversion done!")
        else:
            self.log_action("Please select all input parameters first")

    def log_action(self, loggingtext):
        """Append text for logging on the GUI"""
        self.ids.logging.text += loggingtext + "\n"

class ChainreportConverterApp(App):
    """Main application"""

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        # pylint: disable=protected-access
        resource_add_path(os.path.join(sys._MEIPASS))
    ChainreportConverterApp().run()
