#!/usr/bin/python3

"""
D&D Jukebox

A little program for queuing up and playing audio files from your computer
using semantic labels (that the user assigns). Borrows some ideas from the
PyQT tutorials at http://zetcode.com/gui/pyqt5/.

Author: Andy Tracy <adtme11@gmail.com>
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, 
    QPushButton, QInputDialog, QFileDialog, QLabel, QGridLayout,
    QVBoxLayout, QHBoxLayout, QFrame, QMainWindow,
    QAction, qApp, QApplication)
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QPolygon
from PyQt5 import QtMultimedia, QtCore
from PyQt5.QtCore import QObject, Qt, pyqtSignal

from PyQt5.QtCore import QPoint, Qt, QTime, QTimer
from PyQt5.QtGui import QColor, QPainter, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget

class Playlist(object):

    def __init__(self, parent, url):
        self.now_playing = QLabel(parent)
        self.now_playing.setMaximumSize(150, 22)

        if url is not None:
            title = os.path.split(url)[-1]

            self.now_playing.setText(title)
            self.playlist = [(url, title)]

        else:
            self.playlist = []

    def clear(self):
        ''' Clear the playlist '''
        self.playlist = []
        self.now_playing.setText("")
    
    def add(self, url):
        ''' Add a song to the playlist '''
        pass

class Mood(QWidget):
    ''' A Mood object '''

    def __init__(self, label, url=None):
        ''' Input arguments:

            label: string, label for this mood
            url: url of the first audio file in the playlist
        '''
        super().__init__()

        self.label = label
        self.setMinimumSize(150, 50)
        
        self.playlist = Playlist(self, url)
        
        self.initUI()
        
    def initUI(self):

        self.top_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.play_button = QPushButton(self.label, self)
        self.play_button.clicked.connect(self.play)

        self.edit_button = QPushButton("🛠", self)
        self.edit_button.setMaximumSize(22, 22)
        self.edit_button.clicked.connect(self.edit)

        self.restart_button = QPushButton("↩", self)
        self.restart_button.setMaximumSize(22, 22)
        self.restart_button.clicked.connect(self.restart)

        self.button_layout.addWidget(self.play_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.restart_button)
        self.button_layout.addStretch(1)

        self.top_layout.addLayout(self.button_layout)
        self.top_layout.addWidget(self.playlist.now_playing)
        self.top_layout.addStretch(1)

        self.setLayout(self.top_layout)

    def play(self):
        pass

    def edit(self):
        self.playlist.clear()
        pass

    def restart(self):
        pass    

class Jukebox(QMainWindow):
    
    def __init__(self):
        super().__init__()

        # Get default location
        home = os.path.expanduser("~")

        # Set up audio player

        # Start with default mood
        self.moods = []
        self.moods.append(Mood("Adventure!", "Test"));
        
        self.initUI()
        
    def initUI(self):

        # Top level layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Menus
        load_act = QAction('Load', self)
        load_act.triggered.connect(self.load_settings)
        save_act = QAction('Save', self)
        save_act.triggered.connect(self.save_settings)
        exit_act = QAction('Quit', self)
        exit_act.triggered.connect(qApp.quit)

        pref_act = QAction('Settings', self)
        pref_act.triggered.connect(self.set_settings)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(load_act)
        fileMenu.addAction(save_act)
        fileMenu.addAction(exit_act)

        pref_menu = menubar.addMenu('Preferences')
        pref_menu.addAction(pref_act)

        # Button to add new moods
        self.add_btn = QPushButton('Add Mood', self)
        self.add_btn.clicked.connect(self.add_mood)

        self.add_box = QHBoxLayout()
        self.add_box.addWidget(self.add_btn)
        self.add_box.addStretch(1)

        # Horizontal Line
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setFrameShadow(QFrame.Sunken)

        # Grid for holding moods
        self.mood_box = QGridLayout()
        self.mood_box.addWidget(self.moods[0], 1, 1, 1, 1)

        # Combine layouts
        self.layout.addLayout(self.add_box)
        self.layout.addWidget(h_line)
        self.layout.addLayout(self.mood_box)
        self.layout.addStretch(1)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        
        # Set window properties
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('D&D Jukebox')

        self.show()

    def add_mood(self):
        # Get label
        new_label, ok = QInputDialog.getText(self, 'Mood Label', 'Enter the label for your new mood:')
        
        if ok:
            new_url = QFileDialog.getOpenFileName(self, 'Open file', '/home/Dropbox/Projects/Python/DNDMusic/')

            if new_url[0]:
                self.moods.append(Mood(new_label, new_url[0]))

                row = (len(self.moods) - 1) % 6 + 1
                col = (len(self.moods) - 1) // 6 + 1

                self.mood_box.addWidget(self.moods[-1], row, col, 1, 1)

    def save_settings(self):
        pass

    def load_settings(self):
        pass

    def set_settings(self):
        pass

    '''
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    '''

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    jb = Jukebox()
    sys.exit(app.exec_())
