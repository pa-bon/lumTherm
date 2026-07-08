from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QHBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton,
    QFileDialog
)

class Browse(QWidget):
    '''Browsing file section of the import window'''
    
    #custom signal
    path_changed = pyqtSignal()

    def __init__(self, path):
        super().__init__()

        #holds path to file
        self.path = path    

        #main layout
        L = QHBoxLayout()
        self.setLayout(L)

        #unchanging label
        L.addWidget(QLabel("File path:"))
        
        #space for typing/pasting/coping file path
        self.path_line = QLineEdit(self.path)
        self.path_line.textChanged.connect(self.path_line_changed)
        
        L.addWidget(self.path_line)

        #the 'Browse' button
        button = QPushButton("Browse")
        button.clicked.connect(self.browse_files)

        L.addWidget(button)

        #the select-file dialog window, activated when the 'Browse' button is pressed
        self.dialog = QFileDialog()
        self.dialog.setDirectory(self.path)     #set home directory
  
    def browse_files(self):
        '''Handles event of clicking the browse button'''
        file_name, _ = self.dialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '', 'All Files (*);;CSV Files (*.csv);;TXT files (*.txt)')
        self.path = file_name
        self.path_line.setText(self.path)

    def path_line_changed(self, text):
        '''Handels event of path line changing'''
        self.path = text
        self.dialog.setDirectory(text)
        self.path_changed.emit()



#testing
if __name__ == '__main__':
    
    app = QApplication([])

    window = Browse('/home/beekeeper/programming/lumTherm/')
    window.show()

    app.exec()

    print(window.path)

