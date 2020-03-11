from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
                             QGroupBox, QComboBox, QLineEdit, QFileDialog, QApplication)
from PyQt5.QtCore import Qt, QTimer, QSize, QDir
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont, QPalette
import sys
import os
import cv2 as cv
import datetime
from DataBase import Database

def getCategories():
    global gategories_name

    gategories_number = len(items)
    print(gategories_number)
    gategories_name = []
    for i in range(gategories_number):
        gategories_name.append(items[i]['name'])
    return gategories_name

groupbox_style = 'background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #373535, stop:1 #5f5c5c);'
btn_style = 'QPushButton { background-color: none } QPushButton:pressed { background-color: #e9cd72 } QPushButton {border: 2px solid #d0d1d4} QPushButton {border-radius: 25px}'

label_font = QFont('IRANSans', 16)
class Capture(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.flag = False
        bottle_list = getCategories()

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

        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)

        # ------------ right widgets -----------
        r_groupbox = QGroupBox()
        r_groupbox.setMaximumWidth(500)
        r_groupbox.setStyleSheet(groupbox_style)
        layout.addWidget(r_groupbox)
        
        r_vbox = QVBoxLayout()
        r_vbox.setSpacing(30)
        r_vbox.setContentsMargins(0, 20, 0, 5)
        r_groupbox.setLayout(r_vbox)

        r_hbox = QHBoxLayout()
        r_hbox.setSpacing(5)
        
        self.combo = QComboBox()
        self.combo.setStyleSheet('background-color: #d5d5d5; selection-background-color: #9a9a9a; font-size: 22px;')
        self.combo.setFixedSize(450, 40)
        self.combo.setLayoutDirection(Qt.RightToLeft)
        for i in range(len(bottle_list)):
            self.combo.addItem(bottle_list[i])
        self.combo.setFont(label_font)
        # self.combo.activated[str].connect(self.onChanged)
        r_vbox.addWidget(self.combo, alignment=Qt.AlignHCenter)

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText('D:/Farazist project/bottles')
        self.lineEdit.setStyleSheet('background-color: #d5d5d5; font-size: 18px')
        self.lineEdit.setFixedSize(320, 40)
        r_hbox.addWidget(self.lineEdit)

        self.browse_btn = QPushButton()
        self.browse_btn.setStyleSheet('background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f7f7f8, stop:1 #898c91); color: #373737; font-size: 16px; border: none')
        self.browse_btn.setFixedSize(100, 40)
        self.browse_btn.setText('Browse')
        self.browse_btn.clicked.connect(self.setFolder)
        r_hbox.addWidget(self.browse_btn)

        r_vbox.addLayout(r_hbox)

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
        label.setPixmap(pixmap)
        r_vbox.addWidget(label, alignment=Qt.AlignCenter|Qt.AlignBottom)

        self.controlTimer()
        # self.showMaximized()
                
    def onChanged(self):
        if not self.flag:
            print('camera is off')

        else:
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
            cv.imwrite(path + '/' + name + '.jpg', cv.cvtColor(self.image, cv.COLOR_RGB2BGR))
            
    def viewCam(self):
        try:
            ret, self.image = self.cap.read()
            self.image = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
            self.image = cv.flip(self.image, 1)

            # get image infos
            height, width, channel = self.image.shape
            step = channel * width

            # create QImage from image
            qImg = QImage(self.image.data, width, height, step, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(qImg))
        except:
            self.image_label.setText('Error')
            self.image_label.setStyleSheet('color: #ffffff; font-size: 40px; background-color: none;')

    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            self.flag = True
            try:
                self.cap = cv.VideoCapture(1)
                self.timer.start(2)
            except:
                print('Error')

    def setFolder(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly 
        folder  = QFileDialog.getExistingDirectory(self, 
                            "Open Folder",
                            self.lineEdit.text(),
                            options=options)
        self.lineEdit.setText(folder)

if __name__ == '__main__':
    items = Database.getItems()
    getCategories()
    app = QApplication(sys.argv)
    screen = Capture()
    screen.showMaximized()
    sys.exit(app.exec_())