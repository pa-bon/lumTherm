import os

os.environ["QT_API"] = "PyQt6"

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

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np

class MplCanvas(FigureCanvasQTAgg):
    """Menages general plot styles"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        
        fig, self.axs = plt.subplot_mosaic(
            [['A', '.'], ['heatmap', 'B']],
            figsize=(width, height), 
            dpi=dpi,
            width_ratios=(4, 1), 
            height_ratios=(1, 4),
            layout='constrained')

        self.axs['A'].tick_params(axis="x", labelbottom=False)
        self.axs['B'].tick_params(axis="y", labelbottom=False)

        self.axs['heatmap'].ticklabel_format(style='sci',scilimits=(-3,4),axis='both')
        self.axs['heatmap'].yaxis.major.formatter._useMathText = True
        self.axs['heatmap'].xaxis.major.formatter._useMathText = True
        super().__init__(fig)

class Heatmap2(QWidget):
    """Manages the imshow() plot of a square, 2D np.array, with line plots along both axes"""

    def __init__(self, data: np.array, line: np.array, xvalues=[],):
        super().__init__()

        #determine limits of axes
        try:        
            (xmin, xmax) = (min(xvalues), max(xvalues))
        except:
            (xmin, xmax) = (0, data.shape[0])

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=6, height=5, dpi=100)

        # plot heatmap
        self.plot = self.sc.axs['heatmap'].imshow(
            data, 
            aspect=1, 
            interpolation='nearest', 
            cmap='managua_r', 
            norm='log', 
            extent=(xmin, xmax, xmax, xmin), 
            origin='upper'
            )
        
        #update the axis range
        self.sc.axs['heatmap'].set(xlim=(xmin, xmax), ylim=(xmax, xmin))

        #plot lines
        self.lineA = self.sc.axs['A'].plot(xvalues, line)
        self.lineB = self.sc.axs['A'].plot(xvalues, line)

        # setup the colorbar
        self.colorbar = self.sc.figure.colorbar(self.plot, ax=self.sc.axs['heatmap'])

        #create toolbar, passing canvas as first parament, parent (self) as second.
        toolbar = NavigationToolbar(self.sc, self)

        L = QVBoxLayout()
        L.addWidget(toolbar)
        L.addWidget(self.sc)
        self.setLayout(L)
    
    def redraw(self, data: np.array):
        try:
            #update data
            self.plot.set_data(data)
            
            #adjust colrbar
            self.colorbar.mappable.set_clim(data.min(), data.max())

            #redraw
            self.sc.draw()

            return 'Plot updated'
        
        except TypeError:

            return 'Plot update failed: invalid column headings'

class Heatmap2WithSlider(QWidget):
    """A heatmap with an interactive slider.
    
    The slider selcts a 2D slice from a 3D np.array for plotting. 
    The shape of the 3D array must be (n, n, m), so tht the 2D slices will be square"""

    def __init__(self, data: np.array, lines: np.array, xvalues=[], zvalues=[]):
        super().__init__()

        self.zvalues = zvalues
        self.data = data
        self.lines = lines

        #determine limits of z axis
        try:        
            (zmin, zmax) = (min(zvalues), max(zvalues))
        except:
            (zmin, zmax) = (0, data.shape[2])
            self.zvalues = range(zmax)

        #main layout
        L0 = QVBoxLayout()
        self.setLayout(L0)

        self.heatmap = Heatmap2(self.data[:,:,0], self.lines[:,0], xvalues=xvalues)
        L0.addWidget(self.heatmap)

        L1 = QHBoxLayout()
        L1.addWidget(QLabel(str(zmin)))

        slider = QSlider(orientation=Qt.Orientation.Horizontal)
        slider.setMaximum(0)
        slider.setMaximum(len(holder.data.columns)-1)
        slider.valueChanged.connect(self.value_changed)

        L1.addWidget(slider)

        L1.addWidget(QLabel(str(zmax)))

        self.slice_label = QLabel(f'Current: {self.zvalues[0]}')
        L1.addWidget(self.slice_label)

        L0.addLayout(L1)

  
    def value_changed(self, num):
        '''Handels the event of changing the slider position'''
        self.heatmap.redraw(self.data[:,:,num])
        self.slice_label.setText(f'Current: {self.zvalues[num]}')

if __name__ == '__main__':

    from pathlib import Path
    import pandas as pd
    from lum_data_tmp import Data_tmp

    app = QApplication([])

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
    holder.data.sort_index(axis=1, inplace=True)
    lines = holder.data.to_numpy()
    
    ratios = holder.calculate_sensitivity()


    w = Heatmap2WithSlider(ratios, lines, xvalues=holder.data.index, zvalues=holder.data.columns)
    w.show()

    app.exec()      