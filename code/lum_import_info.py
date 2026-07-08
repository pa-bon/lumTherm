from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout,
    QLabel,
    QGroupBox
)

class DataInfo(QWidget):
    '''A simple lable to communicate the table's shape'''
    def __init__(self, shape):
        super().__init__()
        
        self.shape = shape

        self.setMaximumWidth(250)

        self.box = QGroupBox('Info')
        L0 = QVBoxLayout()
        L0.addWidget(self.box)
        self.setLayout(L0)

        L = QVBoxLayout()

        self.DataShape = QLabel()

        L.addWidget(self.DataShape)

        self.box.setLayout(L)
        
        self.update(shape)
    
    def update(self, shape):
        self.shape = shape
        self.DataShape.setText(f'{self.shape[1]} columns\n{self.shape[0]} rows')

#testing
if __name__ == '__main__':
    
    app = QApplication([])

    window = DataInfo((0,0))
    window.show()

    app.exec()