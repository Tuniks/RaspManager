import sys
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QDirIterator, QDir, QFileInfo, QUrl
from PyQt5.QtWidgets import QMessageBox, QInputDialog


class Ui(QtWidgets.QMainWindow):
    currentDir = QDir.home()
    connected = False

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../src/mainwindow.ui', self)

        self.stackedWidget.setCurrentIndex(0)
        self.Log.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

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
        items = self.Log.selectedItems()
        for item in items:
            confirmation = QMessageBox.question(self, "RASP", "Are you sure you want to delete " + item.text(), QMessageBox.Yes | QMessageBox.No)

            if confirmation == QMessageBox.Yes:
                dirtodelete = QDir(item.text())
                dirtodelete.removeRecursively()
                self.on_execute_clicked()

    def create_item(self):
        dirname, ok = QInputDialog.getText(self, "RASP", "Directory Name:")
        if ok and dirname:
            if self.currentDir.mkdir(dirname):
                QMessageBox.information(self, "RASP", "Directory successfully created.")
                self.on_execute_clicked()
            else:
                QMessageBox.information(self, "RASP", "Directory could not be created.")

    def on_item_double_clicked(self, item):
        iteminfo = QFileInfo(item.text())

        if iteminfo.isDir():
            self.currentDir.cd(item.text())
            self.on_execute_clicked()
            self.Path.setText(self.currentDir.absolutePath())
        else:
            QtGui.QDesktopServices.openUrl(QUrl.fromLocalFile(item.text()))

    def on_workspace_item_double_clicked(self, item):

        if item.text() == "Local":
            self.stackedWidget.setCurrentIndex(0)
        elif item.text() == "Server" and self.connected:
            self.stackedWidget.setCurrentIndex(1)
        elif item.text() == "Server" and not self.connected:
            self.stackedWidget.setCurrentIndex(2)

    def on_connect_clicked(self):
        url = self.serverInput.text()
        user = self.userInput.text()
        pwd = self.passInput.text()

        print(user+":"+pwd+"@"+url)

        self.connected = True
        self.stackedWidget.setCurrentIndex(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    sys.exit(app.exec_())
