# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'siparisler.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Omega(object):
    def setupUi(self, Omega):
        Omega.setObjectName("Omega")
        Omega.resize(800, 600)
        Omega.setAcceptDrops(False)
        Omega.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(Omega)
        self.centralwidget.setObjectName("centralwidget")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setToolTip("")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setRowCount(30)
        self.tableWidget.setColumnCount(50)
        self.tableWidget.setObjectName("tableWidget")
        self.verticalLayout.addWidget(self.tableWidget)
        
        self.newButton = QtWidgets.QPushButton(self.centralwidget)
        self.newButton.setObjectName("newButton")
        self.newButton.setText("Yeni Buton")
        self.verticalLayout.addWidget(self.newButton)

        Omega.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Omega)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Omega.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Omega)
        self.statusbar.setObjectName("statusbar")
        Omega.setStatusBar(self.statusbar)
        self.retranslateUi(Omega)
        QtCore.QMetaObject.connectSlotsByName(Omega)

    def retranslateUi(self, Omega):
        _translate = QtCore.QCoreApplication.translate
        Omega.setWindowTitle(_translate("Omega", "Omega"))
        self.pushButton.setText(_translate("Omega", "Dosya Ekle"))

        # Yeni butonun metnini çevir
        self.newButton.setText(_translate("Omega", "Yeni Buton"))

        self.pushButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.tableWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
