"""View the workout for today"""

import pickle
import os
import sys
import xml.etree.ElementTree

from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QLabel,
    QCalendarWidget,
    QPushButton)
from PyQt5 import QtCore

class App(QWidget):
    """Main class of the script"""

    def __init__(self):
        super().__init__()
        xml.etree.ElementTree.register_namespace(
            '',
            'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
        self.nsworkout = 'http://www.garmin.com/xmlschemas/WorkoutExtension/v1'
        xml.etree.ElementTree.register_namespace(
            'nsworkout',
            self.nsworkout)
        xml.etree.ElementTree.register_namespace(
            'xsi',
            'http://www.w3.org/2001/XMLSchema-instance')
        self.config = None
        self.config_file = None
        self.directory_name = None
        self.start_date = None
        self.days = None
        self.week_day = None
        self.steps = None
        self.duration = None
        self.calendar = QCalendarWidget()
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
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
        self.days = time_diff.days + 1
        self.calculate_week_day()
        label_date_diff = QLabel(self.week_day, self)
        if not self.parse_file():
            label_error = QLabel(
                'Failed to parse workout file',
                self)
            self.vbox.addWidget(label_error)
            self.show()
            return
        label_duration = QLabel(
            '{} minutes'.format(self.duration),
            self)
        step_text = ''
        for step in self.steps:
            step_text += '{}: {}W for {} minutes\n'.format(
                step[0], step[2], str(int(step[1]) / 60))
        label_steps = QLabel(step_text, self)
        self.vbox.addWidget(label_date_diff)
        self.vbox.addWidget(label_duration)
        self.vbox.addWidget(label_steps)
        self.show()

    def calculate_week_day(self):
        """Convert total days into week and day"""
        week = ((self.days - 1) // 7) + 1
        day = ((self.days - 1) % 7) + 1
        self.week_day = 'W{}D{}'.format(week, day)

    def parse_file(self):
        """Read in workout file contents for current day"""
        workout_file = None
        for directory_file in os.listdir(self.directory_name):
            if self.week_day in directory_file:
                workout_file = directory_file
                break
        if workout_file is None:
            return False

        workout_file_path = os.path.join(self.directory_name, workout_file)
        tree = xml.etree.ElementTree.parse(workout_file_path)
        root = tree.getroot()
        self.steps = []
        for step in root.iter('{{{}}}Step'.format(self.nsworkout)):
            interval_id = None
            seconds = None
            power = None
            for step_id in step.iter('{{{}}}StepId'.format(self.nsworkout)):
                interval_id = step_id.text
            for duration_seconds in step.iter(
                    '{{{}}}Seconds'.format(self.nsworkout)):
                seconds = duration_seconds.text
            for high_power in step.iter('{{{}}}High'.format(self.nsworkout)):
                for value in high_power:
                    power = value.text
            self.steps.append((interval_id, seconds, power))
        self.duration = str(sum([int(data[1]) for data in self.steps]) // 60)
        return True

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
