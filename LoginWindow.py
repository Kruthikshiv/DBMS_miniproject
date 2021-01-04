from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget
from HomeWindow import HomeScreen
import sys
from DataBaseOperation import DBOperation


class LoginScreen(QWidget):
    # LoginScreen is a Child class of QWidget
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login")
        self.resize(350, 100)

        # Below code creates a vertical layout window and has been
        # assigned to layout variable
        layout = QVBoxLayout()

        # Now create labels and text fields for username and password
        # and store in label_username and input_username respectively
        # We can use stylesheet(CSS) for setting bg,font,font size etc.
        label_username = QLabel('Username : ')
        label_username.setStyleSheet("color:#000;padding:8px 0px;font-size:18px")
        self.input_username = QLineEdit()
        self.input_username.setStyleSheet("padding:5px;font-size:18px")

        label_password = QLabel('Password : ')
        label_password.setStyleSheet("color:#000;padding:8px 0px;font-size:18px")
        self.input_password = QLineEdit()
        self.input_password.setStyleSheet("padding:5px;font-size:18px")
        self.error_msg = QLabel()
        self.error_msg.setStyleSheet("color:red")

        # Below is login button created and stored under Button_login variable

        button_login = QPushButton('Login')
        button_login.setStyleSheet("background:#B5651D;color:#fff;padding:8px 0px;font-size:20px;font-weight:bold")

        # Now add all the labels and fields to vertical layout
        layout.addWidget(label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(button_login)
        layout.addWidget(self.error_msg)
        layout.addStretch()


        # when login button clicked
        button_login.clicked.connect(self.showHome)

        # Now linking layout as the called class layout
        self.setLayout(layout)

    def showloginscreen(self):
        self.show()

    def showHome(self):
        if self.input_username == '':
            self.error_msg.setText('Enter valid username')
            return

        if self.input_password == '':
            self.error_msg.setText("Enter valid password")
            return
        dboperation = DBOperation()
        result = dboperation.doAdminLogin(self.input_username.text(),self.input_password.text())
        if result:
            self.error_msg.setText("Login successful")
            self.close()
            self.home_screen = HomeScreen()
            self.home_screen.show()
        else:
            self.error_msg.setText('Login unsuccessful')

