import os

os.environ["QT_API"] = "PyQt6"

from PyQt6 import QtCore, QtWidgets

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np

from pathlib import Path

import pandas as pd

from lum_data_tmp import Data_tmp

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.ticklabel_format(style='sci',scilimits=(-3,4),axis='both')
        self.axes.yaxis.major.formatter._useMathText = True
        super().__init__(fig)


class RatiosPlot(QtWidgets.QWidget):

    def __init__(self, data: np.array, slice=-1, xvalues=[]):
        super().__init__()

        try:        
            (xmin, xmax) = (min(xvalues), max(xvalues))
        except:
            (xmin, xmax) = (0, data.shape[0])

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)

        # plot
        self.plot = self.sc.axes.imshow(
            data[:,:,slice], 
            aspect=1, 
            interpolation='nearest', 
            cmap='managua_r', 
            norm='log', 
            extent=(xmin, xmax, xmin, xmax), 
            origin='lower'
            )
        self.sc.axes.set(xlim=(xmin, xmax), ylim=(xmin, xmax))

        # setup the colorbar
        self.colorbar = self.sc.figure.colorbar(self.plot, ax=self.sc.axes)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        self.setLayout(layout)
    
    def redraw(self, data: np.array, slice):
        try:
            #clear plot
            self.sc.axes.cla()

            #plot
            self.plot = self.sc.axes.imshow(data[:,:,slice], aspect=1, interpolation='nearest', cmap='managua_r', norm='log')
            
            self.colorbar.mappable.set_clim(data[:,:,slice].min(), data[:,:,slice].max())

            self.sc.draw()

        except TypeError:
            print('column labels must by numbers')


if __name__ == '__main__':

    app = QtWidgets.QApplication([])

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
    ratios = holder.calculate_ratios()


    w = RatiosPlot(ratios, xvalues=holder.data.index)
    w.show()

    app.exec()      