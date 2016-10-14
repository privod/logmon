import sys
import os.path
from datetime import datetime
import re

from PyQt5.QtCore import Qt, QAbstractTableModel
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
    _header = ['Имя файла', 'Дата', 'Текст сообщения лога']

    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.get_data())

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._header)

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self.get_data()[index.row()][index.column()]
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
        self._log_data = None
        self._table = QTableView()
        self._text = QTextBrowser()
        self.init_ui()

    def init_ui(self):

        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._table.clicked.connect(self.table_row_select)

        vbox = QVBoxLayout()
        vbox.addWidget(self._table)
        vbox.addWidget(self._text)

        widget = QWidget(flags=Qt.Widget)
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.setGeometry(500, 200, 1000, 700)
        # self.resize(1000, 700)
        # frame_geom = self.centralWidget().frameGeometry()
        # frame_geom.moveCenter(QDesktopWidget().availableGeometry().center())
        # self.move(frame_geom.topLeft())

    def load_data(self, log_data):
        self._log_data = log_data
        data = []
        for path, val in self._log_data.items():
            log_file_name = os.path.basename(path)
            for log in val['log_list']:
                date = datetime.strftime(log.get_date(), '%Y.%m.%d %H:%M:%S')

                text_trim = log.get_text()[:100]
                text_trim = _br_trim(text_trim)
                if len(text_trim) < len (log.get_text()):
                    text_trim += '...'
                item = [log_file_name, date, text_trim, path, log.get_text()]
                data.append(item)
        self._table.setModel(TableModel(data))

    def table_row_select(self, index):
        data = index.model().get_data()
        self._text.setPlainText(data[index.row()][4])


def main():
    app = QApplication(sys.argv)
    w = LogQMainWindow()
    w.load_data(keep.load())
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
