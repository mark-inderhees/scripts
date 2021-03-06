'''View the workout for today'''

import pickle
import os
import sys
import re
import xml.etree.ElementTree
import matplotlib

from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QLabel,
    QCalendarWidget,
    QPushButton)
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class App(QWidget):
    '''Main class of the script'''

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
        self.ftp = None
        self.workout_name = None
        self.start_date = None
        self.days = None
        self.days_offset = 0
        self.week_day = None
        self.date = None
        self.steps = None
        self.duration = None
        self.calendar = QCalendarWidget()
        if 'ANDROID_ARGUMENT' in os.environ:
            # On Android, use a larger font size in the graph
            matplotlib.rcParams.update({'font.size': 35})
        self.figure = Figure()
        self.figure.set_facecolor('none')
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setStyleSheet('background-color:transparent;')
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.vbox)
        self.setFixedSize(480, 640)
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
        '''Run UI Code'''
        self.directory_name = self.config['directory_name']
        regex = re.match(
            '([0-9]+)(.*)',
            os.path.basename(self.directory_name))
        self.ftp = int(regex.groups()[0])
        self.workout_name = regex.groups()[1]
        self.start_date = self.config['start_date']
        time_diff = datetime.now().date() - self.start_date
        self.days = time_diff.days + 1
        self.calculate_week_day()
        self.update_ui()

    def update_ui(self):
        '''Refresh the UI'''
        self.hide()

        self.clear_layout(self.vbox)

        # Add date label
        label_date_diff = QLabel(
            '{} {} {} - {}'.format(
                self.week_day,
                self.workout_name.title(),
                self.ftp,
                self.date),
            self)

        # Add reset config button
        button_reset = QPushButton('Reset Configuration')
        button_reset.clicked.connect(self.reset_config)

        # Parse workout info and add to label
        label_duration = None
        label_steps = None
        x_data = []
        y_data = []
        step_start_time = 0
        if self.parse_file():
            label_duration = QLabel(
                '{} minutes, {} intervals'.format(
                    self.duration,
                    len(self.steps)),
                self)
            step_text = ''
            for step in self.steps:
                minutes = round(int(step[1]) / 60, 2)
                power = step[2]
                step_text += '{}: {}W for {} minutes\n'.format(
                    '{:02d}'.format(int(step[0])),
                    power,
                    '{:.2f}'.format(minutes))
                x_data.append(step_start_time)
                y_data.append(int(power))
                step_start_time += minutes
                x_data.append(step_start_time)
                y_data.append(int(power))
            label_steps = QLabel(step_text, self)
        else:
            label_duration = QLabel(
                'No workout file for this date',
                self)
            label_steps = QLabel('', self)

        # Build the chart
        self.axes.clear()
        self.axes.plot(
            [0, step_start_time],
            [self.ftp, self.ftp],
            color='grey',
            linestyle='dashed')
        self.axes.plot(x_data, y_data)
        self.canvas.draw()
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add back, today, and forward buttons
        hbox = QHBoxLayout()
        button_back = QPushButton('<--')
        button_back.clicked.connect(self.back_click)
        button_today = QPushButton('Today')
        button_today.clicked.connect(self.today_click)
        button_forward = QPushButton('-->')
        button_forward.clicked.connect(self.forward_click)
        hbox.addWidget(button_back)
        hbox.addWidget(button_today)
        hbox.addWidget(button_forward)

        self.vbox.addWidget(label_date_diff)
        self.vbox.addWidget(button_reset)
        self.vbox.addWidget(label_duration)
        self.vbox.addWidget(label_steps)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(hbox)
        self.show()

    def reset_config(self):
        '''Query the user for a new configuration'''
        self.build_config()

    def back_click(self):
        '''Go back one day'''
        if self.days + self.days_offset > 1:
            self.days_offset -= 1
        self.calculate_week_day()
        self.update_ui()

    def forward_click(self):
        '''Go forward one day'''
        if self.days + self.days_offset < 4 * 7:
            self.days_offset += 1
        self.calculate_week_day()
        self.update_ui()

    def today_click(self):
        '''Jump to today'''
        self.days_offset = 0
        self.calculate_week_day()
        self.update_ui()

    def clear_layout(self, layout):
        '''Remove all items from a layout, recursively removing layouts'''
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.widget() is not None:
                item.widget().setParent(None)
            elif item.layout() is not None:
                # This is a layout in a layout, recursively remove all widgets
                self.clear_layout(item)
                layout.removeItem(item)
            else:
                layout.removeItem(item)

    def calculate_week_day(self):
        '''Convert total days into week and day'''
        week = ((self.days + self.days_offset - 1) // 7) + 1
        day = ((self.days + self.days_offset - 1) % 7) + 1
        self.week_day = 'W{}D{}'.format(week, day)
        date = datetime.today() + timedelta(days=self.days_offset)
        self.date = date.strftime('%a, %b %d')
        if self.days_offset == 0:
            self.date += ' - Today'

    def parse_file(self):
        '''Read in workout file contents for current day'''
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
        '''Show open dialog'''
        options = QFileDialog.Options()
        directory_name = QFileDialog.getExistingDirectory(
            self,
            'Select Workout Directory',
            '', # Start directory, empty for current directory
            options)
        if directory_name:
            return directory_name
        return None

    def build_config(self):
        '''Prompt user for config settings and save to disk'''
        self.directory_name = self.open_directory_dialog()
        if self.directory_name is None:
            return False

        self.hide()
        self.clear_layout(self.vbox)

        # Show calendar date picker
        self.calendar.setGridVisible(True)
        button = QPushButton('Set Start Date')
        button.clicked.connect(self.set_date_click)
        self.vbox.addWidget(self.calendar)
        self.vbox.addWidget(button)
        self.show()

        return True

    def set_date_click(self):
        '''Calendar set date button click event handler'''
        start_date = self.calendar.selectedDate().toPyDate()
        self.config = {}
        self.config['start_date'] = start_date
        self.config['directory_name'] = self.directory_name
        pickle.dump(self.config, open(self.config_file, 'wb'))
        self.init_ui()

    def load_config(self):
        '''Read config file off disk or create a new one'''
        config_directory = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            '..',
            'etc'))
        if not os.path.exists(config_directory):
            os.mkdir(config_directory)
        self.config_file = os.path.join(
            config_directory,
            'view_todays_workout.b')

        if os.path.exists(self.config_file):
            self.config = pickle.load(open(self.config_file, 'rb'))
            return True
        return self.build_config()

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    ex = App()
    sys.exit(APP.exec_())
