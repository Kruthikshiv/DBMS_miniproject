from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget
from HomeWindow import HomeScreen
import os


class LoginScreen(QWidget):
    # LoginScreen is a Child class of QWidget
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login")
        self.resize(350, 350)

        # Below code creates a vertical layout window and has been
        # assigned to layout variable
        layout = QVBoxLayout()

        # Now create labels and text fields for username and password
        # and store in label_username and input_username respectively
        label_username = QLabel('Username : ')
        input_username = QLineEdit()
        label_password = QLabel('Password : ')
        input_password = QLineEdit()

        # Below is login button created and stored under Button_login variable

        button_login = QPushButton('Login')

        # Now add all the labels and fields to vertical layout
        layout.addWidget(label_username)
        layout.addWidget(input_username)
        layout.addWidget(label_password)
        layout.addWidget(input_password)
        layout.addWidget(button_login)

        # when login button clicked
        button_login.clicked.connect(self.showHome)

        # Now linking layout as the called class layout
        self.setLayout(layout)

    def showloginscreen(self):
        self.show()

    def showHome(self):
        self.close()
        print('In showhome function')
        self.home_screen = HomeScreen()
        self.home_screen.show()
