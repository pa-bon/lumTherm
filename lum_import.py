import pandas as pd

from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QWidget, 
    QHBoxLayout,
    QVBoxLayout,
    QTableView, 
    QLabel, 
)
from lum_import_browse import Browse
from lum_import_add_data import AddReplace
from lum_import_reading import Reading
from lum_import_headings import HeadingsSettings
from lum_import_indexes import IndexesSettings
from lum_import_table import TableModel
from lum_import_info import DataInfo
from lum_data_tmp import Data_tmp


class ImportWindow(QWidget):
    '''The dialog window for importing from file'''
    
    def __init__(self, path, holder):
        super().__init__() #use __init__() from QMainWindow 

        #variables
        #path
        self.path = path
        #data holder
        self.holder = holder
        #raw_data
        self.raw_data = pd.DataFrame()
        
        #window properties
        self.setWindowTitle("Import from text file")
        
        #layout initialization
        L = QVBoxLayout()
        #widget = QWidget()
        self.setLayout(L)
        #self.setCentralWidget(widget)

        #browse tab
        self.Browse = Browse(self.path)
        L.addWidget(self.Browse)

        self.Browse.path_changed.connect(self.update_path)

        #table tap
        L2 = QHBoxLayout()
        L.addLayout(L2)
        
        #table widget
        self.Table = QTableView()
        L2.addWidget(self.Table)

        #table data (model)
        self.TableModel = TableModel(self.raw_data)
        self.Table.setModel(self.TableModel)
        
        #widget with controls
        L3 = QVBoxLayout()
        self.DataInfo = DataInfo(self.raw_data.shape)
        L3.addWidget(self.DataInfo)
        self.Reading = Reading()
        L3.addWidget(self.Reading)
        self.Indexes = IndexesSettings()
        L3.addWidget(self.Indexes)
        self.Headings = HeadingsSettings()
        L3.addWidget(self.Headings)
        L2.addLayout(L3)

        self.Reading.reading_changed.connect(self.update_reading)
        self.Indexes.index_changed.connect(self.update_index)
        self.Headings.headings_changed.connect(self.update_headings)

        #add and replace tab
        self.AddReplace = AddReplace()
        L.addWidget(self.AddReplace)

        self.AddReplace.add_signal.connect(self.add_data)
        self.AddReplace.repalce_signal.connect(self.replace_data)

        #message lable
        self.ImportMessage = QLabel('Messages: none')
        L.addWidget(self.ImportMessage)

    def update_path(self):
        '''Handles the event of path changing'''
        self.path = self.Browse.path
        self.read_text_file(self.path)
        self.update_table(self.raw_data)

    def update_reading(self):
        '''Handels the event of reding controls chaneging'''
        self.read_text_file(self.path)
        self.update_table(self.raw_data)
    
    def update_index(self):
        self.read_text_file(self.path)

        if self.Indexes.indexes_settings['source'] == 'ra':
            if len(self.raw_data.index) == len(self.Indexes.indexes_settings['ra']):
                self.raw_data.index = self.Indexes.indexes_settings['ra']
            else:
                self.raw_data.index = range(len(self.raw_data.index))
    
        self.update_table(self.raw_data)
    
    def update_headings(self):
        '''Handels the event of headings changing'''
        headings_list = self.Headings.headings_settings[self.Headings.headings_settings['source']]
        if len(headings_list) == len(self.raw_data.columns):
            self.raw_data.columns = headings_list
        
        #update table
        self.update_table(self.raw_data)
    
    def update_table(self, data):
        '''Updates data in the table and the data info window'''
        self.TableModel = TableModel(data)
        self.Table.setModel(self.TableModel)
        self.DataInfo.update(self.raw_data.shape)
    
    def read_text_file(self, path):
        '''Reads the file provided
        
        Firstly, tryes to use pandas read_csv() function.
        If unsuccesfull, tries to diplay all lines in file as rows in one column.
        If still unsucesfull, displayes the error message'''
        try:
            #read_csv()
            with open(Path(path), 'r') as f:
                self.raw_data = pd.read_csv(
                    f, 
                    sep=self.Reading.read_controls['delimiter'], 
                    skiprows=self.Reading.read_controls['skr'],
                    usecols=self.Reading.read_controls['uc'],
                    header=0,
                    index_col=self.Indexes.indexes_settings['co']
                )

            #when rows have difrent number of delimiters, they are treated as indexes for an empty column
            #this enshures that only proper (numerical) indexes are assigned
            assert float(self.raw_data.index[1])
            self.ImportMessage.setText('Message: file red')
                
        except:
            print('failed')
            #read file as lines
            try:
                with open(Path(path), 'r') as f:
                    self.raw_data = pd.DataFrame([s.replace('\n', '') for s in f.readlines()])
                    assert float(self.raw_data.index[1])
                self.ImportMessage.setText('Message: file red')
            #all hope lost
            except:
                self.ImportMessage.setText('ERROR: Invalid file format. Use human-redable text file with UTC-8 encoding')
        
        #delete empty columns
        self.raw_data.dropna(how='all', axis=1, inplace=True)

        #store headings
        self.Headings.headings_settings['ro'] = self.raw_data.columns

        return self.raw_data
    
    def add_data(self):
        '''Adds data in current view to the total'''
        self.holder.add_data(self.raw_data)
    
    def replace_data(self):
        '''Replaces data from the current view in the total'''
        self.holder.replace_data(self.raw_data)  


#testing
if __name__ == '__main__':

    holder = Data_tmp()
    
    app = QApplication([])

    window = ImportWindow('/home/beekeeper/programming/lumTherm/', holder)
    window.show()

    app.exec()

    holder = window.holder

    print(holder)

