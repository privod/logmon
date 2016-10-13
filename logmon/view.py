import sys
import os.path
from datetime import datetime
import re

from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableView, QTextBrowser, QWidget
from PyQt5.QtWidgets import QHeaderView

import logmon.keeping as keep
# from .log import Log

_re_br = re.compile('[\r\n]')

def _br_trim(text):
    res_br = _re_br.search(text)
    if res_br:
        return text[:res_br.start()]
    return text

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return 3                                                # TODO Нужно определять динамически

    def data(self, index, role=None):
        if (role == Qt.DisplayRole):
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, p_int, orientation, role=None):
        if (role != Qt.DisplayRole):
            return None
        if (orientation != Qt.Horizontal):
            return None

        header = ['Имя файла', 'Дата', 'Текст сообщения лога']
        return header[p_int]


class LogQMainWindow(QMainWindow):

    def __init__(self, parent=None, flags=Qt.Widget):
        super().__init__(parent, flags)
        self._log_data = None
        self._table = QTableView()
        self._text = QTextBrowser()
        self.init_ui()


    def init_ui(self):

        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._text.setText('Test')

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

                text = log.get_text()[:100]
                text = _br_trim(text)
                if len(text) < len (log.get_text()):
                    text += '...'
                item = [log_file_name, date, text]
                data.append(item)
        self._table.setModel(TableModel(data))


def main():
    app = QApplication(sys.argv)
    w = LogQMainWindow()
    w.load_data(keep.load())
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
