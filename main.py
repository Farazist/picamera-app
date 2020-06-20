from PySide2.QtWidgets import (QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
                             QGroupBox, QComboBox, QLineEdit, QFileDialog, QApplication,
                             QSpinBox, QLCDNumber)
from PySide2.QtCore import Qt, QTimer, QSize, QDir, Signal, QThread
from PySide2.QtGui import QPixmap, QImage, QIcon, QFont, QPalette
import sys
import os
import datetime
from picamera import PiCamera
import threading

from widgets_style import *


class Capture(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.flagT1 = True

        self.setWindowTitle("farazist picture")
        self.setStyleSheet(WINDOW_STYLE)
        self.geometry = QApplication.desktop().availableGeometry(self)
        self.setMaximumSize(self.geometry.width()*0.8, self.geometry.height()*0.7)
        
        # ------------ main ------------
        layout = QHBoxLayout()
        layout.setSpacing(10)
        self.setLayout(layout)

        # ------------ right widgets -----------
        groupbox = QGroupBox()
        groupbox.setMaximumWidth(350)
        groupbox.setStyleSheet(GROUPBOX_STYLE)
        layout.addWidget(groupbox, alignment=Qt.AlignRight)
        
        groupBox_layout = QVBoxLayout()
        groupBox_layout.setSpacing(10)
        groupBox_layout.setContentsMargins(5, 0, 5, 30)
        groupbox.setLayout(groupBox_layout)

        groupBox_hLayout1 = QHBoxLayout()
        groupBox_hLayout1.setSpacing(5)

        groupBox_hLayout2 = QHBoxLayout()
        groupBox_hLayout2.setSpacing(5)

        groupBox_hLayout3 = QHBoxLayout()
        groupBox_hLayout3.setSpacing(5)

        lbl_path = QLabel()
        lbl_path.setText('Path')
        lbl_path.setAlignment(Qt.AlignCenter)
        lbl_path.setStyleSheet(TITLE_STYLE)
        groupBox_layout.addWidget(lbl_path, alignment=Qt.AlignLeft)

        self.tb_path = QLineEdit()
        self.tb_path.setPlaceholderText('/home/pi/Documents')
        self.tb_path.setStyleSheet(LINEEDIT_STYLE)
        self.tb_path.setMaximumHeight(50)
        groupBox_hLayout1.addWidget(self.tb_path)

        self.browse_btn = QPushButton()
        self.browse_btn.setStyleSheet(BTN_BROWSE_STYLE)
        self.browse_btn.setIcon(QIcon('images/browse.png')) 
        self.browse_btn.setIconSize(QSize(45, 45))
        self.browse_btn.clicked.connect(self.setFolder)
        self.browse_btn.setMaximumHeight(50)
        groupBox_hLayout1.addWidget(self.browse_btn)

        groupBox_layout.addLayout(groupBox_hLayout1)

        lbl_item = QLabel()
        lbl_item.setText('Item')
        lbl_item.setAlignment(Qt.AlignCenter)
        lbl_item.setStyleSheet(TITLE_STYLE)
        groupBox_layout.addWidget(lbl_item, alignment=Qt.AlignLeft)

        self.combo = QComboBox()
        self.combo.setStyleSheet(COMBOBOS_STYLE)
        self.combo.setLayoutDirection(Qt.RightToLeft)
        for i in range(len(items)):
            self.combo.addItem(items[i])
        self.combo.setMaximumHeight(50)
        groupBox_layout.addWidget(self.combo)

        self.btn_camera = QPushButton()
        self.btn_camera.setStyleSheet(BTN_CAMERA_STYLE)
        self.btn_camera.setIcon(QIcon('images/camera.png')) 
        self.btn_camera.setIconSize(QSize(60, 60))
        self.btn_camera.clicked.connect(self.onChanged)
        groupBox_layout.addWidget(self.btn_camera, alignment=Qt.AlignHCenter)

        lbl_timer = QLabel()
        lbl_timer.setText('Timer')
        lbl_timer.setAlignment(Qt.AlignCenter)
        lbl_timer.setStyleSheet(TITLE_STYLE)
        groupBox_layout.addWidget(lbl_timer, alignment=Qt.AlignLeft)

        self.time_spinbox = QSpinBox(self)
        self.time_spinbox.setValue(5)
        self.time_spinbox.setMinimum(2)
        self.time_spinbox.setMaximum(60)
        self.time_spinbox.setStyleSheet(SPINBOX_STYLE)
        self.time_spinbox.setMaximumHeight(50)
        groupBox_hLayout2.addWidget(self.time_spinbox)

        self.btn_start = QPushButton()
        self.btn_start.setStyleSheet(BTN_START_STYLE)
        self.btn_start.clicked.connect(self.startTakeImg)
        self.btn_start.setIcon(QIcon('images/start.png')) 
        self.btn_start.setIconSize(QSize(50, 50))
        self.btn_start.setMaximumHeight(50)
        groupBox_hLayout2.addWidget(self.btn_start)
        
        self.btn_pause = QPushButton()
        self.btn_pause.setStyleSheet(BTN_PAUSE_STYLE)
        self.btn_pause.clicked.connect(self.stopTakeImg)
        self.btn_pause.setIcon(QIcon('images/stop.png')) 
        self.btn_pause.setIconSize(QSize(50, 50))
        self.btn_pause.setMaximumHeight(50)
        groupBox_hLayout2.addWidget(self.btn_pause)

        groupBox_layout.addLayout(groupBox_hLayout2)

        self.lcd_timer = QLCDNumber()
        self.lcd_timer.display(None)
        self.lcd_timer.setDigitCount(2)
        self.lcd_timer.setMinimumSize(50, 50)
        self.lcd_timer.setStyleSheet(LCDNUMBER_STYLE)
        groupBox_layout.addWidget(self.lcd_timer,alignment=Qt.AlignCenter)

        self.time_left_int = self.time_spinbox.value()
        self.camera = PiCamera()
        self.camera.start_preview(fullscreen=False, window = (20, 0, self.geometry.width()-410, self.geometry.height()))

    def fileName(self):
        self.name = str(datetime.datetime.now())
        self.name = self.name.replace(':', '-')
        self.name = self.name.replace('.', '-')

    def onChanged(self):
        directory = str(self.combo.currentIndex())
        parent_dir = "Bottles Images"   
        self.path = os.path.join(self.tb_path.text(),parent_dir, directory)  
            
        try:
            os.makedirs(self.path)  
            print("Directory '% s' created" % directory)  
        except OSError:
            print(("Creation of the directory %s failed" % directory))

        self.fileName()

        try:
            self.camera.capture(self.path + '/' + self.name + '.jpg')
        except Exception as e:
            print('error: ', e)
                
    def startTakeImg(self):
            directory = str(self.combo.currentIndex())
            parent_dir = "Bottles Images"   
            self.path = os.path.join(self.tb_path.text(),parent_dir, directory)  
             
            try:
                os.makedirs(self.path)  
                print("Directory '% s' created" % directory)  
            except OSError:
                print(("Creation of the directory %s failed" % directory))

            self.time_left_int = self.time_spinbox.value()
            self.my_qtimer = QTimer(self)
            self.my_qtimer.timeout.connect(self.timerTimeout)
            self.my_qtimer.start(1000)

            self.updateGUI()
    
    def timerTimeout(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            self.time_left_int = self.time_spinbox.value()
            try:
                self.camera.capture(self.path + '/' + self.name + '.jpg')
            except Exception as e:
                print('error: ', e)

        self.fileName()
        self.updateGUI()

    def updateGUI(self):
           self.lcd_timer.display("%6.2f" % (self.time_left_int / 100))
    
    def stopTakeImg(self):
            self.my_qtimer.stop()
            self.lcd_timer.display(None)

    def setFolder(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly 
        folder  = QFileDialog.getExistingDirectory(self, 
                            "Open Folder",
                            self.tb_path.text(),
                            options=options)
        self.tb_path.setText(folder)
        
def getItems():
    items = []
    f = open("items.txt", "r")
    for line in f:
        items.append(line[:-1])
    return items


if __name__ == '__main__':
    os.environ["QT_QPA_FB_FORCE_FULLSCREEN"] = "0"
    # os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
    os.environ["QT_QPA_FONTDIR"] = "fonts"
    items = getItems()
    app = QApplication(sys.argv)
    screen = Capture()
    screen.show()
    try:
        sys.exit(app.exec_())
        screen.camera.start_preview()
        print('stop preview')
        screen.camera.close()
    except SystemExit as e:
        print('error: ', e)