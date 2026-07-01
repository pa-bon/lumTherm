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


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.ticklabel_format(style='sci',scilimits=(-3,4),axis='both')
        self.axes.yaxis.major.formatter._useMathText = True
        super().__init__(fig)


class EmissionPlot(QtWidgets.QWidget):

    def __init__(self, data: pd.DataFrame):
        super().__init__()

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)

        # setup the normalization and the colormap
        normalize = mcolors.Normalize(vmin=data.columns.min(), vmax=data.columns.max())
        colormap = cm.managua_r

        # plot
        data.sort_index(axis=1, inplace=True)
        for column in data.columns:
            self.sc.axes.plot(data[column], color=colormap(normalize(column)))

        # setup the colorbar
        self.scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
        self.scalarmappaple.set_array(data.columns)
        self.sc.figure.colorbar(self.scalarmappaple, ax=self.sc.axes)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        self.setLayout(layout)
    
    def redraw(self, data):
        try:
            #clear plot
            self.sc.axes.cla()
            
            #setup the normalization and the colormap
            normalize = mcolors.Normalize(vmin=data.columns.min(), vmax=data.columns.max())
            colormap = cm.managua_r

            #plot
            data.sort_index(axis=1, inplace=True)
            for column in data.columns:
                self.sc.axes.plot(data[column], color=colormap(normalize(column)))

            #update the range of the colorbar
            self.scalarmappaple.set_clim(data.columns.min(), data.columns.max())

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

    w = EmissionPlot(data)
    w.show()

    app.exec()       


