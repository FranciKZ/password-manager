"""
    Created by: Kollin Francis
"""

import sqlite3
import secrets
import string
from sqlite3 import Error
from encryption import AESCipher

class SaveData:
    def insertNewService(self, key, db, userName, serviceName):
        # Generate New Password and Encrypt
        encryptedPass = AESCipher(key).encrypt(self.genPassword(SaveData))

        # Establish db connection
        # Insert Data
        # Try/catch is to ensure any faults are caught
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()

            c.execute('''INSERT INTO Services (serviceName) VALUES (?)''', (serviceName,))
            serviceID = c.lastrowid
            c.execute('''INSERT INTO Passwords (password, serviceID) VALUES(?, ?) ''', (encryptedPass, serviceID))
            c.execute('''INSERT INTO Usernames (userName, serviceID) VALUES(?, ?) ''', (userName, serviceID))
        except Error as e:
            print(e)
            return False
        finally:
            conn.commit()
            conn.close()
            return True

    def changePassword(self, key, db, serviceName):
        newPass = AESCipher(key).encrypt(self.genPassword())
        #serviceID = c.execute('''   SELECT serviceID 
        #                            FROM services 
        #                            WHERE ? = serviceName''', serviceName)
        try: 
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute('''   UPDATE Passwords (password) 
                            SET password = ?
                            WHERE Passwords.serviceID = (
                                                            SELECT serviceID
                                                            FROM Services
                                                            WHERE serviceName = ?
                                                        )''', (newPass, serviceName))
        except Error as e:
            print(e)
            return False
        finally:
            conn.commit()
            conn.close()
            return True
        
        
    def genPassword(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(20))

    # Used for intial DB creation and setup    
    def createDB(db):
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            create_services_table = '''CREATE TABLE Services (
                                        serviceID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        serviceName TEXT
                                    );'''
            create_user_table = '''CREATE TABLE Usernames (
                                    usernameID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    userName TEXT,
                                    serviceID INTEGER,
                                    FOREIGN KEY(serviceID) REFERENCES Services(serviceID)
                                );'''
            create_pass_table = '''CREATE TABLE Passwords (
                                    passID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    password TEXT
                                    serviceID INTEGER,
                                    FOREIGN KEY(serviceID) REFERENCES Services(serviceID)
                                );'''
            print('Creating Services Table')
            c.execute(create_services_table)
            print('Creating Username Table')
            c.execute(create_user_table)
            print('Creating Passwords Table')
            c.execute(create_pass_table)
        except Error as e:
            print(e)
            return False
        finally:
            conn.commit()
            conn.close()
            return True

class RetrieveData:
    def getPassword(self, key, db, serviceID):
        password = ''
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            password = c.execute('''SELECT password FROM Passwords WHERE Passwords.serviceID = ?''', (serviceID,))
        except Error as e:
            print(e)
            return False
        finally:
            conn.close()
    
        return AESCipher(key).decrypt(password)
    def getUserAndPass(self, key, db, serviceID):
        userName = ''
        password = ''

        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()

            c.execute(  '''   SELECT Usernames.userName, Passwords.password
                              FROM Usernames
                              INNER JOIN Usernames ON Usernames.ServiceID = Passwords.ServiceID
                              WHERE Usernames.ServiceID = ?
                        ''', (serviceID,))
            info = c.fetchone()
            userName = info[0]
            password = AESCipher(key).decrypt(info[1])
        except Error as e:
            print(e)
            return False
        finally:
            conn.close()

        return (userName, password)    

    def retrieveServices(self, db):
        listOfServices = ''
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute(''' SELECT serviceName FROM Services ''')
            listOfServices = list(c.fetchall())
            print(listOfServices)
        except Error as e:
            print(e)
        finally:
            conn.close()

        return listOfServices