"""Main GUI application to create chainreport files"""

import os

# kivy dependencies
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# program dependencies
from chainreport_converter import ChainreportConverter

class MainScreen(Screen):
    """Main screen for the application"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = ""
        self.input_file = ""
        self.local_file_path = ""
        self.output_file = ""
        self.converter = ""

    def open(self, path, filename):
        """Store the full filename (including path) in local variable"""
        if filename:
            self.input_file = filename[0]
            self.local_file_path = path

    def selected(self, filename):
        """Store the selected filename """
        self.input_file = filename[0]
        self.log_action("You selected the input file " + self.input_file)

    def set_parser(self, parserstring):
        """Set the parser for the conversion"""
        self.parser = parserstring
        self.log_action("You selected the parser: " + self.parser)

    def set_outputfile(self, full_filename_path):
        """Set the output file"""
        self.output_file = full_filename_path
        self.log_action("You chose to write to the following file: " + self.output_file)

    def start_conversion(self):
        """Start the conversion process, if all parameters are set"""
        if self.parser and self.input_file and self.output_file:
            self.converter = ChainreportConverter(self.parser, self.input_file, self.output_file)
            self.log_action("Converting " + os.path.join(self.local_file_path, self.input_file) + " to " +
                            os.path.join(self.local_file_path, self.output_file) + " using the Parser for " +
                            self.parser)
            self.converter.convert()
            self.log_action("Conversion done!")
        else:
            self.log_action("Please select all input parameters first")

    def log_action(self, loggingtext):
        """Append text for logging on the GUI"""
        self.ids.logging.text += loggingtext + "\n"

class ChainreportConverterTool(ScreenManager):
    """Extensible screen manager implementation"""

class ChainreportConverterApp(App):
    """Main application"""
    def build(self):
        return ChainreportConverterTool()

if __name__ == '__main__':
    ChainreportConverterApp().run()
