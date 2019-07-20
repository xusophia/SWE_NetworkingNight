from PyQt5 import QtCore, QtGui, QtWidgets



if __name__ == '__main__':
        import sys
        app = QtWidgets.QApplication(sys.argv) # can also pass empty list []
        MainWindow = QtWidgets.QMainWindow()
        from mainwindow import Ui_MainWindow
        ui = Ui_MainWindow() # create an instance of ui main window
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
