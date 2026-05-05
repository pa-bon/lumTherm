# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ColdStar_buttons.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import sys
import os
import originpro as op
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import ColdStar_0 as cs

def number_box(val=0, min=0, max=1000, step=1):
    box = QtWidgets.QDoubleSpinBox()
    box.setMinimum(min)
    box.setMaximum(max)
    box.setSingleStep(step)
    box.setValue(val)
    return box
proceed = False

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.do = False
        self.the_end = False
        self.inp_path = ''
        self.out_path = ''
        while True:
            self.openFileNameDialog()
            if not self.inp_path == '':
                if not (self.inp_path.split('.')[-1] == 'csv' or self.inp_path.split('.')[-1] == 'CSV'):
                    message = QtWidgets.QMessageBox(self)
                    message.setText('\n\tPlease select .CSV file\t\n')
                    message.exec()
                else:
                    self.do = True
                    break
            else:
                self.the_end = True
                break
        if self.do:
            try:
                self.comment, self.values = cs.data_from_csv(self.inp_path)
                self.initUI()
            except:
                widget = QtWidgets.QLabel('\n  The file could not be read.  \n\n  Close the program and start again.  \n')
                self.setCentralWidget(widget)
                self.show()
        if self.the_end:
            widget = QtWidgets.QLabel('\n  You have not chosen any file.  \n\n  Close the program and start again.  \n')
            self.setCentralWidget(widget)
            self.show()

    def initUI(self):
        self.scan_min = self.values[0][0]
        self.scan_max = self.values[0][-1]
        self.scan_step = self.values[0][1] | self.values[0][0]
        self.temps = cs.read_temps(self.comment)
        self.t_max = max(self.temps)
        self.t_min = min(self.temps)
        self.t_step = self.temps[1] | self.temps[0]
        self.smth_order = 2
        self.smth_window = 11
        self.bcg_method = 'None'
        self.therm_method = 'Point'
        self.bcg_x1 = self.scan_min
        self.bcg_x2 = self.scan_max
        self.r_sta1 = self.scan_min
        self.r_stp1 = self.values[0][round(len(self.values[0]) + 2)]
        self.r_sta2 = self.values[0][round(len(self.values[0]) + 2)]
        self.r_stp2 = self.scan_max
        self.smth_bcg_prop = 'bcg none'
        self.smooth_values = cs.smooth(self.values, self.smth_window, self.smth_order)
        self.no_bcg = self.smooth_values
        self.bcg_name = 'SG: 2, 11\tNo bcg'
        self.wls = []
        self.uncs = cs.uncertainty(cs.get_noise(self.values, self.smooth_values), self.smth_window)
        self.ratios = []
        self.ratio_uncs = []
        self.ratio_name = ''
        self.saved_ratios = {'Current\n': []}
        self.r_max = max([max(column) for column in self.no_bcg[1:]])
        self.r_min = min([min(column) for column in self.no_bcg[1:]])
        supreme = QtWidgets.QHBoxLayout()
        main_layout = QtWidgets.QGridLayout()
        sc1 = MplCanvas(self, width=5, height=4, dpi=100)
        for column in self.values[1:]:
            sc1.axes.plot(self.values[0], column)
        sc1.axes.set_title('Original Data')
        self.sc2 = MplCanvas(self, width=5, height=4, dpi=100)
        for column in self.smooth_values[1:]:
            self.sc2.axes.plot(self.smooth_values[0], column)
        self.sc2.axes.set_title('Smoothed data')
        self.sc3 = MplCanvas(self, width=5, height=4, dpi=100)
        for column in self.no_bcg[1:]:
            self.sc3.axes.plot(self.no_bcg[0], column)
        self.sc3.axes.plot([self.r_sta1, self.r_sta1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
        self.sc3.axes.plot([self.r_stp1, self.r_stp1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
        self.sc3.axes.plot([self.r_sta2, self.r_sta2], [self.r_min, self.r_max], color='red', linestyle='dashed')
        self.sc3.axes.plot([self.r_stp2, self.r_stp2], [self.r_min, self.r_max], color='red', linestyle='dashed')
        self.sc3.axes.set_title('Background subtracted')
        self.sc4 = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc4twin = self.sc4.axes.twinx()
        toolbar1 = NavigationToolbar(sc1, self)
        toolbar2 = NavigationToolbar(self.sc2, self)
        toolbar3 = NavigationToolbar(self.sc3, self)
        toolbar4 = NavigationToolbar(self.sc4, self)
        layout1 = QtWidgets.QVBoxLayout()
        layout1.addWidget(toolbar1)
        layout1.addWidget(sc1)
        layout2 = QtWidgets.QVBoxLayout()
        layout2.addWidget(toolbar2)
        layout2.addWidget(self.sc2)
        layout3 = QtWidgets.QVBoxLayout()
        layout3.addWidget(toolbar3)
        layout3.addWidget(self.sc3)
        layout4 = QtWidgets.QVBoxLayout()
        layout4.addWidget(toolbar4)
        layout4.addWidget(self.sc4)
        main_layout.addLayout(layout1, 0, 0)
        main_layout.addLayout(layout2, 0, 1)
        main_layout.addLayout(layout3, 1, 0)
        main_layout.addLayout(layout4, 1, 1)
        buttons = QtWidgets.QVBoxLayout()
        proprietes_box = QtWidgets.QGroupBox()
        proprietes = QtWidgets.QVBoxLayout()
        pass
        file_name = self.inp_path.split('/')[-1]
        proprietes.addWidget(QtWidgets.QLabel(f'{file_name}'))
        proprietes.addWidget(QtWidgets.QLabel(f'Scan: {self.scan_min} nm to {self.scan_max} nm\nStep: {self.scan_step} nm'))
        proprietes.addWidget(QtWidgets.QLabel(f'Temperatures: {self.t_min} K to {self.t_max} K\nStep: {self.t_step} K'))
        proprietes_box.setLayout(proprietes)
        buttons.addWidget(proprietes_box)
        smooth_box = QtWidgets.QGroupBox()
        smooth_box.setTitle('Smooth')
        smooth = QtWidgets.QVBoxLayout()
        smooth_1 = QtWidgets.QHBoxLayout()
        smooth_1.addWidget(QtWidgets.QLabel('Order'))
        order_box = number_box(2, 0, 6, 1)
        order_box.valueChanged.connect(self.smth_order_ch)
        smooth_1.addWidget(order_box)
        smooth_1.addWidget(QtWidgets.QLabel('Window'))
        window_box = number_box(11, 3, 101, 2)
        window_box.valueChanged.connect(self.smth_window_ch)
        smooth_1.addWidget(window_box)
        smooth.addLayout(smooth_1)
        smooth_box.setLayout(smooth)
        buttons.addWidget(smooth_box)
        background_box = QtWidgets.QGroupBox()
        background_box.setTitle('Background')
        background = QtWidgets.QVBoxLayout()
        background_1 = QtWidgets.QHBoxLayout()
        background_1.addWidget(QtWidgets.QLabel('Method'))
        bcg_methods = QtWidgets.QComboBox()
        bcg_methods.addItems(['None', 'Point', 'Line'])
        bcg_methods.currentTextChanged.connect(self.bcg_method_ch)
        background_1.addWidget(bcg_methods)
        background.addLayout(background_1)
        background_2 = QtWidgets.QHBoxLayout()
        self.bcg_lable = QtWidgets.QLabel(' ')
        background_2.addWidget(self.bcg_lable)
        self.bcg_x1_box = number_box(self.scan_min, self.scan_min, self.scan_max)
        self.bcg_x1_box.valueChanged.connect(self.bcg_x1_ch)
        background_2.addWidget(self.bcg_x1_box)
        self.bcg_x1_box.setDisabled(True)
        self.bcg_x2_box = number_box(self.scan_max, self.scan_min, self.scan_max)
        self.bcg_x2_box.valueChanged.connect(self.bcg_x2_ch)
        background_2.addWidget(self.bcg_x2_box)
        self.bcg_x2_box.setDisabled(True)
        background.addLayout(background_2)
        background_box.setLayout(background)
        buttons.addWidget(background_box)
        thermometry_box = QtWidgets.QGroupBox()
        thermometry_box.setTitle('Thermometry')
        thermometry = QtWidgets.QVBoxLayout()
        thermometry_0 = QtWidgets.QHBoxLayout()
        thermometry_0.addWidget(QtWidgets.QLabel('Method:'))
        therm_methods = QtWidgets.QComboBox()
        therm_methods.addItems(['Point', 'Integral', 'Maximum'])
        therm_methods.currentTextChanged.connect(self.therm_method_ch)
        thermometry_0.addWidget(therm_methods)
        thermometry.addLayout(thermometry_0)
        thermometry_1 = QtWidgets.QGridLayout()
        thermometry_1.addWidget(QtWidgets.QLabel('Start 1'), 0, 0)
        sta1_box = number_box(self.scan_min, self.scan_min, self.scan_max)
        sta1_box.valueChanged.connect(self.r_sta1_ch)
        thermometry_1.addWidget(sta1_box, 0, 1)
        thermometry_1.addWidget(QtWidgets.QLabel('Stop 1'), 1, 0)
        stp1_box = number_box(self.values[0][round(len(self.values[0]) + 2)], self.scan_min, self.scan_max)
        stp1_box.valueChanged.connect(self.r_stp1_ch)
        thermometry_1.addWidget(stp1_box, 1, 1)
        thermometry_1.addWidget(QtWidgets.QLabel('Start 2'), 0, 2)
        self.sta2_box = number_box(self.values[0][round(len(self.values[0]) + 2)], self.scan_min, self.scan_max)
        self.sta2_box.valueChanged.connect(self.r_sta2_ch)
        thermometry_1.addWidget(self.sta2_box, 0, 3)
        thermometry_1.addWidget(QtWidgets.QLabel('Stop 2'), 1, 2)
        self.stp2_box = number_box(self.scan_max, self.scan_min, self.scan_max)
        self.stp2_box.valueChanged.connect(self.r_stp2_ch)
        thermometry_1.addWidget(self.stp2_box, 1, 3)
        thermometry.addLayout(thermometry_1)
        self.therm_list = QtWidgets.QListWidget()
        self.therm_list.addItems(self.saved_ratios)
        self.therm_list.itemDoubleClicked.connect(self.therm_list_d_clicked)
        self.therm_list.itemClicked.connect(self.therm_list_clicked)
        thermometry.addWidget(self.therm_list)
        thermometry_box.setLayout(thermometry)
        buttons.addWidget(thermometry_box)
        recalculate = QtWidgets.QPushButton('Recalculate')
        recalculate.clicked.connect(self.recalculating)
        buttons.addWidget(recalculate)
        self.save_ratios = QtWidgets.QPushButton('Save Ratios')
        self.save_ratios.clicked.connect(self.saving_ratios)
        buttons.addWidget(self.save_ratios)
        self.save_ratios.setDisabled(True)
        save = QtWidgets.QPushButton('Export')
        save.clicked.connect(self.saving)
        buttons.addWidget(save)
        supreme.addLayout(main_layout, 5)
        supreme.addLayout(buttons, 1)
        widget = QtWidgets.QWidget()
        widget.setLayout(supreme)
        self.setCentralWidget(widget)
        self.show()

    def smth_window_ch(self, window):
        self.smth_window = int(window)
        self.save_ratios.setDisabled(True)

    def smth_order_ch(self, order):
        self.smth_order = int(order)
        self.save_ratios.setDisabled(True)

    def r_sta1_ch(self, sta1):
        self.r_sta1 = sta1
        self.sc3.axes.cla()
        for column in self.no_bcg[1:]:
            self.sc3.axes.plot(self.no_bcg[0], column)
        self.sc3.axes.plot([self.r_sta1, self.r_sta1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
        self.sc3.axes.plot([self.r_stp1, self.r_stp1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
        if not self.therm_method == 'Maximum':
            self.sc3.axes.plot([self.r_sta2, self.r_sta2], [self.r_min, self.r_max], color='red', linestyle='dashed')
            self.sc3.axes.plot([self.r_stp2, self.r_stp2], [self.r_min, self.r_max], color='red', linestyle='dashed')
        self.sc3.axes.set_title('Background subtracted')
        self.sc3.draw()

    def r_stp1_ch(self, stp1):
        self.r_stp1 = stp1
        self.sc3.axes.cla()
        for column in self.no_bcg[1:]:
            self.sc3.axes.plot(self.no_bcg[0], column)
        self.sc3.axes.plot([self.r_sta1, self.r_sta1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
        self.sc3.axes.plot([self.r_stp1, self.r_stp1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
        if not self.therm_method == 'Maximum':
            self.sc3.axes.plot([self.r_sta2, self.r_sta2], [self.r_min, self.r_max], color='red', linestyle='dashed')
            self.sc3.axes.plot([self.r_stp2, self.r_stp2], [self.r_min, self.r_max], color='red', linestyle='dashed')
        self.sc3.axes.set_title('Background subtracted')
        self.sc3.draw()

    def r_sta2_ch(self, sta2):
        self.r_sta2 = sta2
        self.sc3.axes.cla()
        for column in self.no_bcg[1:]:
            self.sc3.axes.plot(self.no_bcg[0], column)
        self.sc3.axes.plot([self.r_sta1, self.r_sta1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
        self.sc3.axes.plot([self.r_stp1, self.r_stp1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
        self.sc3.axes.plot([self.r_sta2, self.r_sta2], [self.r_min, self.r_max], color='red', linestyle='dashed')
        self.sc3.axes.plot([self.r_stp2, self.r_stp2], [self.r_min, self.r_max], color='red', linestyle='dashed')
        self.sc3.axes.set_title('Background subtracted')
        self.sc3.draw()

    def r_stp2_ch(self, stp2):
        self.r_stp2 = stp2
        self.sc3.axes.cla()
        for column in self.no_bcg[1:]:
            self.sc3.axes.plot(self.no_bcg[0], column)
        self.sc3.axes.plot([self.r_sta1, self.r_sta1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
        self.sc3.axes.plot([self.r_stp1, self.r_stp1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
        self.sc3.axes.plot([self.r_sta2, self.r_sta2], [self.r_min, self.r_max], color='red', linestyle='dashed')
        self.sc3.axes.plot([self.r_stp2, self.r_stp2], [self.r_min, self.r_max], color='red', linestyle='dashed')
        self.sc3.axes.set_title('Background subtracted')
        self.sc3.draw()

    def bcg_method_ch(self, method):
        self.bcg_method = method
        if method == 'Point':
            self.bcg_x1_box.setEnabled(True)
            self.bcg_x2_box.setDisabled(True)
            self.bcg_lable.setText('Equal in:')
        elif method == 'Line':
            self.bcg_x1_box.setEnabled(True)
            self.bcg_x2_box.setEnabled(True)
            self.bcg_lable.setText('Zero in:')
        else:
            self.bcg_x1_box.setDisabled(True)
            self.bcg_x2_box.setDisabled(True)
            self.bcg_lable.setText('None')
        self.save_ratios.setDisabled(True)

    def bcg_x1_ch(self, x1):
        self.bcg_x1 = x1
        self.save_ratios.setDisabled(True)

    def bcg_x2_ch(self, x2):
        self.bcg_x2 = x2
        self.save_ratios.setDisabled(True)

    def therm_method_ch(self, method):
        self.therm_method = method
        if method == 'Maximum':
            self.sta2_box.setDisabled(True)
            self.stp2_box.setDisabled(True)
            self.sc3.axes.cla()
            for column in self.no_bcg[1:]:
                self.sc3.axes.plot(self.no_bcg[0], column)
            self.sc3.axes.plot([self.r_sta1, self.r_sta1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
            self.sc3.axes.plot([self.r_stp1, self.r_stp1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
            self.sc3.axes.set_title('Background subtracted')
            self.sc3.draw()
        else:
            self.sta2_box.setEnabled(True)
            self.stp2_box.setEnabled(True)
            self.sc3.axes.cla()
            for column in self.no_bcg[1:]:
                self.sc3.axes.plot(self.no_bcg[0], column)
            self.sc3.axes.plot([self.r_sta1, self.r_sta1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
            self.sc3.axes.plot([self.r_stp1, self.r_stp1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
            self.sc3.axes.plot([self.r_sta2, self.r_sta2], [self.r_min, self.r_max], color='red', linestyle='dashed')
            self.sc3.axes.plot([self.r_stp2, self.r_stp2], [self.r_min, self.r_max], color='red', linestyle='dashed')
            self.sc3.axes.set_title('Background subtracted')
            self.sc3.draw()

    def therm_list_clicked(self, item):
        data = self.saved_ratios[item.text()]
        self.sc4.axes.cla()
        self.sc4twin.cla()
        self.sc4.axes.scatter(self.temps, data[1])
        self.sc4.axes.set_title(data[0])
        self.sc4.axes.plot(data[2][0], data[2][1])
        self.sc4.axes.legend(['Ratio'])
        self.sc4twin.plot(data[2][0], data[2][2], color='orange')
        self.sc4twin.legend(['Sr'])
        self.sc4.draw()

    def therm_list_d_clicked(self, item):
        if not item.text() == 'Current\n':
            del self.saved_ratios[item.text()]
            self.therm_list.clear()
            self.therm_list.addItems(self.saved_ratios)

    def recalculating(self):
        try:
            self.smooth_values = cs.smooth(self.values, self.smth_window, self.smth_order)
        except TypeError:
            message = QtWidgets.QMessageBox(self)
            message.setText('Window must be an odd number\ngreater then order by at lest 2')
            message.exec()
            return False
        self.uncs = cs.uncertainty(cs.get_noise(self.values, self.smooth_values), self.smth_window)
        if self.bcg_method == 'Point':
            self.no_bcg = cs.remove_bcg_point(self.smooth_values, self.bcg_x1)
            self.bcg_name = f'SG: {self.smth_order}, {self.smth_window}    Point bcg: {self.bcg_x1}'
        elif self.bcg_method == 'Line':
            self.no_bcg = cs.remove_bcg_line(self.smooth_values, self.bcg_x1, self.bcg_x2)
            self.bcg_name = f'SG: {self.smth_order}, {self.smth_window}    Line bcg: {self.bcg_x1}, {self.bcg_x2}'
        else:
            self.no_bcg = self.smooth_values
            self.bcg_name = f'SG: {self.smth_order}, {self.smth_window}    No bcg'
        self.r_max = max([max(column) for column in self.no_bcg[1:]])
        self.r_min = min([min(column) for column in self.no_bcg[1:]])
        self.sc2.axes.cla()
        for column in self.smooth_values[1:]:
            self.sc2.axes.plot(self.smooth_values[0], column)
        self.sc2.axes.set_title('Smoothed data')
        self.sc2.draw()
        if self.therm_method == 'Point':
            self.wls = cs.search_for_wl(self.no_bcg, self.r_sta1, self.r_stp1, self.r_sta2, self.r_stp2)
            if self.r_sta1 >= self.r_stp1 or self.r_sta2 >= self.r_stp2:
                self.wls = [(1, 1, 1)]
                message = QtWidgets.QMessageBox(self)
                message.setText("'Stop' must be after 'Start'")
                message.exec()
                return False
            self.ratios, self.ratio_uncs = cs.get_ratios(self.smooth_values, self.uncs, self.wls[0][1], self.wls[0][2])
            self.ratio_name = f'P {self.values[0][self.wls[0][1]]}/{self.values[0][self.wls[0][2]]} nm'
            self.sc3.axes.cla()
            for column in self.no_bcg[1:]:
                self.sc3.axes.plot(self.no_bcg[0], column)
            self.sc3.axes.plot([self.r_sta1, self.r_sta1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
            self.sc3.axes.plot([self.r_stp1, self.r_stp1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
            self.sc3.axes.plot([self.values[0][self.wls[0][1]], self.values[0][self.wls[0][1]]], [self.r_min, self.r_max], color='blue')
            self.sc3.axes.plot([self.r_sta2, self.r_sta2], [self.r_min, self.r_max], color='red', linestyle='dashed')
            self.sc3.axes.plot([self.r_stp2, self.r_stp2], [self.r_min, self.r_max], color='red', linestyle='dashed')
            self.sc3.axes.plot([self.values[0][self.wls[0][2]], self.values[0][self.wls[0][2]]], [self.r_min, self.r_max], color='red')
            self.sc3.axes.set_title('Background subtracted')
            self.sc3.draw()
            self.sc4.axes.cla()
            self.sc4twin.cla()
            self.sc4.axes.scatter(self.temps, self.ratios)
            self.sc4.axes.set_title(f'Thermometry: {self.values[0][self.wls[0][1]]} nm to {self.values[0][self.wls[0][2]]} nm')
            self.sr = cs.estimate_sr(self.temps, self.ratios)
            self.sc4.axes.plot(self.sr[0], self.sr[1])
            self.sc4.axes.legend(['Ratio'])
            self.sc4twin.plot(self.sr[0], self.sr[2], color='orange')
            self.sc4twin.legend(['Sr'])
            self.sc4.draw()
        if self.therm_method == 'Integral':
            if self.r_sta1 >= self.r_stp1 or self.r_sta2 >= self.r_stp2:
                self.wls = [(1, 1, 1)]
                message = QtWidgets.QMessageBox(self)
                message.setText("'Stop' must be after 'Start'")
                message.exec()
                return False
            self.ratios, self.ratio_uncs = cs.get_ratios_integral(self.smooth_values, self.uncs, self.r_sta1, self.r_stp1, self.r_sta2, self.r_stp2, self.scan_step)
            self.ratio_name = f'I {self.r_sta1}-{self.r_stp1}/{self.r_sta2}-{self.r_stp2} nm'
            self.sc3.axes.cla()
            for column in self.no_bcg[1:]:
                self.sc3.axes.plot(self.no_bcg[0], column)
            self.sc3.axes.plot([self.r_sta1, self.r_sta1], [self.r_min, self.r_max], color='blue')
            self.sc3.axes.plot([self.r_stp1, self.r_stp1], [self.r_min, self.r_max], color='blue')
            self.sc3.axes.plot([self.r_sta2, self.r_sta2], [self.r_min, self.r_max], color='red')
            self.sc3.axes.plot([self.r_stp2, self.r_stp2], [self.r_min, self.r_max], color='red')
            self.sc3.axes.set_title('Background subtracted')
            self.sc3.draw()
            self.sc4.axes.cla()
            self.sc4twin.cla()
            self.sc4.axes.scatter(self.temps, self.ratios)
            self.sc4.axes.set_title(f'Thermometry: {self.r_sta1}-{self.r_stp1} nm to {self.r_sta2}-{self.r_stp2} nm')
            self.sr = cs.estimate_sr(self.temps, self.ratios)
            self.sc4.axes.plot(self.sr[0], self.sr[1])
            self.sc4.axes.legend(['Ratio'])
            self.sc4twin.plot(self.sr[0], self.sr[2], color='orange')
            self.sc4twin.legend(['Sr'])
            self.sc4.draw()
        if self.therm_method == 'Maximum':
            if self.r_sta1 >= self.r_stp1:
                self.wls = [(1, 1, 1)]
                message = QtWidgets.QMessageBox(self)
                message.setText("'Stop' must be after 'Start'")
                message.exec()
                return False
            self.ratios, self.ratio_uncs = cs.get_ratios_max(self.smooth_values, self.r_sta1, self.r_stp1, self.scan_step)
            self.ratio_name = f'M {self.ratios[0]}-{self.ratios[-1]} nm'
            self.sc3.axes.cla()
            for column in self.no_bcg[1:]:
                self.sc3.axes.plot(self.no_bcg[0], column)
            self.sc3.axes.plot([self.r_sta1, self.r_sta1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
            self.sc3.axes.plot([self.r_stp1, self.r_stp1], [self.r_min, self.r_max], color='blue', linestyle='dashed')
            self.sc3.axes.set_title('Background subtracted')
            self.sc3.draw()
            self.sc4.axes.cla()
            self.sc4twin.cla()
            self.sc4.axes.scatter(self.temps, self.ratios)
            self.sc4.axes.set_title(f'Thermometry: maximum {self.ratios[0]} nm to {self.ratios[-1]} nm')
            self.sr = cs.estimate_sr(self.temps, self.ratios)
            self.sc4.axes.plot(self.sr[0], self.sr[1])
            self.sc4.axes.legend(['Ratio'])
            self.sc4twin.plot(self.sr[0], self.sr[2], color='orange')
            self.sc4twin.legend(['Sr'])
            self.sc4.draw()
        self.saved_ratios['Current\n'] = [self.ratio_name, self.ratios, self.sr, self.ratio_uncs]
        self.save_ratios.setEnabled(True)

    def saving_ratios(self):
        self.therm_list.addItem(self.bcg_name + f'\n{self.ratio_name}\nSr = {max(self.sr[2])}\n ')
        self.saved_ratios[self.bcg_name + f'\n' + self.ratio_name + f'\nSr = {max(self.sr[2])}\n '] = self.saved_ratios['Current\n']

    def saving(self):

        def origin_shutdown_exception_hook(exctype, value, traceback):
            """Ensures Origin gets shut down if an uncaught exception"""
            op.exit()
            sys.__excepthook__(exctype, value, traceback)
        if op and op.oext:
            sys.excepthook = origin_shutdown_exception_hook
        if self.out_path == '':
            self.saveFileDialog()
            op.new()
            op.save(self.out_path)
        cs.save_to_op(self.values, self.smooth_values, self.no_bcg, self.comment, self.out_path, self.bcg_name)
        for key in self.saved_ratios:
            if not key == 'Current\n':
                item = self.saved_ratios[key]
                cs.save_ratios(item[1], item[3], self.temps, self.out_path, ' - '.join(key.split('\n')))
        if op.oext:
            op.exit()

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options = options + QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '', 'All Files (*);;CSV Files (*.csv)', options=options)
        self.inp_path = fileName

    def saveFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options = options + QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'QFileDialog.getSaveFileName()', '', 'All Files (*);;Origin Files (*.opju)', options=options)
        filePath = fileName.replace('/', '\\')
        if not filePath.split('.')[-1] == 'opju':
            filePath = filePath + '.opju'
        self.out_path = filePath
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()