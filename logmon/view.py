import sys
import os.path
import re

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAbstractItemView, QSplitter
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableView, QTextBrowser, QWidget
from PyQt5.QtWidgets import QHeaderView

import logmon.keeping as keep

_re_br = re.compile('[\r\n]')


def _br_trim(text):
    res_br = _re_br.search(text)
    if res_br:
        return text[:res_br.start()]
    return text


class TableModel(QAbstractTableModel):
    _header = ['Имя файла', 'Уровень', 'Дата', 'Текст сообщения лога']
    _color = [
        QBrush(QColor(255, 154, 255)),  # magenta
        QBrush(QColor(255, 154, 255)),  # magenta
        QBrush(QColor(255, 154, 255)),  # magenta
        QBrush(QColor(255, 154, 154)),  # red
        QBrush(QColor(255, 255, 154)),  # yellow
        QBrush(QColor(154, 255, 255)),  # blue
        QBrush(QColor(255, 255, 255)),  # white
        QBrush(QColor(154, 255, 154)),  # green
        QBrush(QColor(92, 154, 154)),   # dark blue
    ]

    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.get_data())

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._header)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.get_data()[index.row()][index.column()]
        if role == Qt.BackgroundColorRole:
            level = self.get_data()[index.row()][5]
            return QBrush(self._color[level])

        return None

    def headerData(self, p_int, orientation, role=None):
        if role != Qt.DisplayRole:
            return None
        if orientation != Qt.Horizontal:
            return None
        return self._header[p_int]

    def get_data(self):
        return self._data


class LogQMainWindow(QMainWindow):

    def __init__(self, parent=None, flags=Qt.Widget):
        super().__init__(parent, flags)
        self._table = QTableView()
        self._text = QTextBrowser()
        self.init_ui()

    def init_ui(self):

        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)

        vbox = QVBoxLayout()
        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)
        vbox.addWidget(splitter)
        splitter.addWidget(self._table)
        splitter.addWidget(self._text)

        widget = QWidget(flags=Qt.Widget)
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.setGeometry(500, 200, 1000, 700)
        # self.resize(1000, 700)
        # frame_geom = self.centralWidget().frameGeometry()
        # frame_geom.moveCenter(QDesktopWidget().availableGeometry().center())
        # self.move(frame_geom.topLeft())

    def load_data(self, log_data):
        data = []
        for path, val in log_data.items():
            log_file_name = os.path.basename(path)
            for log in val['log_list']:
                date = log.get_date().strftime('%Y.%m.%d %H:%M:%S')

                text_trim = log.get_text()[:80]
                text_trim = _br_trim(text_trim)
                if len(text_trim) < len (log.get_text()):
                    text_trim += '...'
                item = [log_file_name, log.get_level().name, date, text_trim, path, log.get_level().value, log.get_text()]
                data.append(item)

        data_sort = QSortFilterProxyModel()
        data_sort.setSourceModel(TableModel(data))
        self._table.setModel(data_sort)
        self._table.setSortingEnabled(True)

        self._table.selectionModel().selectionChanged.connect(self.table_row_select)

    def table_row_select(self, selected, deselected):

        text_list = []
        for index in self._table.selectionModel().selectedRows():
            source_index = index.model().mapToSource(index)
            source_model = index.model().sourceModel()
            row = source_model.get_data()[source_index.row()]
            text_list.append('Path: {0}\nLevel: {1}\nDate: {2}\n\n{3}'.format(row[4], row[1], row[2], row[6]))
        self._text.setPlainText('\n----------\n'.join(text_list))


def main():
    app = QApplication(sys.argv)
    w = LogQMainWindow()
    w.load_data(keep.load())
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
