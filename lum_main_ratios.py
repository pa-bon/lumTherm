from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout, 
    QLabel, 
    QLineEdit,
    QGroupBox,
    QSlider
)

from lum_plot_ratios import RatiosPlot
from lum_data_tmp import Data_tmp

class PlotRatiosTab(QWidget):
    '''Add or replace existing data'''

    def __init__(self, holder: Data_tmp):
        super().__init__()

        self.ratios = holder.calculate_ratios()

        #main layout
        L0 = QVBoxLayout()
        self.setLayout(L0)

        self.ratios_plot = RatiosPlot(self.ratios)
        L0.addWidget(self.ratios_plot)

        L1 = QHBoxLayout()
        L1.addWidget(QLabel(str(holder.data.columns.min())))

        slider = QSlider(orientation=Qt.Orientation.Horizontal)
        slider.setMaximum(0)
        slider.setMaximum(len(holder.data.columns)-1)
        slider.sliderMoved.connect(self.slider_moved)

        L1.addWidget(slider)
        L1.addWidget(QLabel(str(holder.data.columns.max())))

        L0.addLayout(L1)

  
    def slider_moved(self, num):
        '''Handels the event of changing the slider position'''
        self.ratios_plot.redraw(self.ratios, num)


#testing
if __name__ == '__main__':

    from pathlib import Path
    import pandas as pd

    with open(Path('/home/beekeeper/programming/lumTherm/PB_1_99_em_340-10K.csv'), 'r') as f:
        data = pd.read_csv(
                            f, 
                            sep=',', 
                            skiprows=list(range(22)),
                            header=0,
                            index_col=0
                        )

    data.dropna(how='all', axis=1, inplace=True)

    data.columns = list(range(340, 0, -10))

    holder = Data_tmp()
    holder.add_data(data)
    
    app = QApplication([])

    window = PlotRatiosTab(holder)
    window.show()

    app.exec()