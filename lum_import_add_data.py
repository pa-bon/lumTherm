from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QHBoxLayout, 
    QPushButton,
)

class AddReplace(QWidget):
    '''Add or replace existing data'''
    
    #custom signals
    add_signal = pyqtSignal()
    repalce_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        #main layout
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)
       

        #the 'Replace' button
        replace_button = QPushButton("Replace")
        replace_button.clicked.connect(self.replace)

        layout.addWidget(replace_button)

        #the 'Add' button
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add)

        layout.addWidget(add_button)

  
    def replace(self):
        '''Propagets signal of clicking the replace button'''
        self.repalce_signal.emit()
    
    def add(self):
        '''Propagates signal of clicking the add button'''
        self.add_signal.emit()

#testing
if __name__ == '__main__':
    
    app = QApplication([])

    window = AddReplace()
    window.show()

    app.exec()