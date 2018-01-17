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
    QAction, qApp, QApplication, QCheckBox, QLineEdit)
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QPolygon, QIcon
from PyQt5 import QtMultimedia, QtCore
from PyQt5.QtCore import QObject, Qt, pyqtSignal

from PyQt5.QtCore import QPoint, Qt, QTime, QTimer
from PyQt5.QtGui import QColor, QPainter, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget

class Playlist(object):

    def __init__(self, parent, url):
        self.now_playing = QLabel(parent)
        self.now_playing.setMaximumSize(150, 22)

        self.now_index = -1
        self.playlist = []

        if url is not None:
            title = self.add(url)
            self.now_playing.setText(title)

            self.now_index = 0

    def clear(self):
        ''' Clear the playlist '''
        self.playlist = []
        self.now_playing.setText("")
        self.now_index = 0
    
    def add(self, url):
        ''' Add a song to the playlist '''
        title = ""
        if url is not None:
            title = os.path.split(url)[-1]
            self.playlist.append((url, title))

        return title

    def remove(self, idx):
        ''' Remove one track from the playlist '''
        pass

    def restart(self):
        if self.playlist:
            self.now_index = 0
            self.now_playing.setText(self.playlist[0][1])
        else:
            self.now_index = -1
            self.now_playing.setText("")

class EditDialog(QMainWindow):
    
    def __init__(self, mood, parent=None):
        super().__init__(parent)

        # Top level layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Tracks have a separate layout
        self.new_tracks = []
        self.track_layout = QVBoxLayout()

        for track in mood.playlist.playlist:
            url = track[0]
            title = track[1]

            self.add_track(url, title)

        # Add parameters
        self.update_box = QLineEdit(mood.label, self)
        self.layout.addWidget(self.update_box)

        #self.layout.addWidget(QLabel("Tracks:", self))

        self.layout.addLayout(self.track_layout)

        add_button = QPushButton("+", self)
        add_button.setMaximumSize(22, 22)
        add_button.clicked.connect(self.pick_track)
        self.layout.addWidget(add_button)

        self.layout.addStretch(1)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(lambda: self.save_settings(mood))
        self.layout.addWidget(save_button)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        
        # Set window properties
        self.setGeometry(400, 400, 320, 240)
        self.setWindowTitle('Settings')

        self.show()

    def pick_track(self):
        url = QFileDialog.getOpenFileName(self, 'Add Track')

        if url[0]:
            title = os.path.split(url[0])[-1]
            self.add_track(url[0], title)

    def add_track(self, url, title):
        idx = len(self.new_tracks)

        label = QLabel(title, self)
        label.setMinimumSize(100, 22)
        remove = QPushButton("-", self)
        remove.setMaximumSize(22, 22)
        mv_up = QPushButton("▲", self)
        mv_up.setMaximumSize(22, 22)
        mv_down = QPushButton("▼", self)
        mv_down.setMaximumSize(22, 22)

        single_track = QHBoxLayout()

        single_track.addWidget(label)
        single_track.addWidget(remove)
        single_track.addWidget(mv_up)
        single_track.addWidget(mv_down)
        single_track.setSpacing(5)

        list_item = (url, title, single_track)
        remove.clicked.connect(lambda: self.remove_track(list_item))
        mv_up.clicked.connect(lambda: self.up_track(list_item))
        mv_down.clicked.connect(lambda: self.down_track(list_item))

        self.new_tracks.append(list_item)
        self.track_layout.addLayout(single_track)

    def remove_track(self, list_item):
        url, title, single_track = list_item
        self.track_layout.removeItem(single_track)

        # Remove all the widgets
        for i in reversed(range(single_track.count())): 
            single_track.itemAt(i).widget().setParent(None)

        # Delete the single track layout
        single_track.deleteLater()
        
        # Remove from list
        try:
            self.new_tracks.remove(list_item)
        except ValueError:
            pass

    def up_track(self, list_item):
        old_idx = self.new_tracks.index(list_item)
        if old_idx > 0:
            new_idx = old_idx - 1
            self.new_tracks.remove(list_item)
            self.new_tracks.insert(new_idx, list_item)

            _, _, single_track = list_item
            self.track_layout.removeItem(single_track)
            self.track_layout.insertItem(new_idx, single_track)

    def down_track(self, list_item):
        old_idx = self.new_tracks.index(list_item)
        if old_idx < len(self.new_tracks) - 1:
            new_idx = old_idx + 1
            self.new_tracks.remove(list_item)
            self.new_tracks.insert(new_idx, list_item)

            _, _, single_track = list_item
            self.track_layout.removeItem(single_track)
            self.track_layout.insertItem(new_idx, single_track)

    def save_settings(self, mood):
        # Update label
        new_label = self.update_box.text()
        if new_label != mood.label:
            mood.label = new_label
            mood.play_button.setText(mood.label)

        # Update playlist with new tracks
        mood.playlist.clear()
        for track in self.new_tracks:
            mood.playlist.add(track[0])

        mood.playlist.restart()

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
        last_idx = self.playlist.now_index

        if last_idx >= 0:
            next_idx = last_idx + 1
            if next_idx == len(self.playlist.playlist):
                next_idx = 0

            self.playlist.now_index = next_idx
            self.playlist.now_playing.setText(self.playlist.playlist[next_idx][1])

    def edit(self):
        diag = EditDialog(self, self)

    def restart(self):
        self.playlist.restart()

class SettingsDialog(QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # Top level layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Add settings
        self.fade = QCheckBox("Fade between tracks", self)
        self.layout.addWidget(self.fade)
        self.layout.addStretch(1)

        self.save = QPushButton("Save", self)
        self.save.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        
        # Set window properties
        self.setGeometry(300, 300, 320, 240)
        self.setWindowTitle('Settings')

        self.show()

    def save_settings(self):
        print(self.fade.isChecked())

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
        self.setWindowIcon(QIcon('icon.png'))
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
        print("Save")

    def load_settings(self):
        print("Load")

    def set_settings(self):
        settings_window = SettingsDialog(self)

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
