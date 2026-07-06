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
from lum_plot_heatmap3 import Heatmap3WithSlider


class MainWindow(QMainWindow):
    '''The main window of the program'''
    
    def __init__(self, path, holder):
        super().__init__() #use __init__() from QMainWindow 

        #variables
        #path
        self.path = path
        #data
        self.holder = holder
        #tabs_present
        self.tabs_present = False
        
        #window properties
        self.setWindowTitle("lumTherm")
    

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)

        self.ImportTab = ImportWindow(self.path, self.holder)
        self.ImportTab.data_replaced.connect(self.update_plots)
        self.tabs.addTab(self.ImportTab, 'Import')


        self.EmPlotTab = EmissionPlot(self.holder.data)
        self.tabs.addTab(self.EmPlotTab, 'Plot')

        #tabs.tabBarClicked.connect(self.tab_changed)
        
    #def tab_changed(self):
    #    self.holder.data = self.ImportTab.holder.data
    #    self.EmPlotTab.redraw(self.holder.data)

    def update_plots(self):
        self.holder.data = self.ImportTab.holder.data
        self.EmPlotTab.redraw(self.holder.data)
        
        self.ratios = self.holder.calculate_ratios()
        self.sensitivity = self.holder.calculate_sensitivity()
        self.lines = self.holder.data.to_numpy()

        if self.tabs_present:
            self.tabs.removeTab(2)
            self.tabs.removeTab(2)

        self.RatiosPlotTab = Heatmap3WithSlider(self.ratios, self.lines, self.holder.data.index, self.holder.data.columns)
        self.tabs.addTab(self.RatiosPlotTab, 'Ratios')
        
        self.SensitivityPlotTab = Heatmap3WithSlider(self.sensitivity, self.lines, self.holder.data.index, self.holder.data.columns)
        self.tabs.addTab(self.SensitivityPlotTab, 'Sensitivity')
        
        self.tabs_present = True



        
        
        

#testing
if __name__ == '__main__':

    holder = Data_tmp()
    
    app = QApplication([])

    window = MainWindow('/home/beekeeper/programming/lumTherm/', holder)
    window.show()

    app.exec()

