import sqlite3
from encryption import *

class SaveData:
    def insert(userID, password, serviceName):
        # Establish db connection

        # Build insert query

        # Insert Data
        encryptedPass = encryptPassword(password)

        # If save is successful return true else return false
        if():
            return True
        else:
            return False
        
        # Commit and close connection

class RetrieveData:
    def retrievePassword(userID):
        password = ''
        return PasswordEncryption.unencryptPassword(password)
    
    def retrieveServices(userID):
        return listOfThings
