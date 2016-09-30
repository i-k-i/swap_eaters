import sys
import os
import signal
import time
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTableWidget, QApplication, QTableWidgetItem, QMenu, qApp, QPushButton
from PyQt4 import QtGui
from collector import find_eaters

#TODO: updating table data
#TODO: set layout https://habrahabr.ru/post/31687/

class Table(QTableWidget):
    def __init__(self, data_source):
        self.data_source = data_source
        self.get_data(self.data_source)
        QTableWidget.__init__(self, self.amount_rows, self.amount_columns)
        self.fill()
        # self.horizontalHeader().setStretchLastSection(True)

    def fill(self):
        self.setSortingEnabled(False)
        self.setmydata()
        self.setSortingEnabled(True) # Only after filling the table
        self.sortByColumn(2)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def get_data(self, data_source):
        self.data = data_source()
        self.amount_rows = len(self.data)
        self.amount_columns = len(self.data.items()[0][1].keys())

    def get_pid(self):
        col_ind = self.currentItem().column()
        row_ind = self.currentItem().row()
        pid = int(self.item(row_ind, 0).text())
        return pid

    def setmydata(self):
        horHeaders = []
        for n, proc_inf in enumerate(self.data.values()):
            for m, k in enumerate(proc_inf.keys()):
                horHeaders.append(k)
                # newitem = QTableWidgetItem(proc_inf[k])
                newitem = QTableWidgetItem()
                newitem.setData(Qt.EditRole, proc_inf[k])
                self.setItem(n, m, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

    def update(self):
        self.clear()
        self.get_data(self.data_source)
        self.fill()


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Swap eaters')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #GUIelems
        self.table = Table(find_eaters)
        self.reload_button = QPushButton('Update', self)
        self.debug_button = QPushButton('Debug', self)
        self.reload_button.clicked.connect(self.table.update)
        self.debug_button.clicked.connect(self.debug_trace)
        #
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(5)
        self.grid.addWidget(self.debug_button, 0, 0)
        self.grid.addWidget(self.reload_button, 1, 0)
        self.grid.addWidget(self.table, 0, 1, 5,5)
        self.setLayout(self.grid)
        self.resize(440, 650)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        terminator = menu.addAction("-------")
        dbg = menu.addAction("Debugger")
        quitAction = menu.addAction("Quit")
        kill_process = menu.addAction("Kill")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            qApp.quit()
        elif action == kill_process:
            self.kill_glutton()
        elif action == dbg:
            self.debug_trace()

    def kill_glutton(self):
        pid = self.table.get_pid()
        def process_exists(pid):
            pids = [int(p) for p in os.listdir('/proc') if p.isdigit()]
            if pid in pids:
                return True
            else:
                return False
        if process_exists(pid):
            os.kill(pid, signal.SIGTERM)
            # time.sleep(5)
            # if process_exists(pid):
            #     os.kill(pid, signal.SIGKILL)
        self.table.update()

    def debug_trace(self):
        '''Set a tracepoint in the Python debugger that works with Qt'''
        from PyQt4.QtCore import pyqtRemoveInputHook
        # Or for Qt5
        #from PyQt5.QtCore import pyqtRemoveInputHook
        import ipdb
        pyqtRemoveInputHook()
        ipdb.set_trace()

def main():
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # data = find_eaters
    main()
