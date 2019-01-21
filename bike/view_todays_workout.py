"""View the workout for today"""

import pickle
import os
import sys

from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QLabel,
    QCalendarWidget,
    QPushButton)

class App(QWidget):
    """Main class of the script"""

    def __init__(self):
        super().__init__()
        self.config = None
        self.config_file = None
        self.directory_name = None
        self.start_date = None
        self.week = None
        self.day = None
        self.calendar = QCalendarWidget()
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.setWindowTitle("Today's Workout")
        if self.load_config():
            if self.config is not None:
                self.init_ui()
        else:
            label_error = QLabel(
                'Failed to load configuration information',
                self)
            self.vbox.addWidget(label_error)
            self.show()

    def init_ui(self):
        """Run UI Code"""
        self.hide()
        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().setParent(None)
        self.directory_name = self.config['directory_name']
        self.start_date = self.config['start_date']
        time_diff = datetime.now().date() - self.start_date
        days = time_diff.days + 1
        self.week = days // 7
        self.day = days % 7
        label_directory = QLabel(
            'Directory {}'.format(self.directory_name),
            self)
        label_start_date = QLabel(
            'Start date {}'.format(self.start_date),
            self)
        label_date_diff = QLabel(
            'W{}D{}'.format(self.week, self.day),
            self)
        self.vbox.addWidget(label_directory)
        self.vbox.addWidget(label_start_date)
        self.vbox.addWidget(label_date_diff)
        self.show()

    def open_directory_dialog(self):
        """Show open dialog"""
        options = QFileDialog.Options()
        directory_name = QFileDialog.getExistingDirectory(
            self,
            "Select Workout Directory",
            "", # Start directory, empty for current directory
            options)
        if directory_name:
            return directory_name
        return None

    def build_config(self):
        """Prompt user for config settings and save to disk"""
        self.directory_name = self.open_directory_dialog()
        if self.directory_name is None:
            return False

        self.hide()
        self.calendar.setGridVisible(True)
        button = QPushButton("Set Start Date")
        button.clicked.connect(self.set_date_click)
        self.vbox.addWidget(self.calendar)
        self.vbox.addWidget(button)
        self.show()

        return True

    def set_date_click(self):
        """Calendar set date button click event handler"""
        start_date = self.calendar.selectedDate().toPyDate()
        self.config = {}
        self.config['start_date'] = start_date
        self.config['directory_name'] = self.directory_name
        pickle.dump(self.config, open(self.config_file, 'wb'))
        self.init_ui()

    def load_config(self):
        """Read config file off disk or create a new one"""
        config_directory = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            '..',
            "etc"))
        if not os.path.exists(config_directory):
            os.mkdir(config_directory)
        self.config_file = os.path.join(
            config_directory,
            "view_todays_workout.b")

        if os.path.exists(self.config_file):
            self.config = pickle.load(open(self.config_file, 'rb'))
            return True
        return self.build_config()

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    ex = App()
    sys.exit(APP.exec_())
