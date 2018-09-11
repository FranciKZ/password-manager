"""
    Created by: Kollin Francis

    Todo:
        Create Change Password Layout ~~~~ DONE
        Create Generate Password Layout ~~~~ DONE
        Implement Add Service Layout Functionality ~~~~ DONE
            Get information from Text boxes ~~~~ DONE
            Send information to database functions ~~~~ DONE
        Implement Get Username and Password Layout Functionality ~~~~ DONE
            Display username textually ~~~~ DONE
            Have it copy password straight to clipboard ~~~~ DONE
        Add combobox information in username and password layout ~~~~ DONE
        Add master key lock before welcome screen
        Redesign GUI to be way nicer
        Look over code to see opportunities to improve efficiency and clean up code
        Store passwords in database more securely by using a randomly generated salt and then hashing it
"""
from databaseFunction import SaveData, RetrieveData
from PyQt5.QtWidgets import (   QApplication, QWidget, QPushButton, QApplication,
                                QGridLayout, QStackedLayout, QMainWindow, QLineEdit, QLabel,
                                QComboBox, QMessageBox)
import os
import sys
import os.path
from encryption import AESCipher

def restOfCode(db, dbFound):
    app = QApplication(sys.argv)
    ex = MainWindow(db, dbFound)
    sys.exit(app.exec_())

class MainWindow(QMainWindow):

    def __init__(self, db, dbFound):
        super().__init__()
        self.db = db
        self.setWindowTitle('Password Manager')
        self.setStyleSheet(open("styles.qss", "r").read())
        self.stacked_layout = QStackedLayout() # Holds various layouts
        self.create_login_layout(db, dbFound)
        self.stacked_layout.addWidget(self.login_screen)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)
        self.setGeometry(500, 500, 600, 300)
        self.show()
            
    def change_layout(self, page):
        if(page == 0):
            self.welcome()
            self.stacked_layout.addWidget(self.welcome_screen)
            self.stacked_layout.setCurrentWidget(self.welcome_screen)
        if(page == 1):
            self.stacked_layout.setCurrentWidget(self.welcome_screen)
        elif(page == 2):
            self.create_add_service_layout()
            self.stacked_layout.addWidget(self.add_service_widget)
            self.stacked_layout.setCurrentWidget(self.add_service_widget)
        elif(page == 3):
            self.create_get_userpass_layout()
            self.stacked_layout.addWidget(self.get_userpass_widget)
            self.stacked_layout.setCurrentWidget(self.get_userpass_widget)
        elif(page == 4):
            self.create_change_pass_layout()
            self.stacked_layout.addWidget(self.change_pass_widget)
            self.stacked_layout.setCurrentWidget(self.change_pass_widget)
        # elif(sender.text() == 'Generate Password'):
        #     self.create_gen_pass_layout()
        #     self.stacked_layout.addWidget(self.gen_pass_widget)
        #     self.stacked_layout.setCurrentWidget(self.gen_pass_widget)

    def create_login_layout(self, db, dbFound):
        grid = QGridLayout()
        self.login_screen = QWidget()
        self.login_screen.setLayout(grid)
        loginLbl = QLabel('Login')
        loginForm = QLineEdit()
        loginForm.setPlaceholderText('Password')
        loginBtn = QPushButton('Login')
        grid.addWidget(loginLbl, 0, 0)
        grid.addWidget(loginForm, 0, 1)
        grid.addWidget(loginBtn, 1, 1)
        loginBtn.clicked.connect(lambda: login(self, db, dbFound, loginForm.text()))

    def welcome(self):
        grid = QGridLayout()
        self.welcome_screen = QWidget()
        self.welcome_screen.setLayout(grid)
        addServiceBtn = QPushButton('Add Service', self)
        getUserAndPassBtn = QPushButton('Get Username and Password', self)
        changePassBtn = QPushButton('Change Password', self)
        # genPassBtn = QPushButton('Generate Password', self)  
        grid.addWidget(addServiceBtn, 0, 0)
        grid.addWidget(getUserAndPassBtn, 0, 1)
        grid.addWidget(changePassBtn, 0, 2)
        # grid.addWidget(genPassBtn, 2, 1)    

        addServiceBtn.clicked.connect(self.change_layout(2))
        getUserAndPassBtn.clicked.connect(self.change_layout(3))
        changePassBtn.clicked.connect(self.change_layout(4))
        # genPassBtn.clicked.connect(self.change_layout)
    
    def create_add_service_layout(self):
        grid = QGridLayout()
        self.add_service_widget = QWidget()
        self.add_service_widget.setLayout(grid)
        serviceLbl = QLabel('Service Name: ')
        serviceName = QLineEdit()
        serviceName.setPlaceholderText('Service')
        userLbl = QLabel('Username: ')
        userNameField = QLineEdit()
        userNameField.setPlaceholderText('User name')
        addServiceBtn = QPushButton('Add Service') # ~~~~Todo Write Add Service Function~~~~~ DONE
        returnBtn = QPushButton('Return')

        grid.addWidget(serviceLbl, 1, 0)
        grid.addWidget(serviceName, 1, 1)
        grid.addWidget(userLbl, 2, 0)
        grid.addWidget(userNameField, 2, 1)
        grid.addWidget(addServiceBtn, 3, 0)
        grid.addWidget(returnBtn, 3, 1)

        addServiceBtn.clicked.connect(lambda: addService(self.db, userNameField.text(), serviceName.text()))
        returnBtn.clicked.connect(self.change_layout(1))

    def create_get_userpass_layout(self):
        grid = QGridLayout()
        self.get_userpass_widget = QWidget()
        self.get_userpass_widget.setLayout(grid)
        serviceSelecter = QComboBox()
        for i in RetrieveData.retrieveServices(self.db):
            serviceSelecter.addItem(i[0])
        userLbl = QLabel('Username: ')
        passLbl = QLabel('Password has been copied to clipboard')
        getInfoBtn = QPushButton('Get Username and Password')
        returnBtn = QPushButton('Return')

        grid.addWidget(serviceSelecter, 1, 0)
        grid.addWidget(getInfoBtn, 1, 1)
        grid.addWidget(returnBtn, 2, 1)
        getInfoBtn.clicked.connect(lambda: getUserPassInfo(self.db, serviceSelecter.currentText()))
        returnBtn.clicked.connect(self.change_layout(1))
    
    def create_change_pass_layout(self):
        grid = QGridLayout()
        self.change_pass_widget = QWidget()
        self.change_pass_widget.setLayout(grid)

        serviceLbl = QLabel('Service')
        serviceSelecter = QComboBox()
        for i in RetrieveData.retrieveServices(self.db):
            serviceSelecter.addItem(i[0])
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

        changePassBtn.clicked.connect(lambda: changePass(self.db, serviceSelecter.currentText(), oldField.text()))
        returnBtn.clicked.connect(self.change_layout(1))

    # def create_gen_pass_layout(self):
    #     grid = QGridLayout()
    #     self.gen_pass_widget = QWidget()
    #     self.gen_pass_widget.setLayout(grid)
   
    #     serviceLbl = QLabel('Service')
    #     serviceSelecter = QComboBox()
    #     for i in RetrieveData.retrieveServices(self.db):
    #         serviceSelecter.addItem(i[0])
    #     returnBtn = QPushButton('Return')
    #     genPassBtn = QPushButton('Generate Password')

    #     grid.addWidget(serviceLbl, 1, 0)
    #     grid.addWidget(serviceSelecter, 1, 1)
    #     grid.addWidget(genPassBtn, 2, 0)
    #     grid.addWidget(returnBtn, 2, 1)

    #     genPassBtn.clicked.connect(lambda: genPassword())
    #     returnBtn.clicked.connect(self.change_layout)

def addService(db, userName, serviceName):
    listOfServices = RetrieveData.retrieveServices(db)
    if userName == '' or serviceName == '':
        showDialog('You must enter information for the service and username')
    elif (serviceName,) in listOfServices:
        showDialog('Service already in system')
    else:
        SaveData.insertNewService('testkey', db, userName, serviceName)
        copyToClip(getPassword(db, serviceName))
        showDialog('Successfully Added. \nPassword For Service Has Been Copied to Your Clipboard')

def showDialog(message):
    msg = QMessageBox()
    msg.setText(message)
    msg.exec()

def getUserPassInfo(db, serviceName):
    userPass = RetrieveData.getUserAndPass('testkey', db, serviceName)
    copyToClip(userPass[1])
    showDialog('Username: %s \nPassword has been copied to clipboard' % userPass[0])
    
def getPassword(db, serviceName):
    password = RetrieveData.getPassword('testkey', db, serviceName)
    return password

def changePass(db, serviceName, oldPassword):
    if oldPassword.strip() == RetrieveData.getPassword('testkey', db, serviceName):
        SaveData.changePassword('', db, serviceName)
        showDialog('Password Change Successful')

def copyToClip(txt):
    command = 'echo ' + txt.strip() + '| pbcopy'
    os.system(command)

def login(self, db, dbFound, password): # ~~~~~ TO DO
    if dbFound:
        # check if entered password matches password in databse because if the database
        # exists then that means the program has been run before and there should be a master
        # password in the database already
        if(RetrieveData.checkMasterPass(db, password)):
            self.change_layout(0)
    else:
        # Ask the user to enter a master password because it needs to be saved in the database
        SaveData.setMaster(db, password)
        self.change_layout(0)
        return None

def main():
    #how to use databaseFunction functions
    db = 'pass_manager_db.db'
    #if not os.path.isfile(db):
    #    print('Not found')
    #    SaveData.createDB(db)
    #    restOfCode(db, False)
    #else:
        # Just do the rest of the code
    #    restOfCode(db, True)
    password = 'Fran6819KO50IP1e'
    generated = 'tHrPSvvVIHTRBNc8'
    toDecrypt = "dc94RN/GLfJcVCD6e5+FvGyFitfR+MvLh1Fj3T/mwkyM4YeUeBA6NNroDiVHNKn0"
    print(password)
    unencrypted = AESCipher(password).decrypt(toDecrypt)
    print(unencrypted)

if __name__ == '__main__':
    main()