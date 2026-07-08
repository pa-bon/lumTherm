from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout,
    QGridLayout, 
    QLabel, 
    QLineEdit,
    QRadioButton,
    QGroupBox
)
from lum_tools import (
    phriser_range,
    mark_text_edit_error
)

class IndexesSettings(QWidget):
    '''Control the indexes of the dataframe.
    
    The indexes correspond to X values, or 'x' and 'y' axis in final 3D array'''
    
    #custom signals
    index_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setMaximumWidth(250)

        #controls
        self.indexes_settings = {
            'source':'co',           #take data from range or list
            'range':'',               #text seen by user
            'co':0,                 #0 when first column is to be used, False when index comes from range
            'ra':[],                 #headings when source 'ra' (range)
        }

        #main layout
        L0 = QVBoxLayout()
        self.setLayout(L0)

        #defining headings section
        index_box = QGroupBox('X axis (row names)')
        L0.addWidget(index_box)
        L = QGridLayout()
        index_box.setLayout(L)

        #labels
        L.addWidget(QLabel('First column'), 0, 1)
        L.addWidget(QLabel('Range (start, stop, step)'), 1, 1)

        #toggles
        self.radio_column = QRadioButton()
        self.radio_column.setChecked(True)
        self.radio_column.toggled.connect(self.radio_column_toggled)
        L.addWidget(self.radio_column, 0, 0)

        self.radio_range = QRadioButton()
        self.radio_range.setChecked(False)
        self.radio_range.toggled.connect(self.radio_range_toggled)
        L.addWidget(self.radio_range, 1, 0)

        self.range_line = QLineEdit('')
        self.range_line.setEnabled(False)
        self.range_line.textChanged.connect(self.range_changed)
        L.addWidget(self.range_line, 2, 1)

    def radio_column_toggled(self, selected):
        '''Handels the event of selecting the column option'''
        if selected:
            self.indexes_settings['source'] = 'co'
            self.indexes_settings['co'] = 0
            self.range_line.setEnabled(False)
            self.index_changed.emit()

    def radio_range_toggled(self, selected):
        '''Handels the event of selecting the range option'''
        if selected:
            self.indexes_settings['source'] = 'ra'
            self.indexes_settings['co'] = False
            self.range_line.setEnabled(True)
            self.index_changed.emit()

    def range_changed(self, text):
        '''handels the event of changing range for indexes
        
        Will insert the list based on range into the list slot, 
        overriding what is already there.
        
        Will emit signal only when valid string is provided.'''
        self.indexes_settings['range'] = text
        ra = phriser_range(text)
        mark_text_edit_error(self.range_line, bool(ra))
        if ra:
            self.indexes_settings['ra'] = ra
            self.index_changed.emit()

#testing
if __name__ == '__main__':
    
    app = QApplication([])

    window = IndexesSettings()
    window.show()

    app.exec()