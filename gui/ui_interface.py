# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfacemTuXsa.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QCursor, QFont, QIcon
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFrame, QGridLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
                               QStackedWidget, QVBoxLayout, QWidget)

from gui.highlight_widget import HighlightPlainTextEdit, HighlightLabel
import resources.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setToolTipDuration(1)
        self.centralwidget.setStyleSheet(u"#centralwidget { background-color: #2C313A }\n"
"#contentTop { background-color: rgb(33, 37, 43) }\n"
"#bottomBar QPushButton {\n"
"	font-size: 11px; color: rgb(113, 126, 149);\n"
"	border: none;\n"
"	padding: 0 5px}\n"
"*{ border: none }\n"
"#send, #tag { background-color: rgb(40, 44, 52) }\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\" }\n"
"QLabel, QPushButton, QPlainTextEdit, QLineEdit, QComboBox, QCheckBox, QToolTip {\n"
"	font-size: 20px }\n"
"QToolTip { 	color: rgb(221, 221, 221) }\n"
"QPushButton {font-weight: bold}\n"
"QComboBox{\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px }\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88) }\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-ri"
                        "ght-radius: 3px;\n"
"	border-bottom-right-radius: 3px;\n"
"	background-image: url(:/icons/icons/arrowDown.svg);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54) }\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60) }\n"
"QCheckBox::indicator:hover { border: 3px solid rgb(58, 66, 81) }\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);\n"
"	background-image: url(:/icons/icons/check.svg) }\n"
"QScrollBar:horizontal {\n"
"	border: none;\n"
"	background: rgb(52, 59, 72);\n"
"	height: 8px;\n"
"	margin: 0px 21px 0 21px;\n"
"	border-radius: 0px }\n"
"QScrollBar::handle:horizontal {\n"
"	background: rgb(189, 147, 249);\n"
"	min-width: 25px"
                        ";\n"
"	border-radius: 4px }\n"
"QScrollBar::handle:horizontal:hover, QScrollBar::handle:vertical:hover {\n"
"	background: rgb(208, 181, 249) }\n"
"QScrollBar::handle:horizontal:pressed, QScrollBar::handle:vertical:pressed {\n"
"	background: rgb(161, 103, 249) }\n"
"QScrollBar::add-line:horizontal {\n"
"	border: none;\n"
"	background: rgb(55, 63, 77);\n"
"	width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"	border-bottom-right-radius: 4px;\n"
"	subcontrol-position: right;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::sub-line:horizontal {\n"
"	border: none;\n"
"	background: rgb(55, 63, 77);\n"
"	width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"	border-bottom-left-radius: 4px;\n"
"	subcontrol-position: left;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal,\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vert"
                        "ical {\n"
"	background: none }\n"
"QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px }\n"
"QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"	min-height: 25px;\n"
"	border-radius: 4px }\n"
"QScrollBar::add-line:vertical {\n"
"	border: none;\n"
"	background: rgb(55, 63, 77);\n"
"	height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"	border-bottom-right-radius: 4px;\n"
"	subcontrol-position: bottom;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"	background: rgb(55, 63, 77);\n"
"	height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"	border-top-right-radius: 4px;\n"
"	subcontrol-position: top;\n"
"	subcontrol-origin: margin }\n"
"QScrollBar::add-line:horizontal:hover, QScrollBar::sub-line:horizontal:hover,\n"
"QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {\n"
"	background: rgb(64, 69, 77) }\n"
"QScrollBar::add-line:ho"
                        "rizontal:pressed, QScrollBar::sub-line:horizontal:pressed,\n"
"QScrollBar::add-line:vertical:pressed, QScrollBar::sub-line:vertical:pressed {\n"
"	background: rgb(189, 147, 249) }\n"
"QPushButton {\n"
"	border: 3px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	padding: 10px }\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 3px solid rgb(61, 70, 86) }\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 3px solid rgb(43, 50, 61) }\n"
"QLabel { qproperty-alignment: AlignCenter }\n"
"QPlainTextEdit, QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 3px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198) }\n"
"QPlainTextEdit:hover, QLineEdit:hover { border: 2px solid rgb(64, 71, 88) }\n"
"QPlainTextEdit:focus, QLineEdit:focus { border: 2px solid rgb(91, 101, 124) }\n"
"QMenu {\n"
"	bac"
                        "kground-color: rgb(51, 57, 66);\n"
"    border: 1px solid black;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    background-color: transparent;\n"
"    color: rgb(221, 221, 221);\n"
"}\n"
"\n"
"QMenu::item:selected { /* when user selects item using mouse or keyboard */\n"
"    background-color: #654321;\n"
"}")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.bottomBar = QFrame(self.centralwidget)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setStyleSheet(u"background-color: rgb(33, 37, 43)")
        self._31 = QHBoxLayout(self.bottomBar)
        self._31.setSpacing(0)
        self._31.setObjectName(u"_31")
        self._31.setContentsMargins(0, 0, 0, 0)
        self.credits = QPushButton(self.bottomBar)
        self.credits.setObjectName(u"credits")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.credits.sizePolicy().hasHeightForWidth())
        self.credits.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/icons/icons/meta.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.credits.setIcon(icon)

        self._31.addWidget(self.credits, 0, Qt.AlignmentFlag.AlignLeft)

        self.sizeGrip = QFrame(self.bottomBar)
        self.sizeGrip.setObjectName(u"sizeGrip")
        self.sizeGrip.setMinimumSize(QSize(22, 0))
        self.sizeGrip.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))

        self._31.addWidget(self.sizeGrip, 0, Qt.AlignmentFlag.AlignRight)


        self.gridLayout.addWidget(self.bottomBar, 4, 0, 1, 2)

        self.contentTop = QFrame(self.centralwidget)
        self.contentTop.setObjectName(u"contentTop")
        self.contentTop.setMinimumSize(QSize(0, 50))
        self.contentTop.setMaximumSize(QSize(16777215, 50))
        self.contentTop.setStyleSheet(u"QPushButton {\n"
"	border: 3px;\n"
"	border-radius: 5px;	\n"
"	background-color: transparent;\n"
"	padding: 10px }\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 3px solid rgb(61, 70, 86) }\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 3px solid rgb(43, 50, 61) }\n"
"QLabel { qproperty-alignment: AlignVCenter }")
        self._15 = QHBoxLayout(self.contentTop)
        self._15.setSpacing(0)
        self._15.setObjectName(u"_15")
        self._15.setContentsMargins(0, 0, 7, 0)
        self.autoSave = QPushButton(self.contentTop)
        self.autoSave.setObjectName(u"autoSave")
        sizePolicy.setHeightForWidth(self.autoSave.sizePolicy().hasHeightForWidth())
        self.autoSave.setSizePolicy(sizePolicy)
        self.autoSave.setStyleSheet(u"background-color: transparent;\n"
"border: none")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/autoSaveOff.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/icons/icons/autoSaveOn-01.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.autoSave.setIcon(icon1)
        self.autoSave.setIconSize(QSize(50, 25))
        self.autoSave.setCheckable(True)

        self._15.addWidget(self.autoSave)

        self.comboBox = QComboBox(self.contentTop)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self._15.addWidget(self.comboBox)

        self.dragLabel = QLabel(self.contentTop)
        self.dragLabel.setObjectName(u"dragLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dragLabel.sizePolicy().hasHeightForWidth())
        self.dragLabel.setSizePolicy(sizePolicy1)

        self._15.addWidget(self.dragLabel)

        self.navigationBar = QFrame(self.contentTop)
        self.navigationBar.setObjectName(u"navigationBar")
        self._16 = QHBoxLayout(self.navigationBar)
        self._16.setSpacing(0)
        self._16.setObjectName(u"_16")
        self._16.setContentsMargins(0, 0, 0, 0)
        self.minimizeBtn = QPushButton(self.navigationBar)
        self.minimizeBtn.setObjectName(u"minimizeBtn")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(True)
        font.setItalic(False)
        self.minimizeBtn.setFont(font)
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/minimize.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeBtn.setIcon(icon2)

        self._16.addWidget(self.minimizeBtn)

        self.changeWindowBtn = QPushButton(self.navigationBar)
        self.changeWindowBtn.setObjectName(u"changeWindowBtn")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/maximize.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addFile(u":/icons/icons/restore.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.changeWindowBtn.setIcon(icon3)
        self.changeWindowBtn.setCheckable(True)

        self._16.addWidget(self.changeWindowBtn)

        self.closeBtn = QPushButton(self.navigationBar)
        self.closeBtn.setObjectName(u"closeBtn")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/close.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeBtn.setIcon(icon4)

        self._16.addWidget(self.closeBtn)


        self._15.addWidget(self.navigationBar, 0, Qt.AlignmentFlag.AlignRight)


        self.gridLayout.addWidget(self.contentTop, 0, 0, 1, 2)

        self.cookieFrame = QFrame(self.centralwidget)
        self.cookieFrame.setObjectName(u"cookieFrame")
        self.cookieFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.cookieFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.cookieFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.label_6 = QLabel(self.cookieFrame)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.cookieInput = QLineEdit(self.cookieFrame)
        self.cookieInput.setObjectName(u"cookieInput")

        self.horizontalLayout_2.addWidget(self.cookieInput)


        self.gridLayout.addWidget(self.cookieFrame, 1, 0, 1, 1)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.send = QWidget()
        self.send.setObjectName(u"send")
        self.gridLayout_2 = QGridLayout(self.send)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.sendOK = QPushButton(self.send)
        self.sendOK.setObjectName(u"sendOK")
        sizePolicy.setHeightForWidth(self.sendOK.sizePolicy().hasHeightForWidth())
        self.sendOK.setSizePolicy(sizePolicy)
        self.sendOK.setMinimumSize(QSize(0, 70))
        self.sendOK.setToolTipDuration(2000)
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/post.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sendOK.setIcon(icon5)
        self.sendOK.setIconSize(QSize(50, 50))

        self.gridLayout_2.addWidget(self.sendOK, 4, 1, 1, 1)

        self.label_5 = QLabel(self.send)
        self.label_5.setObjectName(u"label_5")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setBold(False)
        font1.setItalic(False)
        self.label_5.setFont(font1)

        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 2)

        self.listLink = QPlainTextEdit(self.send)
        self.listLink.setObjectName(u"listLink")

        self.gridLayout_2.addWidget(self.listLink, 1, 0, 1, 2)

        self.label_7 = QLabel(self.send)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)

        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)

        self.message = QPlainTextEdit(self.send)
        self.message.setObjectName(u"message")

        self.gridLayout_2.addWidget(self.message, 3, 0, 2, 1)

        self.logFrame = QFrame(self.send)
        self.logFrame.setObjectName(u"logFrame")
        self.logFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.logFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.logFrame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_8 = QLabel(self.logFrame)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)
        self.label_8.setFont(font1)

        self.horizontalLayout_6.addWidget(self.label_8)

        self.copyLogBtn = QPushButton(self.logFrame)
        self.copyLogBtn.setObjectName(u"copyLogBtn")
        self.copyLogBtn.setMaximumSize(QSize(30, 33))
        self.copyLogBtn.setToolTipDuration(3000)
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/copy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.copyLogBtn.setIcon(icon6)
        self.copyLogBtn.setIconSize(QSize(15, 20))

        self.horizontalLayout_6.addWidget(self.copyLogBtn, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.sendLog = HighlightPlainTextEdit(self.logFrame)
        self.sendLog.setObjectName(u"sendLog")
        self.sendLog.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.sendLog)


        self.gridLayout_2.addWidget(self.logFrame, 0, 2, 5, 1)

        self.stackedWidget.addWidget(self.send)
        self.tag = QWidget()
        self.tag.setObjectName(u"tag")
        self.gridLayout_4 = QGridLayout(self.tag)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.listName = HighlightPlainTextEdit(self.tag)
        self.listName.setObjectName(u"listName")
        self.listName.setFont(font1)

        self.gridLayout_4.addWidget(self.listName, 4, 0, 1, 6)

        self.frame_2 = QFrame(self.tag)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.linkPost = QLineEdit(self.frame_2)
        self.linkPost.setObjectName(u"linkPost")

        self.horizontalLayout.addWidget(self.linkPost)


        self.gridLayout_4.addWidget(self.frame_2, 2, 0, 1, 6)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, -1, 5, -1)
        self.delayCheckbox = QCheckBox(self.tag)
        self.delayCheckbox.setObjectName(u"delayCheckbox")
        sizePolicy.setHeightForWidth(self.delayCheckbox.sizePolicy().hasHeightForWidth())
        self.delayCheckbox.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.delayCheckbox)

        self.delay = QLineEdit(self.tag)
        self.delay.setObjectName(u"delay")
        sizePolicy.setHeightForWidth(self.delay.sizePolicy().hasHeightForWidth())
        self.delay.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.delay)

        self.delayLabel = QLabel(self.tag)
        self.delayLabel.setObjectName(u"delayLabel")

        self.verticalLayout.addWidget(self.delayLabel)


        self.gridLayout_4.addLayout(self.verticalLayout, 5, 4, 1, 1)

        self.tagStatus = HighlightLabel(self.tag)
        self.tagStatus.setObjectName(u"tagStatus")
        self.tagStatus.setFont(font1)

        self.gridLayout_4.addWidget(self.tagStatus, 6, 0, 1, 6)

        self.getNameBtn = QPushButton(self.tag)
        self.getNameBtn.setObjectName(u"getNameBtn")
        self.getNameBtn.setToolTipDuration(3000)

        self.gridLayout_4.addWidget(self.getNameBtn, 3, 5, 1, 1)

        self.tagOK = QPushButton(self.tag)
        self.tagOK.setObjectName(u"tagOK")
        sizePolicy.setHeightForWidth(self.tagOK.sizePolicy().hasHeightForWidth())
        self.tagOK.setSizePolicy(sizePolicy)
        self.tagOK.setMinimumSize(QSize(0, 70))
        self.tagOK.setToolTipDuration(2000)
        self.tagOK.setIcon(icon5)
        self.tagOK.setIconSize(QSize(50, 50))

        self.gridLayout_4.addWidget(self.tagOK, 5, 5, 1, 1)

        self.fromGroupCheckbox = QCheckBox(self.tag)
        self.fromGroupCheckbox.setObjectName(u"fromGroupCheckbox")
        self.fromGroupCheckbox.setFont(font1)
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/ImportFromGroup.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fromGroupCheckbox.setIcon(icon7)
        self.fromGroupCheckbox.setIconSize(QSize(40, 32))

        self.gridLayout_4.addWidget(self.fromGroupCheckbox, 3, 0, 1, 1)

        self.frame = QFrame(self.tag)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 120))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_11)

        self.comment = QPlainTextEdit(self.frame)
        self.comment.setObjectName(u"comment")
        self.comment.setFont(font1)

        self.horizontalLayout_3.addWidget(self.comment)


        self.gridLayout_4.addWidget(self.frame, 5, 0, 1, 4)

        self.linkForName = QLineEdit(self.tag)
        self.linkForName.setObjectName(u"linkForName")

        self.gridLayout_4.addWidget(self.linkForName, 3, 1, 1, 4)

        self.stackedWidget.addWidget(self.tag)

        self.gridLayout.addWidget(self.stackedWidget, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.credits.setText(QCoreApplication.translate("MainWindow", u" cre: h0anq.qianq", None))
        self.autoSave.setText("")
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"G\u1eecI HO\u1ea0T \u0110\u1ed8NG", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"TAG TH\u00c0NH VI\u00caN", None))

        self.dragLabel.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Cookie", None))
#if QT_CONFIG(tooltip)
        self.sendOK.setToolTip(QCoreApplication.translate("MainWindow", u"G\u1eedi!", None))
#endif // QT_CONFIG(tooltip)
        self.sendOK.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Nh\u1eadp link facebook", None))
        self.listLink.setPlainText("")
        self.listLink.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ng\u0103n c\u00e1ch b\u1edfi d\u1ea5u xu\u1ed1ng d\u00f2ng", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Nh\u1eadp ho\u1ea1t \u0111\u1ed9ng c\u1ea7n g\u1eedi", None))
        self.message.setPlainText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Log", None))
#if QT_CONFIG(tooltip)
        self.copyLogBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Copy c\u00e1c link b\u1ecb l\u1ed7i", None))
#endif // QT_CONFIG(tooltip)
        self.copyLogBtn.setText("")
        self.listName.setPlainText("")
        self.listName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nh\u1eadp list t\u00ean th\u00e0nh vi\u00ean (V\u0103n A, Th\u1ecb B, ...)", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Nh\u1eadp link post", None))
        self.delayCheckbox.setText(QCoreApplication.translate("MainWindow", u"Delay", None))
        self.delay.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0111\u01a1n v\u1ecb: gi\u00e2y", None))
        self.delayLabel.setText(QCoreApplication.translate("MainWindow", u"v\u00ed d\u1ee5: 3, 2, 0.5, 1.5", None))
        self.tagStatus.setText("")
#if QT_CONFIG(tooltip)
        self.getNameBtn.setToolTip(QCoreApplication.translate("MainWindow", u"L\u1ea5y list th\u00e0nh vi\u00ean c\u1ee7a nh\u00f3m", None))
#endif // QT_CONFIG(tooltip)
        self.getNameBtn.setText(QCoreApplication.translate("MainWindow", u"OK", None))
#if QT_CONFIG(tooltip)
        self.tagOK.setToolTip(QCoreApplication.translate("MainWindow", u"Tag!", None))
#endif // QT_CONFIG(tooltip)
        self.tagOK.setText("")
        self.fromGroupCheckbox.setText(QCoreApplication.translate("MainWindow", u"L\u1ea5y t\u1eeb nh\u00f3m facebook", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Nh\u1eadp comment", None))
        self.comment.setPlainText("")
        self.linkForName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0110i\u1ec1n link nh\u00f3m facebook", None))
    # retranslateUi