"""
    Created by: Kollin Francis
"""

import sqlite3
import secrets
import string
from sqlite3 import Error
from encryption import AESCipher

class SaveData:
    def insertNewService(key, db, userName, serviceName):
        # Generate New Password and Encrypt
        newPass = SaveData.genPassword()
        salt = SaveData.genSalt()
        newPass += salt
        encryptedPass = AESCipher(key).encrypt(newPass)

        # Establish db connection
        # Insert Data
        # Try/catch is to ensure any faults are caught
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()

            c.execute('''INSERT INTO Services (serviceName) VALUES (?) ''', (serviceName,))
            serviceID = c.lastrowid
            c.execute('''INSERT INTO Passwords (password, serviceID) VALUES(?, ?) ''', (encryptedPass, serviceID))
            c.execute('''INSERT INTO Usernames (userName, serviceID, salt) VALUES(?, ?, ?) ''', (userName, serviceID, salt))
        except Error as e:
            print(e)
            return False
        finally:
            conn.commit()
            conn.close()
            return True

    #~~~~TODO
    def setMaster(db, password):
        salt = SaveData.genSalt()
        password += salt
        toEncrypt = SaveData.genPassword()
        print('setMaster pass + salt = ', password)
        encryptedPass = AESCipher(password).encrypt(toEncrypt)
        print('To Encrypt = ', toEncrypt)
        print('Encrypted pass = ', encryptedPass)

        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute(''' INSERT INTO Services (serviceName) VALUES(?) ''', ('Master',))
            serviceId = c.lastrowid
            c.execute(''' INSERT INTO Passwords(password, serviceID) VALUES (?, ?) ''', (encryptedPass, serviceId))
            c.execute(''' INSERT INTO Usernames(userName, serviceID, salt) VALUES(?, ?, ?) ''', ('Master', serviceId, salt))
        except Error as e:
            return False
        finally:
            conn.commit()
            conn.close()

    def changePassword(key, db, serviceName):
        newPass = SaveData.genPassword()
        salt = SaveData.genSalt()
        newPass += salt
        encryptedPass = AESCipher(key).encrypt(newPass)
        
        #serviceID = c.execute('''   SELECT serviceID 
        #                            FROM services 
        #                            WHERE ? = serviceName''', serviceName)
        try: 
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute('''   UPDATE Passwords
                            SET password = ?
                            WHERE Passwords.serviceID = (
                                                            SELECT serviceID
                                                            FROM Services
                                                            WHERE serviceName = ?
                                                        )''', (encryptedPass, serviceName))
            c.execute(  ''' UPDATE Usernames 
                            SET salt = ?
                            WHERE Usernames.serviceID = (
                                                            SELECT serviceID
                                                            FROM Services
                                                            WHERE serviceName = ?
                            )
                        ''', (salt, serviceName))
        except Error as e:
            print(e)
            return False
        finally:
            conn.commit()
            conn.close()
            return True       
        
    def genPassword():
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(16))

    def genSalt():
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(8))

    # Used for intial DB creation and setup    
    def createDB(db):
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            create_services_table = '''CREATE TABLE Services (
                                        serviceID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        serviceName TEXT,
                                        UNIQUE (serviceName)
                                    );'''
            create_user_table = '''CREATE TABLE Usernames (
                                    usernameID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    userName TEXT,
                                    serviceID INTEGER,
                                    salt TEST,
                                    FOREIGN KEY(serviceID) REFERENCES Services(serviceID)
                                );'''
            create_pass_table = '''CREATE TABLE Passwords (
                                    passID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    password TEXT,
                                    serviceID INTEGER,
                                    FOREIGN KEY(serviceID) REFERENCES Services(serviceID)
                                );'''
            c.execute(create_services_table)
            c.execute(create_user_table)
            c.execute(create_pass_table)
        except Error as e:
            print(e)
            return False
        finally:
            conn.commit()
            conn.close()

class RetrieveData:
    # This is used to check the login password provided
    # if it matched what is decrypted then the user should be allowed 
    # to access the program
    def checkMasterPass(db, password):
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute(''' SELECT salt FROM Usernames WHERE serviceID = 0 ''')
            salt = c.fetchone()[0]
            password += salt
            c.execute(''' SELECT password FROM Passwords where serviceID = 0 ''')
            masterpass = c.fetchone()[0]

            decryptedPass = AESCipher(password).decrypt(masterpass)

            if(decryptedPass == password):
                return True
            else:
                return False
        except Error as e:
            print(e)
            return False
        finally: 
            conn.close()

    def getPassword(key, db, serviceName):
        password = ''
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute(  ''' SELECT password 
                            FROM Passwords 
                            WHERE Passwords.serviceID = (
                                SELECT serviceID
                                FROM Services
                                WHERE serviceName = ?
                        )''', (serviceName,))
            
            password = c.fetchone()[0]
        except Error as e:
            print(e)
            return False
        finally:
            conn.close()
    
        return AESCipher(key).decrypt(password)

    def getUserAndPass(key, db, serviceName):
        userName = ''
        password = ''

        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute(  '''   SELECT Usernames.userName, Passwords.password
                              FROM Usernames
                              JOIN Passwords ON Usernames.serviceID = Passwords.serviceID
                              WHERE Usernames.serviceID = (
                                  SELECT serviceID
                                  FROM Services
                                  WHERE serviceName = ?
                              )
                        ''', (serviceName,))
            info = c.fetchall()
            userName = info[0][0]
            password = AESCipher(key).decrypt(info[0][1])
        except Error as e:
            print(e)
            return False
        finally:
            conn.close()

        return (userName, password)    

    def retrieveServices(db):
        listOfServices = ''
        try:
            conn = sqlite3.connect(db)
            conn.text_factory = str
            c = conn.cursor()
            c.execute('''   SELECT serviceName 
                            FROM Services 
                    ''')
            listOfServices = c.fetchall()       
        except Error as e:
            print(e)
            return e.message
        finally:
            conn.close()

        return listOfServices