from PySide2.QtWidgets import (QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
                             QGroupBox, QComboBox, QLineEdit, QFileDialog, QApplication)
from PySide2.QtCore import Qt, QTimer, QSize, QDir
from PySide2.QtGui import QPixmap, QImage, QIcon, QFont, QPalette
import sys
import os
import datetime
from picamera import PiCamera
import time
import threading

groupbox_style = 'background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #373535, stop:1 #5f5c5c);'
btn_style = 'background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f7f7f8, stop:1 #898c91); color: #373737; border: none;font: 16pt "IRANSans";'
teke_btn_style = 'QPushButton { background-color: #28a745;color: rgb(255, 255, 255);font: 20pt "IRANSans";padding: 3px; border: none; outline-style: none; } QPushButton:pressed { background-color: #145222; border-style: inset;}'
endTeke_btn_style = 'QPushButton { background-color: #ff0022;color: rgb(255, 255, 255);font: 20pt "IRANSans";padding: 3px; border: none; outline-style: none; } QPushButton:pressed { background-color: #800011; border-style: inset;}'

label_font = QFont('IRANSans', 16)
class Capture(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.flagT1 = True
        self.flagT2 = True

        self.setWindowTitle("farazist picture")
        self.setStyleSheet('background-color: #898989')
        
        # ------------ main ------------
        layout = QHBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)

        # ------------ left widgets ------------
        l_groupbox = QGroupBox()
        l_groupbox.setStyleSheet(groupbox_style)
        layout.addWidget(l_groupbox)

        l_vbox = QVBoxLayout()
        l_groupbox.setLayout(l_vbox)

        self.image_label = QLabel()
        l_vbox.addWidget(self.image_label, alignment=Qt.AlignCenter)


        # ------------ right widgets -----------
        r_groupbox = QGroupBox()
        r_groupbox.setMaximumWidth(400)
        r_groupbox.setStyleSheet(groupbox_style)
        layout.addWidget(r_groupbox)
        
        r_vbox = QVBoxLayout()
        r_vbox.setSpacing(30)
        r_vbox.setContentsMargins(0, 20, 0, 5)
        r_groupbox.setLayout(r_vbox)

        r_hbox1 = QHBoxLayout()
        r_hbox1.setSpacing(5)

        r_hbox2 = QHBoxLayout()
        r_hbox2.setSpacing(5)

        r_hbox3 = QHBoxLayout()
        r_hbox3.setSpacing(5)
        
        self.combo = QComboBox()
        self.combo.setStyleSheet('background-color: #d5d5d5; selection-background-color: #9a9a9a; font: 20pt "IRANSans";')
        self.combo.setFixedSize(350, 40)
        self.combo.setLayoutDirection(Qt.RightToLeft)
        for i in range(len(items)):
            self.combo.addItem(items[i])
        self.combo.setFont(label_font)
        # self.combo.activated[str].connect(self.startTakeImg)
        r_vbox.addWidget(self.combo, alignment=Qt.AlignHCenter)

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText('/home/pi/Documents')
        self.lineEdit.setStyleSheet('background-color: #d5d5d5; font-size: 18px')
        self.lineEdit.setFixedSize(220, 40)
        r_hbox1.addWidget(self.lineEdit)

        self.browse_btn = QPushButton()
        self.browse_btn.setStyleSheet(btn_style)
        self.browse_btn.setFixedSize(100, 40)
        self.browse_btn.setText('Browse')
        self.browse_btn.clicked.connect(self.setFolder)
        r_hbox1.addWidget(self.browse_btn)

        r_vbox.addLayout(r_hbox1)

        self.time_tb = QLineEdit()
        self.time_tb.setPlaceholderText('4')
        self.time_tb.setStyleSheet('background-color: #d5d5d5; font-size: 18px')
        self.time_tb.setFixedSize(220, 40)
        r_hbox2.addWidget(self.time_tb)

        self.time_label = QLabel()
        self.time_label.setText('timer (second)')
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet('background-color: none; color: #ffffff; font-size: 18px')
        self.time_label.setFixedSize(120, 40)
        r_hbox2.addWidget(self.time_label)

        r_vbox.addLayout(r_hbox2)

        self.take_btn = QPushButton()
        self.take_btn.setText('Start')
        self.take_btn.setMaximumSize(172, 40)
        self.take_btn.setStyleSheet(teke_btn_style)
        self.take_btn.clicked.connect(self.startTakeImg)
        r_hbox3.addWidget(self.take_btn)

        self.endTake_btn = QPushButton()
        self.endTake_btn.setText('End')
        self.endTake_btn.setMaximumSize(172, 40)
        self.endTake_btn.setStyleSheet(endTeke_btn_style)
        self.endTake_btn.clicked.connect(self.stopTakeImg)
        r_hbox3.addWidget(self.endTake_btn)

        r_vbox.addLayout(r_hbox3)

        label = QLabel(self)
        label.setStyleSheet('background-color: none')
        pixmap = QPixmap('images/farazist.png')
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.FastTransformation)
        label.setPixmap(pixmap)
        r_vbox.addWidget(label, alignment=Qt.AlignCenter|Qt.AlignBottom)

        self.camera = PiCamera()
        self.camera.start_preview(fullscreen=False, window = (50, 100, 640, 480))
        
        # self.showMaximized()
                
    def startTakeImg(self):
            directory = str(self.combo.currentIndex())
            parent_dir = "Bottles Images"   
            path = os.path.join(self.lineEdit.text(),parent_dir, directory)  
                
            try:
                os.makedirs(path)  
                print("Directory '% s' created" % directory)  
            except OSError:
                print(("Creation of the directory %s failed" % directory))

            self.name = str(datetime.datetime.now())
            self.name = self.name.replace(':', '-')
            self.name = self.name.replace('.', '-')

            if self.time_tb.text() == '':
                self.flagT1 = False
                self.t1 = threading.Timer(10.0, self.startTakeImg)
                self.t1.start()
            if self.time_tb.text() != '':
                self.flagT2 = False
                self.t2 = threading.Timer(int(self.time_tb.text()), self.startTakeImg)
                self.t2.start()
            try:
                self.camera.capture(path + '/' + self.name + '.jpg')
            except Exception as e:
                print('error: ', e)


    def stopTakeImg(self):
        if self.flagT1 == False:
            self.t1.cancel()
            self.flagT1 = True
        elif self.flagT2 == False:
            self.t2.cancel()
            self.flagT2 = True


    def setFolder(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly 
        folder  = QFileDialog.getExistingDirectory(self, 
                            "Open Folder",
                            self.lineEdit.text(),
                            options=options)
        self.lineEdit.setText(folder)
        
def getItems():
    items = []
    f = open("items.txt", "r")
    for line in f:
        items.append(line[:-1])
    return items


if __name__ == '__main__':
    os.environ["QT_QPA_FB_FORCE_FULLSCREEN"] = "0"
    os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
    os.environ["QT_QPA_FONTDIR"] = "fonts"
    items = getItems()
    app = QApplication(sys.argv)
    screen = Capture()
    screen.showMaximized()
    try:
        sys.exit(app.exec_())
    except SystemExit as e:
        print('error: ', e)