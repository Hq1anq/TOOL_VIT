# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerxaxrZt.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.linkInput = QPlainTextEdit(self.centralwidget)
        self.linkInput.setObjectName(u"linkInput")
        font1 = QFont()
        font1.setPointSize(15)
        self.linkInput.setFont(font1)

        self.verticalLayout.addWidget(self.linkInput)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_2.addWidget(self.label_2)

        self.contentInput = QPlainTextEdit(self.centralwidget)
        self.contentInput.setObjectName(u"contentInput")
        self.contentInput.setFont(font1)

        self.verticalLayout_2.addWidget(self.contentInput)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.btn_ok = QPushButton(self.centralwidget)
        self.btn_ok.setObjectName(u"btn_ok")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_ok.sizePolicy().hasHeightForWidth())
        self.btn_ok.setSizePolicy(sizePolicy)
        self.btn_ok.setMinimumSize(QSize(0, 70))

        self.verticalLayout_3.addWidget(self.btn_ok, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Nh\u1eadp link facebook", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Nh\u1eadp ho\u1ea1t \u0111\u1ed9ng c\u1ea7n g\u1eedi", None))
        self.btn_ok.setText(QCoreApplication.translate("MainWindow", u"OK", None))
    # retranslateUi

