"""View the workout for today"""

import pickle
import os
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QCalendarWidget,
    QPushButton)

class App(QWidget):
    """Main class of the script"""

    def __init__(self):
        super().__init__()
        self.config = None
        self.init_ui()

    def init_ui(self):
        """Run UI Code"""
        self.setWindowTitle("Today's Workout")
        self.setFixedSize(640, 480)
        self.load_config()
        self.show()

    def open_directory_dialog(self):
        """Show open dialog"""
        options = QFileDialog.Options()
        directory_name = QFileDialog.getExistingDirectory(
            self,
            "Workout Directory",
            "",
            options=options)
        if directory_name:
            return directory_name
        return None

    def build_config(self):
        """Prompt user for config settings and save to disk"""
        directory_name = self.open_directory_dialog()
        if directory_name is None:
            return

        vbox = QVBoxLayout()
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        button = QPushButton("Set Start Date")
        vbox.addWidget(calendar)
        vbox.addWidget(button)
        self.setLayout(vbox)
        date = calendar.selectedDate()
        print(date)

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
