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

class Reading(QWidget):
    '''Add or replace existing data'''
    
    #custom signals
    
    #notifies when delimiter, rows to skip (skr) or columns to use (uc) change
    reading_changed = pyqtSignal()
    
    #notifies when source or headings (r or l) change
    headings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setMaximumWidth(250)

        #controls
        self.read_controls = {
            'delimiter':',',        #delimiter
            'skip_rows':'',         #text seen by user
            'use_columns':'',       #text seen by user
            'skr':[],               #numbers of rows to skip
            'uc':[]                 #numbers of columns to use
        }


        #main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        #reading from file section
        reading_box = QGroupBox('Reading')
        layout.addWidget(reading_box)
        reading = QGridLayout()
        reading_box.setLayout(reading)
        
        #labels
        reading.addWidget(QLabel('Delimiter:'), 0, 0)
        reading.addWidget(QLabel('Skip rows:'), 1, 0)
        reading.addWidget(QLabel('Use columns:'), 2, 0)

        #input fields
        self.delimiter_line = QLineEdit(self.read_controls['delimiter'])
        self.delimiter_line.textChanged.connect(self.delimiter_changed)
        reading.addWidget(self.delimiter_line, 0, 1)

        self.skip_rows_line = QLineEdit(self.read_controls['skip_rows'])
        self.skip_rows_line.textChanged.connect(self.skip_rows_changed)
        reading.addWidget(self.skip_rows_line, 1, 1)

        self.use_columns_line = QLineEdit(self.read_controls['use_columns'])
        self.use_columns_line.textChanged.connect(self.use_columns_changed)
        reading.addWidget(self.use_columns_line, 2, 1)
  
    def delimiter_changed(self, text):
        '''Handels the event of changing the delimeter'''
        self.read_controls['delimiter'] = text
        self.reading_changed.emit()

    def skip_rows_changed(self, text):
        '''Handels the event of changing rows to skip
        
        Will emit signal only when valid string is provided.'''
        self.read_controls['skip_rows'] = text
        valid, skr = phriser(text)
        mark_text_edit_error(self.skip_rows_line, valid)
        if valid:
            self.read_controls['skr'] = skr
            self.reading_changed.emit()
            
    def use_columns_changed(self, text):
        '''Handels the event of changing column to use
        
        Will emit signal only when valid string is provided.'''
        self.read_controls['use_columns'] = text
        valid, uc = phriser(text)
        mark_text_edit_error(self.use_columns_line, valid)
        if valid:
            self.read_controls['uc'] = uc
            self.reading_changed.emit()


#testing
if __name__ == '__main__':
    
    app = QApplication([])

    window = Reading()
    window.show()

    app.exec()