# encoding: utf-8
"""
@version: 1.0
@author: Jarrrett
@file: app_run.py
@time: 2020/3/27 16:41
"""
import sys
import os
from purecode import GetPureCode
import shutil

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAction, QFileDialog
from PyQt5 import QtGui

from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("init/window.ui", self)
        self.setFixedSize(self.width(), self.height());
        self.setWindowIcon(QIcon('init/cloud.ico'))
        self.setWindowTitle('纯净的代码_JIARUI')

        self.setWindowFlags(Qt.WindowStaysOnTopHint) #强制置顶


        self.pushButton.setEnabled(False)
        self.pushButton_4.setEnabled(False)

        self.statusbar.showMessage('初始化成功')

        self.pushButton_2.clicked.connect(self.getCANdata)
        #self.pushButton.clicked.connect(self.freshDBCfile)
        self.pushButton_3.clicked.connect(self.Dataparse)
        #self.pushButton_4.clicked.connect(self.initDBCfile)


    def getCANdata(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./","All Files (*);Text Files (*.js);")  # 设置文件扩展名过滤,注意用双分号间隔
        if fileName1:
            print(fileName1)
            self.lineEdit.setText(fileName1)
            self.CAN_data_file = fileName1
            file_path_list = fileName1.split('/')[0:-1] #获取文件路径
            self.filename = fileName1.split('/')[-1]
            self.file_path = '/'.join(file_path_list)
            self.pushButton_3.setEnabled(True)
            self.statusbar.showMessage(f'加载{self.filename}文件成功！')
            return fileName1
        else:
            pass



    def freshDBCfile(self):
        if self.dbc_exist_flag == 1:
            self.initDBCfile()
        fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./","Text Files (*.csv);;All Files (*)")  # 设置文件扩展名过滤,注意用双分号间隔
        oldname = fileName1
        fresh_dbc_file_name = fileName1.split('/')[-1]
        shutil.copyfile(oldname, self.new_dbc_file_name)
        self.dbc_exist_flag = 1; #如果文件夹里存在新dbc则，将dbc的标志置为1
        self.pushButton_4.setEnabled(True)
        self.statusbar.showMessage(f'更新{fresh_dbc_file_name}文件成功！')

    def initDBCfile(self):
        """
        重置dbc文件，删除new文件夹的dbc文件。
        :return:
        """
        if self.dbc_exist_flag == 1:
            os.remove(self.new_dbc_file_name)
            self.pushButton_4.setEnabled(False)
            self.statusbar.showMessage('重置文件成功！')
        else:
            self.pushButton_4.setEnabled(True)
            pass

    def dbc_flag(self):
        """
        监测是否有新的dbc文件
        :return:
        """
        if (os.path.exists(self.new_dbc_file_name)):
            return 1
        else:
            self.pushButton_4.setEnabled(False)
            return 0


    def Dataparse(self):
        get_pure_code = GetPureCode(self.CAN_data_file)
        kk = get_pure_code.delete_code()
        zz = get_pure_code.save_to_path()
        file_window = (self.file_path).replace('/', '\\')
        if zz == 1:
            os.system("start explorer "+file_window)
            self.pushButton_3.setEnabled(True)
            self.statusbar.showMessage(f'{self.filename}文件解析完成！')
            self.lineEdit.setText(' ')
        else:
            self.lineEdit.setText(' ')
            self.statusbar.showMessage(f'{self.filename}文件解析失败，请重新提交！')



#编写一个公共类CommomHelper,用于帮助解读qss文件
class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r',encoding = 'utf-8') as f:
            return f.read()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    styleFile = 'init/style.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    window.setStyleSheet(qssStyle)

    window.show()
    sys.exit(app.exec_())