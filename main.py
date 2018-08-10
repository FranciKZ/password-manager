from databaseFunction import SaveData, RetrieveData
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont
import os
import sys
import os.path

def restOfCode():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(100, 100)

        # x, y, width, height
        self.setGeometry(500, 500, 600, 300)
        self.setWindowTitle('Icon')
        self.show()

def main():
    #how to use databaseFunction functions
    db = 'pass_manager_db.db'
    if not os.path.isfile(db):
        print('Not found')
        SaveData.createDB(None)
        restOfCode()
    else:
        # Just do the rest of the code
        restOfCode()
    return True
    # app = QApplication(sys.argv)
    # ex = Example()
    # sys.exit(app.exec_())    

if __name__ == '__main__':
    main()