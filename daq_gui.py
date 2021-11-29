# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'DAQ_logger.ui'
# Created by: PyQt5 UI code generator 5.9.2

import os
import glob
from datetime import datetime
import pandas as pd
from serial.tools import list_ports
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFileDialog

from data_logger import *

#-------------------------------
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(700, 650)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(700, 0))
        MainWindow.setMaximumSize(QtCore.QSize(700, 650))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("daq_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.edt_db_path = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.edt_db_path.setFont(font)
        self.edt_db_path.setObjectName("edt_db_path")
        self.gridLayout.addWidget(self.edt_db_path, 0, 1, 1, 4)
        self.btn_browse = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_browse.setFont(font)
        self.btn_browse.setAutoDefault(False)
        self.btn_browse.setDefault(False)
        self.btn_browse.setFlat(False)
        self.btn_browse.setObjectName("btn_browse")
        self.gridLayout.addWidget(self.btn_browse, 0, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.edt_main_dir = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.edt_main_dir.setFont(font)
        self.edt_main_dir.setAlignment(QtCore.Qt.AlignCenter)
        self.edt_main_dir.setObjectName("edt_main_dir")
        self.gridLayout.addWidget(self.edt_main_dir, 1, 1, 1, 1)
        self.edt_patient = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.edt_patient.setFont(font)
        self.edt_patient.setAlignment(QtCore.Qt.AlignCenter)
        self.edt_patient.setObjectName("edt_patient")
        self.gridLayout.addWidget(self.edt_patient, 1, 2, 1, 1)
        self.edt_date = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.edt_date.setFont(font)
        self.edt_date.setAlignment(QtCore.Qt.AlignCenter)
        self.edt_date.setObjectName("edt_date")
        self.gridLayout.addWidget(self.edt_date, 1, 3, 1, 1)
        self.ext_record_num = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ext_record_num.setFont(font)
        self.ext_record_num.setAlignment(QtCore.Qt.AlignCenter)
        self.ext_record_num.setObjectName("ext_record_num")
        self.gridLayout.addWidget(self.ext_record_num, 1, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.combo_exp = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.combo_exp.setFont(font)
        self.combo_exp.setObjectName("combo_exp")        
        for cur_prot in os.listdir('exp_protocols'):
            if cur_prot.endswith('.csv'):
                prot = (cur_prot.split('/')[-1])[:-4]
                self.combo_exp.addItem(prot) 
        self.gridLayout.addWidget(self.combo_exp, 2, 1, 1, 4)
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_start.setFont(font)
        self.btn_start.setObjectName("btn_start")
        self.gridLayout.addWidget(self.btn_start, 2, 5, 1, 1)
        self.motion_pic = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.motion_pic.sizePolicy().hasHeightForWidth())
        self.motion_pic.setSizePolicy(sizePolicy)
        self.motion_pic.setMaximumSize(QtCore.QSize(600, 380))
        self.motion_pic.setText("")
        # self.motion_pic.setPixmap(QtGui.QPixmap("pics/2.jpg"))
        self.motion_pic.setScaledContents(True)
        self.motion_pic.setAlignment(QtCore.Qt.AlignCenter)
        self.motion_pic.setObjectName("motion_pic")
        self.gridLayout.addWidget(self.motion_pic, 3, 0, 1, 6)
        # self.gridLayout.addWidget(self.motion_pic, 3, 0, 1, 6, alignment=QtCore.Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.btn_browse.clicked.connect(self.open_browse)
        self.btn_start.clicked.connect(self.start_collecting) 

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DAQ logger"))
        self.label.setText(_translate("MainWindow", " DataBase Path: "))
        self.edt_db_path.setText(_translate("MainWindow", "C:/Recordings/"))
        self.btn_browse.setText(_translate("MainWindow", "Browse"))
        self.label_2.setText(_translate("MainWindow", " Recording Folder:"))
        self.edt_main_dir.setText(_translate("MainWindow", "BL-001"))
        self.edt_patient.setText(_translate("MainWindow", "000"))
        self.edt_date.setText(_translate("MainWindow", '000000'))
        self.ext_record_num.setText(_translate("MainWindow", "1"))
        self.label_3.setText(_translate("MainWindow", " Recording Protocol:"))
        # self.combo_exp.setItemText(0, _translate("MainWindow", "Exp#1"))
        # self.combo_exp.setItemText(1, _translate("MainWindow", "Exp#2"))
        # self.combo_exp.setItemText(2, _translate("MainWindow", "Exp#3"))
        self.btn_start.setText(_translate("MainWindow", "Start"))

    def open_browse(self):
        path_db = QFileDialog.getExistingDirectory(caption="Choose Directory", directory="C:/")
        if path_db != ('',''):
            self.edt_db_path.setText(path_db)
        self.edt_date.setText(datetime.today().strftime('%y%m%d'))

        path_new = self.edt_db_path.text() +'/'+ self.edt_main_dir.text()
        if not os.path.exists(path_new):
            os.makedirs(path_new)

    def start_collecting(self):
        self.edt_date.setText(datetime.today().strftime('%y%m%d'))
        self.ext_record_num.setText(datetime.today().strftime('%H%M%S'))
        main_dir = self.edt_db_path.text() +'\\'+ self.edt_main_dir.text()
        patient_dir = main_dir +'\\'+ self.edt_main_dir.text() +'_'+ self.edt_patient.text() +'_'+ self.edt_date.text()
        if not os.path.exists(patient_dir):
            os.makedirs(patient_dir)
        file_name = datetime.today().strftime('%y%m%d')+'_'+datetime.today().strftime('%H%M%S')
        file_name_opt = file_name +'_OPT.csv'
        file_name_imu = file_name +'_IMU.csv'
        self.path_opt = patient_dir+'\\'+file_name_opt
        self.path_imu = patient_dir+'\\'+ file_name_imu
        print(self.path_opt,'\n', self.path_imu)
        collect_data(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# python daq_gui.py
