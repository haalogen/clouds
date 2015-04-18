#TODO: learn how to CONNECT widgets correctly

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Label(QLabel):
    def __init__(self, title=""):
        super(Label, self).__init__()
        
        self.title = title
        self.side = 100
        self.rect = QRect(0,0,self.side,self.side)
        
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        
    def mousePressEvent(self, event):
        print self.title + " mousePressEvent"
        print event.pos()
        
        side = self.side
        self.rubberBand.setGeometry(event.x()-side/2,
                                    event.y()-side/2,
                                    side, side )
        self.rubberBand.show();
        self.rect = (self.rubberBand.x(),
                    self.rubberBand.y(),
                    self.rubberBand.width(),
                    self.rubberBand.height() )
        print self.rect

class MyWidget(QWidget):
    def __init__(self, fname1, fname2):
        super(MyWidget, self).__init__()
        
        self.fileName1 = fname1
        self.fileName2 = fname2
        
        self.image1 = QImage(self.fileName1)
        self.image2 = QImage(self.fileName2)
        
        self.initUI()
    
    def initUI(self):
        image1 = self.image1
        image2 = self.image2
        
        lbl1 = Label("Label1")
        lbl1.setPixmap(QPixmap.fromImage(image1).scaled(lbl1.size(), Qt.KeepAspectRatio))
        lbl2 = Label("Label2")
        lbl2.setPixmap(QPixmap(image2).scaled(lbl2.size(), Qt.KeepAspectRatio))
        
        print "lbl1:", lbl1.size()
        print "lbl2:", lbl2.size()
        print "image1:", image1.size()
        print "image2:", image2.size()
        kw = 1.0*image1.width() / lbl1.width()
        kh = 1.0*image1.height() / lbl1.height()
        print "kw:", kw, "kh:", kh
        
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        
        grid1 = QGridLayout()
        grid2 = QGridLayout()
        
        lblLeft1 = QLabel("Left coord.")
        lblLeft2 = QLabel("Left coord.")
        lblTop1 = QLabel("Top coord.")
        lblTop2 = QLabel("Top coord.")
        lblSide1 = QLabel("Width=Height")
        lblSide2 = QLabel("Width=Height")
        
        leftSpinBox1 = QSpinBox()
        leftSpinBox1.setRange(0, image1.width())
        leftSpinBox2 = QSpinBox()
        leftSpinBox2.setRange(0, image2.width())

        topSpinBox1 = QSpinBox()
        topSpinBox1.setRange(0, image1.height())
        topSpinBox2 = QSpinBox()
        topSpinBox2.setRange(0, image2.height())

        sideSpinBox1 = QSpinBox()
        sideSpinBox1.setRange(0, 500)
        sideSpinBox2 = QSpinBox()
        sideSpinBox2.setRange(0, 500)
        
        pbHelp = QPushButton("Help")
        
        grid1.addWidget(lblLeft1,0,1)
        grid1.addWidget(leftSpinBox1,0,2)
        grid1.addWidget(lblTop1,0,3)
        grid1.addWidget(topSpinBox1,0,4)
        grid1.addWidget(lblSide1,0,5)
        grid1.addWidget(sideSpinBox1,0,6)
        grid1.addWidget(pbHelp,1,1)
        
        grid2.addWidget(lblLeft2,0,1)
        grid2.addWidget(leftSpinBox2,0,2)
        grid2.addWidget(lblTop2,0,3)
        grid2.addWidget(topSpinBox2,0,4)
        grid2.addWidget(lblSide2,0,5)
        grid2.addWidget(sideSpinBox2,0,6)
        
        vbox1.addWidget(lbl1)
        vbox1.addLayout(grid1)
        vbox1.addStretch(1)
        
        vbox2.addWidget(lbl2)
        vbox2.addLayout(grid2)
        vbox2.addStretch(1)
        
        hbox = QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        
        self.setLayout(hbox)
        self.showMaximized()
    
    def openImageDialog1(self, fname):
        self.fileName1 = QFileDialog.getOpenFileName(self,"Open Image #1", ".");
        print self.fileName1

    
    def openImageDialog2(self):
        self.fileName2 = QFileDialog.getOpenFileName(self, "Open Image #2", ".")
        print self.fileName2

def createParser():
    parser = argparse.ArgumentParser(
        description = """This is a program for matching the pieces of 2 pictures.""",
        epilog = "(c) Stanislav Nikitin, Apr 2015. <sv.nikitin@physics.msu.ru>"
        
    )
    
    parser.add_argument("file1", metavar="FILE1", 
    help = "image1 (left image) filename")
    parser.add_argument("file2", metavar="FILE2",
    help = "image2 (left image) filename")
    
    return parser


def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    fileName1 = namespace.file1
    fileName2 = namespace.file2
    
    app = QApplication(sys.argv)
    w = MyWidget(fileName1, fileName2)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


