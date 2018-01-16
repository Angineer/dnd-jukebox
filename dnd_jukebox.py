#!/usr/bin/python3

"""
D&D Jukebox

A little program for queuing up and playing audio files from your computer
using semantic labels (that the user assigns). Borrows some ideas from the
PyQT tutorials at http://zetcode.com/gui/pyqt5/.

Author: Andy Tracy <adtme11@gmail.com>
"""

import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication

class Jukebox(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        self.setGeometry(300, 300, 640, 480)        
        self.setWindowTitle('D&D Jukebox')    
        self.show()
        
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    jb = Jukebox()
    sys.exit(app.exec_())
