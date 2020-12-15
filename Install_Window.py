from PyQt5.QtWidgets import QWidget,QPushButton,QVBoxLayout,QLabel,QLineEdit
from LoginWindow import LoginScreen
import json
from DataBaseOperation import DBOperation

class InstallWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Install Vehiccle Paking Management System")
        self.resize(700,200)

        layout=QVBoxLayout()

        label_db_name = QLabel('Database Name :')
        label_db_username = QLabel('Database Username :')
        label_db_password = QLabel('Database password :')
        label_admin_username = QLabel('Admin Username :')
        label_admin_password = QLabel('Admin Password :')
        label_no_of_two_seater = QLabel('Number of two seaters :')
        label_no_of_four_seater = QLabel('Number of four seaters :')

        # Below code is used to create text fields for all entries in install window
        # We use self for all of this to convert from local to global object
        self.input_db_name = QLineEdit()
        self.input_db_username = QLineEdit()
        self.input_db_password = QLineEdit()
        self.input_admin_username = QLineEdit()
        self.input_admin_password = QLineEdit()
        self.input_no_of_two_wheelers = QLineEdit()
        self.input_no_of_four_wheelers = QLineEdit()

        # A button is created of name button_save with text in it has Save Configuration
        button_save = QPushButton('Save Configuration')

        # This label is red to indicate error in filling details
        self.error_label = QLabel()
        self.error_label.setStyleSheet("solor:red")

        layout.addWidget(label_db_name)
        layout.addWidget(self.input_db_name)
        layout.addWidget(label_db_username)
        layout.addWidget(self.input_db_username)
        layout.addWidget(label_db_password)
        layout.addWidget(self.input_db_password)
        layout.addWidget(label_admin_username)
        layout.addWidget(self.input_admin_username)
        layout.addWidget(label_admin_password)
        layout.addWidget(self.input_admin_password)
        layout.addWidget(label_no_of_two_seater)
        layout.addWidget(self.input_no_of_two_wheelers)
        layout.addWidget(label_no_of_four_seater)
        layout.addWidget(self.input_no_of_four_wheelers)
        layout.addWidget(button_save)
        layout.addWidget(self.error_label)

        button_save.clicked.connect(self.showStepInfo)

        self.setLayout(layout)

    def showStepInfo(self):
        # Creating a dict and storing config into it
        # and then writing it into json file
        if self.input_db_name.text() == "":
            self.error_label.setText("Please Enter valid DB name")
            # We use return so that if right input is not typed then
            # further execution of program will not take palce
            return

        if self.input_db_username.text() == "":
            self.error_label.setText("Please Enter valid DB username")
            return

        if self.input_db_password.text() == "":
            self.error_label.setText("Please Enter valid DB Password")
            return

        if self.input_admin_username_name.text() == "":
            self.error_label.setText("Please Enter valid Admin Username")
            return

        if self.input_admin_password_name.text() == "":
            self.error_label.setText("Please Enter valid Admin password")
            return

        if self.input_no_of_two_wheelers.text() == "":
            self.error_label.setText("Please Enter valid number of two wheeler spaces")
            return

        if self.input_admin_password_name.text() == "":
            self.error_label.setText("Please Enter valid number of four wheeler spaces")
            return

        file = open('./config.json','w')
        data = {"username":self.input_db_username.text(),
                "database":self.input_db_name.text(),
                "password":self.input_db_password.text()}
        # json.dumps is used to convert dict to json file type format
        file.write(json.dumps(data))
        file.close()
        # Creating DBOperation instance and calling all functions in correct order
        # for specified execution flow
        dboperation = DBOperation()
        dboperation.createTables()
        dboperation.InsertAdmin(self.input_admin_username.text(),self.input_admin_password.text())
        dboperation.InsertOneTimeData(self.input_no_of_two_wheelers.text(),self.input_no_of_four_wheelers.text())

        self.close()
        self.login = LoginScreen()
        self.login.showloginscreen()
        print('Save')

