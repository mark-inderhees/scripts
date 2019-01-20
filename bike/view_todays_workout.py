"""View the workout for today"""

import pickle
import os
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog)

class App(QWidget):
    """Main class of the script"""

    def __init__(self):
        super().__init__()
        self.config = {}
        self.init_ui()

    def init_ui(self):
        """Run UI Code"""
        self.setWindowTitle("Today's Workout")
        self.setFixedSize(640, 480)
        self.open_file_name_dialog()
        self.show()

    def open_file_name_dialog(self):
        """Show open dialog"""
        options = QFileDialog.Options()
        file_name = QFileDialog.getExistingDirectory(
            self,
            "Workout Directory",
            "",
            options=options)
        if file_name:
            print(file_name)

    def build_config(self):
        """Prompt user for config settings and save to disk"""
        self.config = None

    def load_config(self):
        """Read config file off disk or create a new one"""
        config_file = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            '..',
            "etc",
            "viewTodaysWorkout.config"))

        if os.path.exists(config_file):
            self.config = pickle.load(open(config_file))
        else:
            self.build_config()

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    ex = App()
    sys.exit(APP.exec_())
