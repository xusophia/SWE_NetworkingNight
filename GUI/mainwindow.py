# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets

from companysetup import Ui_CompanySetupWindow
from engine import *
import sys
class Ui_MainWindow(object):

    def openCompanyWindow(self):

        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_CompanySetupWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.close()

        #MainWindow.close()
        #sys.exit(self.window.exec())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 543)
        MainWindow.setStyleSheet("\n"
"background-color: rgb(245, 224, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainBtn = QtWidgets.QPushButton(self.centralwidget)
        self.mainBtn.setGeometry(QtCore.QRect(270, 380, 261, 41))
        # button click
        self.mainBtn.clicked.connect(self.openCompanyWindow)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.mainBtn.setFont(font)
        self.mainBtn.setObjectName("mainBtn")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 10, 431, 231))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 301, 181))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../SWE_NetworkingNight2/GUI/images/SWE_Logo.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 450, 751, 71))
        font = QtGui.QFont()
        font.setFamily("Helvetica 45 Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 520, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica 45 Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 250, 371, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(40, 290, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica 45 Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(40, 330, 401, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica 45 Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Home"))
        self.mainBtn.setText(_translate("MainWindow", "Press here to continue."))
        self.label.setText(_translate("MainWindow", "Welcome to the Networking Night Assignment Program! This program is intended to assign students to 2 companies (1 for entree seating, 1 for dessert seating). This program relies on a connection to Google Sheets and will produce an Excel file of your results. "))
        self.label_3.setText(_translate("MainWindow", "This program was designed by Sophia Xu. If there are any problems or you have any questions, please let me know at sophiahxu@gmail.com.  "))
        self.label_4.setText(_translate("MainWindow", "Last Updated: 7/17/2019"))
        self.label_5.setText(_translate("MainWindow", "First, make sure you have the following:"))
        self.label_6.setText(_translate("MainWindow", "- an internet connection"))
        self.label_7.setText(_translate("MainWindow", "- Google Sheets file with all the student responses"))
