from databaseFunction import SaveData, RetrieveData
import os
import os.path

def restOfCode():
    return False

def main():
    # how to use databaseFunction functions
    if not os.path.isfile('password_manager_db.db'):
        SaveData.createDB(None)
        restOfCode()
    else:
        #do the rest of the code
        restOfCode()
    return True

if __name__ == '__main__':
    main()