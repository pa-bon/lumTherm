from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout,
    QGridLayout, 
    QLabel, 
    QLineEdit,
    QRadioButton
)
from lum_tools import (
    phriser,
    phriser_list,
    phriser_range
)

class TableControl(QWidget):
    '''Add or replace existing data'''
    
    #custom signals
    
    #notifies when delimiter, rows to skip (skr) or columns to use (uc) change
    reading_changed = pyqtSignal()
    
    #notifies when source or headings (r or l) change
    headings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        #controls
        self.read_controls = {
            'delimiter':',',        #delimiter
            'skip_rows':'',         #text seen by user
            'use_columns':'',       #text seen by user
            'skr':[],               #numbers of rows to skip
            'uc':[]                 #numbers of columns to use
        }

        self.headings = {
            'source':'r',           #take data from range or list
            'range':'',             #text seen by user
            'list':'',              #text seen by user
            'r':[],                 #headings when source 'r' (range)
            'l':[]                  #headings when source 'l' (list)
        }

        #main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        #reading from file section
        layout.addWidget(QLabel('Reading'))

        reading = QGridLayout()
        layout.addLayout(reading)
        
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

        self.skip_columns_line = QLineEdit(self.read_controls['use_columns'])
        self.skip_columns_line.textChanged.connect(self.skip_columns_changed)
        reading.addWidget(self.skip_columns_line, 2, 1)

        #defining headings section
        layout.addWidget(QLabel('Headings'))

        headings = QGridLayout()
        layout.addLayout(headings)

        #labels
        headings.addWidget(QLabel('Range (start, stop, step)'), 0, 1)
        headings.addWidget(QLabel('List (number, number, ...)'), 2, 1)

        #toggles
        self.radio_range = QRadioButton()
        self.radio_range.setChecked(True)
        self.radio_range.toggled.connect(self.radio_range_toggled)
        headings.addWidget(self.radio_range, 0, 0)

        self.radio_list = QRadioButton()
        self.radio_list.toggled.connect(self.radio_list_toggled)
        headings.addWidget(self.radio_list, 2, 0)

        #input fields
        self.range_line = QLineEdit('')
        self.range_line.textChanged.connect(self.range_changed)
        headings.addWidget(self.range_line, 1, 1)

        self.list_line = QLineEdit('')
        self.list_line.setEnabled(False)
        self.list_line.textChanged.connect(self.list_changed)
        headings.addWidget(self.list_line, 3, 1)

  
    def delimiter_changed(self, text):
        '''Handels the event of changing the delimeter'''
        self.read_controls['delimiter'] = text
        self.reading_changed.emit()

    def skip_rows_changed(self, text):
        '''Handels the event of changing rows to skip
        
        Will emit signal only when valid string is provided.'''
        self.read_controls['skip_rows'] = text
        skr = phriser(text)
        if skr:
            self.read_controls['skr'] = skr
            self.reading_changed.emit()

    def skip_columns_changed(self, text):
        '''Handels the event of changing column to use
        
        Will emit signal only when valid string is provided.'''
        self.read_controls['use_columns'] = text
        uc = phriser(text)
        if uc:
            self.read_controls['uc'] = uc
            self.reading_changed.emit()

    def radio_range_toggled(self, selected):
        '''Handels the event of selecting the range option'''
        if selected:
            self.headings['source'] = 'r'
            self.range_line.setEnabled(True)
            self.list_line.setEnabled(False)
            self.headings_changed.emit()

    def radio_list_toggled(self, selected):
        '''Handels the event of selecting the list option'''
        if selected:
            self.headings['source'] = 'l'
            self.range_line.setEnabled(False)
            self.list_line.setEnabled(True)
            self.headings_changed.emit()
    
    def range_changed(self, text):
        '''handels the event of changing range for headings
        
        Will insert the list based on range into the list slot, 
        overriding what is already there.
        
        Will emit signal only when valid string is provided.'''
        self.headings['range'] = text
        r = phriser_range(text)
        if r:
            list = ', '.join([str(i) for i in r])
            self.headings['r'] = r
            self.headings['l'] = r
            self.headings['list'] = list
            self.list_line.setText(list)
            self.headings_changed.emit()

    def list_changed(self, text):
        '''Handels the event of changing list of headings
        
        Will emit signal only when valid string is provided.'''
        self.headings['list'] = text
        l = phriser_list(text)
        if l:
            self.headings['l'] = l
            self.headings_changed.emit()

#testing
if __name__ == '__main__':
    
    app = QApplication([])

    window = TableControl()
    window.show()

    app.exec()