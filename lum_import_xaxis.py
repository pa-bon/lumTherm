from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout,
    QGridLayout, 
    QLabel, 
    QLineEdit,
    QRadioButton,
    QPlainTextEdit,
    QGroupBox
)
from lum_tools import (
    phriser,
    phriser_list,
    phriser_range,
    mark_text_edit_error
)

class XAxis(QWidget):
    '''Add or replace existing data'''
    
    #custom signals
    #notifies when source or headings (r or l) change
    index_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setMaximumWidth(250)

        #controls
        self.index = {
            'source':'co',           #take data from range or list
            'range':'',               #text seen by user
            'co':[],                 #headings when source 'co' (column)
            'ra':[],                 #headings when source 'ra' (range)
        }

        #main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        #defining headings section
        index_box = QGroupBox('X axis (row names)')
        layout.addWidget(index_box)
        index = QGridLayout()
        index_box.setLayout(index)

        #labels
        index.addWidget(QLabel('First column'), 0, 1)
        index.addWidget(QLabel('Range (start, stop, step)'), 1, 1)

        #toggles
        self.radio_column = QRadioButton()
        self.radio_column.toggled.connect(self.radio_column_toggled)
        index.addWidget(self.radio_column, 0, 0)

        self.radio_range = QRadioButton()
        self.radio_range.setChecked(True)
        self.radio_range.toggled.connect(self.radio_range_toggled)
        index.addWidget(self.radio_range, 1, 0)

        self.range_line = QLineEdit('')
        self.range_line.textChanged.connect(self.range_changed)
        index.addWidget(self.range_line, 2, 1)

    def radio_column_toggled(self, selected):
        '''Handels the event of selecting the column option'''
        if selected:
            self.index['source'] = 'co'
            self.range_line.setEnabled(False)
            self.index_changed.emit()

    def radio_range_toggled(self, selected):
        '''Handels the event of selecting the range option'''
        if selected:
            self.index['source'] = 'ra'
            self.range_line.setEnabled(True)
            self.index_changed.emit()

    def range_changed(self, text):
        '''handels the event of changing range for headings
        
        Will insert the list based on range into the list slot, 
        overriding what is already there.
        
        Will emit signal only when valid string is provided.'''
        self.index['range'] = text
        ra = phriser_range(text)
        mark_text_edit_error(self.range_line, bool(ra))
        if ra:
            self.index['ra'] = ra
            self.index_changed.emit()

#testing
if __name__ == '__main__':
    
    app = QApplication([])

    window = XAxis()
    window.show()

    app.exec()