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
    QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5 import QtMultimedia, QtCore

class Playlist(object):

    def __init__(self, parent, url, title):
        self.now_playing = QLabel(parent)
        self.now_playing.setMaximumSize(150, 22)
        self.now_playing.setText(title)
        self.playlist = [url]

    def clear(self):
        ''' Clear the playlist '''
        pass
    
    def add(self, url):
        ''' Add a song to the playlist '''
        pass

class Mood(object):
    ''' A Mood object

    I'd like to make this a QWidget, but I'm not sure how at
    this point
    '''

    def __init__(self, parent, label, url):
        ''' Input arguments:

            parent: parent QWidget object
            label: string, label for this mood
            url: url of the first audio file in the playlist
        '''

        # Parse out url
        title = os.path.split(url)[-1]

        self.top_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.playlist = Playlist(parent, url, title)

        self.play_button = QPushButton(label, parent)
        self.play_button.clicked.connect(self.play)

        self.edit_button = QPushButton("🛠", parent)
        self.edit_button.setMaximumSize(22, 22)
        self.edit_button.clicked.connect(self.edit)

        self.restart_button = QPushButton("↩", parent)
        self.restart_button.setMaximumSize(22, 22)
        self.restart_button.clicked.connect(self.restart)

        self.button_layout.addWidget(self.play_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.restart_button)
        self.button_layout.addStretch(1)

        self.top_layout.addLayout(self.button_layout)
        self.top_layout.addWidget(self.playlist.now_playing)

    def play(self):
        pass

    def edit(self):
        pass

    def restart(self):
        pass    

class Jukebox(QWidget):
    
    def __init__(self):
        super().__init__()

        # Set up audio player

        # Start with default mood
        self.moods = []
        self.moods.append(Mood(self, "Adventure!", "Takin' it easy.wav"));
        
        self.initUI()
        
    def initUI(self):

        # Top level layout
        self.layout = QVBoxLayout()

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
        self.mood_box.addLayout(self.moods[0].top_layout, 1, 1, 1, 1)

        # Combine layouts
        self.layout.addLayout(self.add_box)
        self.layout.addWidget(h_line)
        self.layout.addLayout(self.mood_box)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
        
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
                self.moods.append(Mood(self, new_label, new_url[0]))

                row = (len(self.moods) - 1) % 8 + 1
                col = (len(self.moods) - 1) // 8 + 1
                print(row, col)

                self.mood_box.addLayout(self.moods[-1].top_layout, row, col, 1, 1)
                

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
