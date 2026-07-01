import pandas as pd

from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QWidget, 
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QBoxLayout,
    QTableView, 
    QLabel,
    QTabWidget, 
)
from lum_import import ImportWindow
from lum_data_tmp import Data_tmp
from lum_plot_emission import EmissionPlot


class MainWindow(QMainWindow):
    '''The main window of the program'''
    
    def __init__(self, path, holder):
        super().__init__() #use __init__() from QMainWindow 

        #variables
        #path
        self.path = path
        #data
        self.holder = holder
        
        #window properties
        self.setWindowTitle("lumTherm")
    

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)
        self.setCentralWidget(tabs)

        self.ImportTab = ImportWindow(self.path, self.holder)
        tabs.addTab(self.ImportTab, 'Import')

        self.EmPlotTab = EmissionPlot(self.holder.data)
        tabs.addTab(self.EmPlotTab, 'Plot')

        tabs.tabBarClicked.connect(self.tab_changed)
        
    def tab_changed(self):
        self.holder.data = self.ImportTab.holder.data
        self.EmPlotTab.redraw(self.holder.data)

#testing
if __name__ == '__main__':

    holder = Data_tmp()
    
    app = QApplication([])

    window = MainWindow('/home/beekeeper/programming/lumTherm/', holder)
    window.show()

    app.exec()

