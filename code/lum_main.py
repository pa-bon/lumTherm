from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget, 
)
from lum_import import ImportWindow
from lum_plot_emission import EmissionPlot
from lum_plot_heatmap import HeatmapWithSlider


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
    
        # tabs setup
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)

        #import tab
        self.ImportTab = ImportWindow(self.path, self.holder)
        self.ImportTab.data_replaced.connect(self.update_plots)
        self.tabs.addTab(self.ImportTab, 'Import')

    def update_plots(self):
        '''Redraws the plots with new data'''

        self.holder.data = self.ImportTab.holder.data
        
        self.ratios = self.holder.calculate_ratios()
        self.sensitivity = self.holder.calculate_sensitivity()
        self.lines = self.holder.data.to_numpy()

        #remove tabs with heatmaps
        if self.tabs_present:
            self.tabs.removeTab(2)
            self.tabs.removeTab(2)
            self.tabs.removeTab(2)

        #emission plot tab
        self.EmPlotTab = EmissionPlot(self.holder.data)
        self.tabs.addTab(self.EmPlotTab, 'Plot')

        #intensity ratios plot
        self.RatiosPlotTab = HeatmapWithSlider(self.ratios, self.lines, self.holder.data.index, self.holder.data.columns)
        self.tabs.addTab(self.RatiosPlotTab, 'Ratios')
        
        #relative sensitivity plot
        self.SensitivityPlotTab = HeatmapWithSlider(self.sensitivity, self.lines, self.holder.data.index, self.holder.data.columns)
        self.tabs.addTab(self.SensitivityPlotTab, 'Sensitivity')
        
        self.tabs_present = True

#testing
if __name__ == '__main__':
    from lum_data import DataHolder

    holder = DataHolder()
    
    app = QApplication([])

    window = MainWindow('/home/beekeeper/programming/lumTherm/', holder)
    window.show()

    app.exec()

