from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow, 
    QWidget, 
    QHBoxLayout,
    QVBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton,
    QFileDialog
)
from lum_import_browse import Browse
from lum_import_add_data import AddReplace

class ImportWindow(QMainWindow):
    '''The dialog window for importing from file'''
    
    def __init__(self, path):
        super().__init__() #use __init__() from QMainWindow 

        #variables
        self.path = path
        
        #window properties
        self.setWindowTitle("Import from text file")
        
        #layout initialization
        L = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(L)
        self.setCentralWidget(widget)


        self.browse_tab = Browse(self.path)
        L.addWidget(self.browse_tab)

        self.browse_tab.path_changed.connect(self.update_path)

        self.add_replace_tab = AddReplace()
        L.addWidget(self.add_replace_tab)

    def update_path(self):
        self.path = self.browse_tab.path

#testing
if __name__ == '__main__':
    
    app = QApplication([])

    window = ImportWindow('/home/beekeeper/programming/lumTherm/')
    window.show()

    app.exec()

    print(window.path)