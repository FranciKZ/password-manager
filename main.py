"""
    Created by: Kollin Francis

    Todo:
        Create Change Password Layout
        Create Generate Password Layout
        Implement Add Service Layout Functionality
            Get information from Text boxes
            Send information to database functions
        Implement Get Username and Password Layout Functionality
            Display username textually
            Have it copy password straight to clipboard
        Add master key lock before welcome screen
        Add combobox information in username and password layout
"""
from databaseFunction import SaveData, RetrieveData
from PyQt5.QtWidgets import (   QApplication, QWidget, QPushButton, QApplication,
                                QGridLayout, QStackedLayout, QMainWindow, QLineEdit, QLabel,
                                QComboBox)
from PyQt5.QtGui import QFont
import os
import sys
import os.path



def restOfCode(db):
    app = QApplication(sys.argv)
    ex = MainWindow(db)
    sys.exit(app.exec_())

class MainWindow(QMainWindow):

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle('Password Manager')
        self.setStyleSheet(open("styles.qss", "r").read())
        self.welcome()

        self.stacked_layout = QStackedLayout() # Holds various layouts
        self.create_add_service_layout()
        self.create_get_userpass_layout()
        self.create_change_pass_layout()
        self.create_gen_pass_layout()
        self.stacked_layout.addWidget(self.welcome_screen)
        self.stacked_layout.addWidget(self.add_service_widget)
        self.stacked_layout.addWidget(self.get_userpass_widget)
        self.stacked_layout.addWidget(self.change_pass_widget)
        self.stacked_layout.addWidget(self.gen_pass_widget)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)
        self.setGeometry(500, 500, 600, 300)
        self.show()

    def welcome(self):
        grid = QGridLayout()
        self.welcome_screen = QWidget()
        self.welcome_screen.setLayout(grid)
        addServiceBtn = QPushButton('Add Service', self)
        getUserAndPassBtn = QPushButton('Get Username and Password', self)
        changePassBtn = QPushButton('Change Password', self)
        genPassBtn = QPushButton('Generate Password', self)  

        grid.addWidget(addServiceBtn, 0, 0)
        grid.addWidget(getUserAndPassBtn, 0, 1)
        grid.addWidget(changePassBtn, 2, 0)
        grid.addWidget(genPassBtn, 2, 1)    

        addServiceBtn.clicked.connect(self.change_layout)
        getUserAndPassBtn.clicked.connect(self.change_layout)
        changePassBtn.clicked.connect(self.change_layout)
        genPassBtn.clicked.connect(self.change_layout)
        
    def change_layout(self):
        sender = self.sender()
        if(sender.text() == 'Return'):
            self.stacked_layout.setCurrentIndex(0)
        elif(sender.text() == 'Add Service'):
            self.stacked_layout.setCurrentIndex(1)
        elif(sender.text() == 'Get Username and Password'):
            self.stacked_layout.setCurrentIndex(2)
        elif(sender.text() == 'Change Password'):
            self.stacked_layout.setCurrentIndex(3)
        elif(sender.text() == 'Generate Password'):
            self.stacked_layout.setCurrentIndex(4)
        
    
    def create_add_service_layout(self):
        grid = QGridLayout()
        self.add_service_widget = QWidget()
        self.add_service_widget.setLayout(grid)
        serviceLbl = QLabel('Service Name: ')
        serviceName = QLineEdit()
        userLbl = QLabel('Username: ')
        userNameField = QLineEdit()
        addServiceBtn = QPushButton('Add Service') # ~~~~Todo Write Add Service Function
        returnBtn = QPushButton('Return')

        grid.addWidget(serviceLbl, 1, 0)
        grid.addWidget(serviceName, 1, 1)
        grid.addWidget(userLbl, 2, 0)
        grid.addWidget(userNameField, 2, 1)
        grid.addWidget(addServiceBtn, 3, 0)
        grid.addWidget(returnBtn, 3, 1)

        addServiceBtn.clicked.connect(self.addService)
        returnBtn.clicked.connect(self.change_layout)

    def create_get_userpass_layout(self):
        grid = QGridLayout()
        self.get_userpass_widget = QWidget()
        self.get_userpass_widget.setLayout(grid)

        combo = QComboBox()
        # ~~ Todo loop through results of services query and add it to combo box
        userLbl = QLabel('Username: ')
        passLbl = QLabel('Password has been copied to clipboard')
        getInfoBtn = QPushButton('Get Username and Password')
        returnBtn = QPushButton('Return')

        grid.addWidget(combo, 1, 0)
        grid.addWidget(getInfoBtn, 1, 1)
        grid.addWidget(returnBtn, 2, 1)
        # getInfoBtn.clicked.connect(self.getInfo)
        returnBtn.clicked.connect(self.change_layout)
    
    def create_change_pass_layout(self):
        grid = QGridLayout()
        self.change_pass_widget = QWidget()
        self.change_pass_widget.setLayout(grid)

        serviceLbl = QLabel('Service')
        serviceSelecter = QComboBox()
        oldLbl = QLabel('Old Password')
        oldField = QLineEdit()
        returnBtn = QPushButton('Return')
        changePassBtn = QPushButton('Confirm Change')

        grid.addWidget(serviceLbl,1, 0)
        grid.addWidget(serviceSelecter, 1, 1)
        grid.addWidget(oldLbl, 2, 0)
        grid.addWidget(oldField, 2, 1)
        grid.addWidget(changePassBtn, 3, 0)
        grid.addWidget(returnBtn, 3, 1)

        # changePassBtn.clicked.connect(self.changePass)
        returnBtn.clicked.connect(self.change_layout)

    def create_gen_pass_layout(self):
        grid = QGridLayout()
        self.gen_pass_widget = QWidget()
        self.gen_pass_widget.setLayout(grid)
   
        serviceLbl = QLabel('Service')
        serviceSelecter = QComboBox()
        returnBtn = QPushButton('Return')
        genPassBtn = QPushButton('Generate Password')

        grid.addWidget(serviceLbl, 1, 0)
        grid.addWidget(serviceSelecter, 1, 1)
        grid.addWidget(genPassBtn, 2, 0)
        grid.addWidget(returnBtn, 2, 1)

        # genPassBtn.clicked.connect(self.changePass
        returnBtn.clicked.connect(self.change_layout)

    def addService(self):
        SaveData.insertNewService(SaveData, 'Fran6819', self.db, 'francikz', 'Netflix')

def main():
    #how to use databaseFunction functions
    db = 'pass_manager_db.db'
    if not os.path.isfile(db):
        print('Not found')
        SaveData.createDB(db)
        restOfCode(db)
    else:
        # Just do the rest of the code
        restOfCode(db)
    return True  

if __name__ == '__main__':
    main()