#source: https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])


#testing
if __name__ == '__main__':
    import pandas as pd

    class MainWindow(QtWidgets.QMainWindow):

        def __init__(self):
            super().__init__()

            self.table = QtWidgets.QTableView()

            data = pd.DataFrame([
              [1, 9, 2],
              [1, 0, -1],
              [3, 5, 2],
              [3, 3, 2],
              [5, 8, 9],
            ], columns=['A', 'B', 'C'], index=['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5'])

            self.model = TableModel(data)
            self.table.setModel(self.model)

            self.setCentralWidget(self.table)


    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()