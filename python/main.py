import sys
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QDirIterator, QDir


class Ui(QtWidgets.QMainWindow):
    currentDir = QDir.home()

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../src/mainwindow.ui', self)

        self.stackedWidget.setCurrentIndex(0)
        self.Log.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.Log.setContextMenuPolicy(Qt.CustomContextMenu)

        self.Path.setText(self.currentDir.absolutePath())
        self.on_execute_clicked()
        self.show()


# SLOTS
    def on_execute_clicked(self):
        self.Log.clear()
        it = QDirIterator(self.currentDir, QDirIterator.NoIteratorFlags)
        while it.hasNext():
            self.Log.addItem(it.next())

    def on_path_change(self):
        self.currentDir.cd(self.Path.text())
        self.on_execute_clicked()

    def on_back_clicked(self):
        self.currentDir.cdUp()
        self.on_execute_clicked()
        self.Path.setText(self.currentDir.absolutePath())

    def show_context_menu(self, click):
        globalpos = self.Log.mapToGlobal(click)
        menu = QtWidgets.QMenu()
        menu.addAction("Delete", lambda: self.erase_item())
        menu.addAction("Create", lambda: self.create_item())
        menu.exec(globalpos)

    def erase_item(self):
        print("Deeting")

    def create_item(self):
        print("Creating")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    sys.exit(app.exec_())
