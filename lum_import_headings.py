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
    mark_line_edit_error
)

class Headings(QWidget):
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

        #defining headings section
        headings_box = QGroupBox('Headings')
        layout.addWidget(headings_box)
        headings = QGridLayout()
        headings_box.setLayout(headings)

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

        self.list_line = QPlainTextEdit('')
        self.list_line.setEnabled(False)
        self.list_line.textChanged.connect(self.list_changed)
        headings.addWidget(self.list_line, 3, 1)

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
        mark_line_edit_error(self.range_line, bool(r))
        if r:
            list = ', '.join([str(i) for i in r])
            self.headings['r'] = r
            self.headings['l'] = r
            self.headings['list'] = list
            self.list_line.setPlainText(list)
            self.headings_changed.emit()

    def list_changed(self):
        '''Handels the event of changing list of headings
        
        Will emit signal only when valid string is provided.'''
        text = self.list_line.toPlainText().replace('\n', '')
        self.headings['list'] = text
        l = phriser_list(text)
        mark_line_edit_error(self.list_line, bool(l))
        if l:
            self.headings['l'] = l
            self.headings_changed.emit()


#testing
if __name__ == '__main__':
    
    app = QApplication([])

    window = TableControl()
    window.show()

    app.exec()