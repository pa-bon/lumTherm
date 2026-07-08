import os

os.environ["QT_API"] = "PyQt6"

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
import matplotlib.cm as cm

import numpy as np

class MplCanvas(FigureCanvasQTAgg):
    """Menages general plot styles"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        
        #create figure
        fig = Figure(
            layout='constrained',
            figsize=(width, height),
            dpi=dpi
            )

        #add main axis (for heatmap)
        self.ax = fig.add_subplot()

        #add aditional axis for line plots
        self.ax_A = self.ax.inset_axes([0, 1.05, 1, 0.25], sharex=self.ax)
        self.ax_B = self.ax.inset_axes([1.05, 0, 0.25, 1], sharey=self.ax)

        #costumise appreance
        self.ax_A.tick_params(axis="both", labelbottom=False, left=False, labelleft=False)
        self.ax_B.tick_params(axis="both", labelleft=False, bottom=False, labelbottom=False)
        self.ax.ticklabel_format(style='sci',scilimits=(-3,4),axis='both')
        self.ax.yaxis.major.formatter._useMathText = True
        self.ax.xaxis.major.formatter._useMathText = True
        
        super().__init__(fig)

class Heatmap(QWidget):
    """Manages the imshow() plot of a square, 2D np.array, with line plots along both axes 
    with indicator lines responding to current cursor position
    
        data: 2D np.array
    
        line: 1D np.array
    
        line_color: color of line plots (default blue)
    
        xvalues: list of values corresponding to 'x' (and 'y') axis of data and 'x' axis of line,
        default - counting numbers starting from 0"""

    def __init__(self, data: np.array, line: np.array, line_color='blue', xvalues=[]):
        super().__init__()

        #test input data
        assert data.shape[0] == data.shape[1]
        assert data.shape[0] == line.shape[0]

        #store shape for further tests
        self._data_shape = data.shape

        #determine limits of axes
        try:        
            (xmin, xmax) = (min(xvalues), max(xvalues))
            self.xvalues = xvalues
        except:
            (xmin, xmax) = (0, data.shape[0])
            self.xvalues = range(xmax)

        # Create the maptlotlib FigureCanvas object
        self.sc = MplCanvas(self, width=8, height=7, dpi=100)
        self.sc.mpl_connect('motion_notify_event', self.mouse_moved_on_plot)

        # plot heatmap
        self.plot = self.sc.ax.imshow(
            data, 
            aspect=1, 
            interpolation='nearest', 
            cmap='managua_r', 
            norm='log', 
            extent=(xmin, xmax, xmax, xmin), 
            origin='upper'
            )
        
        #update the axis range
        self.sc.ax.set(xlim=(xmin, xmax), ylim=(xmax, xmin))

        #plot lines (plot returns a list)
        [self.lineA] = self.sc.ax_A.plot(xvalues, line, color=line_color)
        [self.lineB] = self.sc.ax_B.plot(line, xvalues, color=line_color)

        #plot position indicators
        self.vline = self.sc.ax_A.axvline(xmin)
        self.hline = self.sc.ax_B.axhline(xmin)

        # setup the colorbar
        self.colorbar = self.sc.figure.colorbar(self.plot, ax=self.sc.ax)

        #create toolbar, passing canvas as first parament, parent (self) as second.
        toolbar = NavigationToolbar(self.sc, self)

        #display toolbar above the plot
        L = QVBoxLayout()
        L.addWidget(toolbar)
        L.addWidget(self.sc)
        self.setLayout(L)

    def mouse_moved_on_plot(self, event):
        """Handles the event of mous moveng across the heatmap.
        
        Changes postion of markings on the subplots"""
        if event.inaxes:
            self.vline.set_xdata([event.xdata, event.xdata])
            self.hline.set_ydata([event.ydata, event.ydata])
            self.sc.figure.canvas.draw_idle()
    
    def redraw(self, data: np.array, line: np.array, line_color='blue'):
        """Redraws the plot with new data
        
            data: 2D np.array
        
            line: 1D np.array
        
            line_color: color of line plots (default blue)
        
        The arrays are expected to be of the same shape as the ones used in plot creation"""
        try:
            #test input data
            assert self._data_shape[0] == data.shape[0]
            assert self._data_shape[0] == data.shape[1]
            assert self._data_shape[0] == line.shape[0]

            #update data on heatmap
            self.plot.set_data(data)
            
            #update data on line plots
            self.lineA.set(ydata=line, color=line_color)
            self.sc.ax_A.set_ylim(line.min(), line.max())
            
            self.lineB.set(xdata=line, color=line_color)
            self.sc.ax_B.set_xlim(line.min(), line.max())
            
            #adjust colrbar
            self.colorbar.mappable.set_clim(data.min(), data.max())

            #redraw
            self.sc.figure.canvas.draw_idle()

            return 'Redraw sucessfull'
        
        except:
            
            return 'Redraw failed'

class HeatmapWithSlider(QWidget):
    """A heatmap with an interactive slider.
    
    The slider selcts a 2D slice from a 3D np.array for plotting. 
    The shape of the 3D array must be (n, n, m), so that the 2D slices will be square

        data: 3D np.array
        
        line: 2D np.array
        
        xvalues: list of values corresponding to 'x' (and 'y') axis of `data` and 'x' axis of `line`,
            if empty - counting numbers starting from 0 will be used
        
        zvalues: list of values corresponding to 'z' axis of `data` and 'y' axis of `line`,
            if empty - counting numbers starting from 0 will be used"""

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

        #preprae colormap for line plots
        self.normalize = mcolors.Normalize(vmin=zmin, vmax=zmax)
        self.colormap = cm.managua_r

        #main layout
        L0 = QVBoxLayout()
        self.setLayout(L0)

        #add the heatmap
        self.heatmap = Heatmap(
            self.data[:,:,0], 
            self.lines[:,0], 
            self.colormap(self.normalize(self.zvalues[0])), 
            xvalues=xvalues)
        L0.addWidget(self.heatmap)

        #preper slicer bar
        L1 = QHBoxLayout()
        L1.addWidget(QLabel(str(zmin)))

        #set up horizotal slicer
        slider = QSlider(orientation=Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(data.shape[2]-1)
        slider.valueChanged.connect(self.value_changed)

        L1.addWidget(slider)

        L1.addWidget(QLabel(str(zmax)))

        self.slice_label = QLabel(f'Current: {self.zvalues[0]}')
        L1.addWidget(self.slice_label)

        L0.addLayout(L1)

  
    def value_changed(self, num):
        '''Handels the event of changing the slider position'''
        print(num)
        self.heatmap.redraw(
            self.data[:,:,num], 
            self.lines[:,num], 
            self.colormap(self.normalize(self.zvalues[num]))
            )
        self.slice_label.setText(f'Current: {self.zvalues[num]}')



if __name__ == '__main__':

    from pathlib import Path
    import pandas as pd
    from lum_data import DataHolder

    app = QApplication([])

    with open(Path('/home/beekeeper/programming/lumTherm/examples/Example1.csv'), 'r') as f:
        data = pd.read_csv(
                            f, 
                            sep=',', 
                            skiprows=list(range(22)),
                            header=0,
                            index_col=0
                        )

    data.dropna(how='all', axis=1, inplace=True)

    data.columns = list(range(340, 0, -10))

    holder = DataHolder()
    holder.add_data(data)
    holder.data.sort_index(axis=1, inplace=True)
    lines = holder.data.to_numpy()
    
    ratios = holder.calculate_sensitivity()


    w = HeatmapWithSlider(ratios, lines, xvalues=holder.data.index, zvalues=holder.data.columns)
    w.show()

    app.exec()      