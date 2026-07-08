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
    phriser_list,
    phriser_range,
    mark_text_edit_error
)

class HeadingsSettings(QWidget):
    '''Control the headings of the dataframe.
    
    The headings correspond to Y values, or 'z' axis in final 3D array'''
    
    #custom signals
    headings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setMaximumWidth(250)

        #controls
        self.headings_settings = {
            'source':'ro',           #take data from range or list
            'range':'',              #text seen by user
            'list':'',               #text seen by user
            'ro':0,                  #headings when source 'ro' (row) - 0 if first row, None otherwise
            'ra':[],                 #headings when source 'ra' (range)
            'li':[]                  #headings when source 'li' (list)
        }

        #main layout
        L0 = QVBoxLayout()
        self.setLayout(L0)

        #defining headings section
        headings_box = QGroupBox('Y axis (column names)')
        L0.addWidget(headings_box)
        L = QGridLayout()
        headings_box.setLayout(L)

        #labels
        L.addWidget(QLabel('First row'), 0, 1)
        L.addWidget(QLabel('Range (start, stop, step)'), 1, 1)
        L.addWidget(QLabel('List (number, number, ...)'), 3, 1)

        #toggles
        self.radio_row = QRadioButton()
        self.radio_row.setChecked(True)
        self.radio_row.toggled.connect(self.radio_row_toggled)
        L.addWidget(self.radio_row, 0, 0)

        self.radio_range = QRadioButton()
        self.radio_range.setChecked(False)
        self.radio_range.toggled.connect(self.radio_range_toggled)
        L.addWidget(self.radio_range, 1, 0)

        self.radio_list = QRadioButton()
        self.radio_list.setChecked(False)
        self.radio_list.toggled.connect(self.radio_list_toggled)
        L.addWidget(self.radio_list, 3, 0)

        self.range_line = QLineEdit('')
        self.range_line.setEnabled(False)
        self.range_line.textChanged.connect(self.range_changed)
        L.addWidget(self.range_line, 2, 1)

        self.list_line = QPlainTextEdit('')
        self.list_line.setEnabled(False)
        self.list_line.textChanged.connect(self.list_changed)
        L.addWidget(self.list_line, 4, 1)

    def radio_row_toggled(self, selected):
        '''Handels the event of selecting the row option'''
        if selected:
            self.headings_settings['source'] = 'ro'
            self.headings_settings['ro'] = 0
            self.range_line.setEnabled(False)
            self.list_line.setEnabled(False)
            self.headings_changed.emit()

    def radio_range_toggled(self, selected):
        '''Handels the event of selecting the range option'''
        if selected:
            self.headings_settings['source'] = 'ra'
            self.headings_settings['ro'] = None
            self.range_line.setEnabled(True)
            self.list_line.setEnabled(False)
            self.headings_changed.emit()

    def radio_list_toggled(self, selected):
        '''Handels the event of selecting the list option'''
        if selected:
            self.headings_settings['source'] = 'li'
            self.headings_settings['ro'] = None
            self.range_line.setEnabled(False)
            self.list_line.setEnabled(True)
            self.headings_changed.emit()


    def range_changed(self, text):
        '''handels the event of changing range for headings
        
        Will insert the list based on range into the list slot, 
        overriding what is already there.
        
        Will emit signal only when valid string is provided.'''
        self.headings_settings['range'] = text
        ra = phriser_range(text)
        mark_text_edit_error(self.range_line, bool(ra))
        if ra:
            list = ', '.join([str(i) for i in ra])
            self.headings_settings['ra'] = ra
            self.headings_settings['li'] = ra
            self.headings_settings['list'] = list
            self.list_line.setPlainText(list)
            self.headings_changed.emit()

    def list_changed(self):
        '''Handels the event of changing list of headings
        
        Will emit signal only when valid string is provided.'''
        text = self.list_line.toPlainText().replace('\n', '')
        self.headings_settings['list'] = text
        li = phriser_list(text)
        mark_text_edit_error(self.list_line, bool(li))
        if li:
            self.headings_settings['li'] = li
            self.headings_changed.emit()


#testing
if __name__ == '__main__':
    
    app = QApplication([])

    window = HeadingsSettings()
    window.show()

    app.exec()