from PySide2.QtWidgets import (QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
                             QGroupBox, QComboBox, QLineEdit, QFileDialog, QApplication)
from PySide2.QtCore import Qt, QTimer, QSize, QDir
from PySide2.QtGui import QPixmap, QImage, QIcon, QFont, QPalette
import sys
import os
import datetime
from picamera import PiCamera
import time

groupbox_style = 'background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #373535, stop:1 #5f5c5c);'
btn_style = 'QPushButton { background-color: none } QPushButton:pressed { background-color: #e9cd72 } QPushButton {border: 2px solid #d0d1d4} QPushButton {border-radius: 25px}'

label_font = QFont('IRANSans', 16)
class Capture(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.flag = False

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
        r_groupbox.setMaximumWidth(500)
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
        
        self.combo = QComboBox()
        self.combo.setStyleSheet('background-color: #d5d5d5; selection-background-color: #9a9a9a; font-size: 22px;')
        self.combo.setFixedSize(450, 40)
        self.combo.setLayoutDirection(Qt.RightToLeft)
        for i in range(len(items)):
            self.combo.addItem(items[i])
        self.combo.setFont(label_font)
        # self.combo.activated[str].connect(self.onChanged)
        r_vbox.addWidget(self.combo, alignment=Qt.AlignHCenter)

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText('/home/pi/Documents')
        self.lineEdit.setStyleSheet('background-color: #d5d5d5; font-size: 18px')
        self.lineEdit.setFixedSize(320, 40)
        r_hbox1.addWidget(self.lineEdit)

        self.browse_btn = QPushButton()
        self.browse_btn.setStyleSheet('background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f7f7f8, stop:1 #898c91); color: #373737; font-size: 16px; border: none')
        self.browse_btn.setFixedSize(100, 40)
        self.browse_btn.setText('Browse')
        self.browse_btn.clicked.connect(self.setFolder)
        r_hbox1.addWidget(self.browse_btn)

        r_vbox.addLayout(r_hbox1)

        self.time_tb = QLineEdit()
        self.time_tb.setPlaceholderText('4')
        self.time_tb.setStyleSheet('background-color: #d5d5d5; font-size: 18px')
        self.time_tb.setFixedSize(320, 40)
        r_hbox2.addWidget(self.time_tb)

        self.time_label = QLabel()
        self.time_label.setText('تایمر')
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet('background-color: none; color: #ffffff; font-size: 18px')
        self.time_label.setFixedSize(100, 40)
        r_hbox2.addWidget(self.time_label)

        r_vbox.addLayout(r_hbox2)

        self.take_btn = QPushButton()
        self.take_btn.setFixedSize(110, 110)
        self.take_btn.setStyleSheet(btn_style)
        self.take_btn.setIcon(QIcon('images/camera.png')) 
        self.take_btn.setIconSize(QSize(95, 95))
        self.take_btn.clicked.connect(self.onChanged)
        r_vbox.addWidget(self.take_btn, alignment=Qt.AlignCenter)

        label = QLabel(self)
        label.setStyleSheet('background-color: none')
        pixmap = QPixmap('images/farazist.png')
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.FastTransformation)
        label.setPixmap(pixmap)
        r_vbox.addWidget(label, alignment=Qt.AlignCenter|Qt.AlignBottom)

        self.camera = PiCamera()
        self.camera.start_preview(fullscreen=False, window = (100, 20, 640, 480))
        
        # self.showMaximized()
                
    def onChanged(self):
        
            directory = str(self.combo.currentIndex())
            parent_dir = "Bottles Images"   
            path = os.path.join(self.lineEdit.text(),parent_dir, directory)  
                
            try:
                os.makedirs(path)  
                print("Directory '% s' created" % directory)  
            except OSError:
                print(("Creation of the directory %s failed" % directory))

            name = str(datetime.datetime.now())
            name = name.replace(':', '-')
            name = name.replace('.', '-')
            self.camera.capture(path + '/' + name + '.jpg')
            
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
    items = getItems()
    app = QApplication(sys.argv)
    screen = Capture()
    screen.showMaximized()
    try:
        sys.exit(app.exec_())
    except SystemExit as e:
        print(e)