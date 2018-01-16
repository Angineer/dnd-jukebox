#!/usr/bin/python3

"""
D&D Jukebox

A little program for queuing up and playing audio files from your computer
using semantic labels (that the user assigns). Borrows some ideas from the
PyQT tutorials at http://zetcode.com/gui/pyqt5/.

Author: Andy Tracy <adtme11@gmail.com>
"""

import sys
from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, 
    QPushButton, QLineEdit, QFileDialog)

class Playlist(object):

    def __init__(self, url):
        self.playlist = [url]

    def clear(self):
        ''' Clear the playlist '''
        pass
    
    def add(self, url):
        ''' Add a song to the playlist '''
        pass

class Mood(object):

    def __init__(self, parent, label, url):
        ''' Input arguments:

            parent: parent QWidget object
            label: string, label for this mood
            url: url of the first audio file in the playlist
        '''

        self.playlist = Playlist(url)
        self.play_button = QPushButton(label, parent)
        self.play_button.clicked.connect(self.edit)

    def edit(self):
        pass

    def position(self, x, y):
        self.play_button.move(x, y)

class Jukebox(QWidget):
    
    def __init__(self):
        super().__init__()

        # Start with default mood
        self.moods = []
        self.moods.append(Mood(self, "Adventure!", ""));
        
        self.initUI()
        
        
    def initUI(self):

        # Button to add new moods
        self.add_btn = QPushButton('Add Mood', self)
        self.add_btn.move(20, 10)
        self.add_btn.clicked.connect(self.addMood)

        # Default mood
        self.moods[0].position(20, 60)
        
        # Set window properties
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('D&D Jukebox')

        self.show()

    def addMood(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/Dropbox/Projects/Python/DNDMusic/')

        if fname[0]:
            print("Success")
        
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    jb = Jukebox()
    sys.exit(app.exec_())
