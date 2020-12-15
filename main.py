# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import os
from Install_Window import InstallWindow
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from LoginWindow import LoginScreen

class MainScreen():
    def showsplashscreen(self):
        self.pix = QPixmap('parking.png')
        self.splaash = QSplashScreen(self.pix,Qt.WindowStaysOnTopHint)
        self.splaash.show()

def showsetupwindow():
    mainscreen.splaash.close()
    installwindow.show()

def showloginwindow():
    mainscreen.splaash.close()
    login.showloginscreen()

app = QApplication(sys.argv)
login = LoginScreen()
mainscreen = MainScreen()
mainscreen.showsplashscreen()
installwindow = InstallWindow()


if os.path.exists("./config.json"):
    QTimer.singleShot(3000,showloginwindow)
else:
    QTimer.singleShot(3000,showsetupwindow)


sys.exit(app.exec())
