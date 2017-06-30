import sys
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QDirIterator, QDir, QFileInfo, QUrl
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from FtpClass import FtpConnection


class Ui(QtWidgets.QMainWindow):
    currentDir = QDir.home()
    connected = False

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../src/mainwindow.ui', self)

        self.stackedWidget.setCurrentIndex(0)
        self.Log.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.ftp = FtpConnection()

        self.Path.setText(self.currentDir.absolutePath())
        self.passInput.setText("lookatme")
        self.userInput.setText("meeseeks")
        self.serverInput.setText("vbustamante.xyz")
        self.on_execute_clicked()
        self.show()


# SLOTS
    def on_execute_clicked(self):
        self.Log.clear()
        it = QDirIterator(self.currentDir, QDirIterator.NoIteratorFlags)
        while it.hasNext():
            self.Log.addItem(it.next())
        self.Path.setText(self.currentDir.absolutePath())

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
        menu.addAction("Upload", lambda: self.upload_item())
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
            self.load_remote_log()
            self.stackedWidget.setCurrentIndex(1)
        elif item.text() == "Server" and not self.connected:
            self.stackedWidget.setCurrentIndex(2)

    def on_connect_clicked(self):
        url = self.serverInput.text()
        user = self.userInput.text()
        pwd = self.passInput.text()

        try:
            self.ftp.connect(url)
            self.ftp.login(user, pwd)
        except:
            QMessageBox.information(self, "RASP", "Error connecting to server.")
            self.stackedWidget.setCurrentIndex(0)
            return

        self.connected = True
        self.stackedWidget.setCurrentIndex(1)
        self.load_remote_log()

    def on_disconnect_clicked(self):
        self.ftp.close()
        self.connected = False
        self.stackedWidget.setCurrentIndex(2)

    def load_remote_log(self):
        self.Path_2.setText(self.ftp.pwd())
        self.Log_2.clear()
        self.ftp.ls()
        for item in self.ftp.objList:
            self.Log_2.addItem(item['name'])

    def on_remote_back_double_clicked(self):
        self.ftp.cd("..")
        self.load_remote_log()

    def on_remote_item_double_clicked(self, item):
        self.ftp.cd(item.text())
        self.load_remote_log()

    def show_remote_context_menu(self, click):
        globalpos = self.Log.mapToGlobal(click)
        menu = QtWidgets.QMenu()
        menu.addAction("Delete", lambda: self.erase_remote_item())
        menu.addAction("Create", lambda: self.create_remote_item())
        menu.addAction("Download", lambda: self.download_remote_item())
        menu.exec(globalpos)

    def erase_remote_item(self):
        items = self.Log.selectedItems()
        for item in items:
            self.ftp.exclude(item.getText())

        return

    def create_remote_item(self):
        return
        #CREATE DIRECTORY

    def download_remote_item(self):
        return
        #DOWNLOAD FILE

    def upload_item(self):
        itemNames = []
        if not self.connected:
            QMessageBox.information(self, "RASP", "Connect to server before uploading.")
            return

        items = self.Log.selectedItems()
        for item in items:
            itemNames.append(item.text())
        if len(itemNames) == 1:
            for item in items:
                self.ftp.upload(item.getText())
        else:
            self.ftp.uploadPool(itemNames)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    sys.exit(app.exec_())
