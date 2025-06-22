from PySide6.QtWidgets import QMainWindow, QSizeGrip
from PySide6.QtCore import QPoint, Qt, QEvent, QThreadPool
from PySide6.QtGui import QShortcut, QKeySequence, QMouseEvent
import pyperclip

from gui.ui_interface import Ui_MainWindow
from gui.custom_grips import CustomGrip

from manager import DataManager, DriverManager
from workers import SendMessage, TagMembers, GetNames

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.dragPos = QPoint()

        # Remove window tittle bar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        def doubleClickMaximizeRestore(event: QMouseEvent):
            if event.type() == QEvent.Type.MouseButtonDblClick:
                self.ui.changeWindowBtn.click()
        self.ui.contentTop.mouseDoubleClickEvent = doubleClickMaximizeRestore

        def moveWindow(event: QMouseEvent):
            if self.isMaximized() == True:
                self.showNormal()
                self.move(event.globalPosition().toPoint() - QPoint(900/2, 0))
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()
        
        self.ui.dragLabel.mouseMoveEvent = moveWindow
        # Resize window
        self.sizegrip = QSizeGrip(self.ui.sizeGrip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")
        # CUSTOM GRIPS
        self.left_grip = CustomGrip(self, Qt.Edge.LeftEdge, True)
        self.right_grip = CustomGrip(self, Qt.Edge.RightEdge, True)
        self.top_grip = CustomGrip(self, Qt.Edge.TopEdge, True)
        self.bottom_grip = CustomGrip(self, Qt.Edge.BottomEdge, True)

        self.left_grip.setGeometry(0, 5, 5, self.height())
        self.right_grip.setGeometry(self.width() - 5, 5, 5, self.height())
        self.top_grip.setGeometry(0, 0, self.width(), 5)
        self.bottom_grip.setGeometry(0, self.height() - 5, self.width(), 5)
        # Minimize window
        self.ui.minimizeBtn.clicked.connect(self.showMinimized)
        # Close window
        self.ui.closeBtn.clicked.connect(self.close)
        # Restore/Maximize window
        self.ui.changeWindowBtn.clicked.connect(self.maximize_restore)
        
        self.data_manager = DataManager()
        self.init_textbox()
        self.driver_manager = DriverManager(self.data_manager.chrome_path)
        self.send = SendMessage(self.driver_manager, self.data_manager)
        self.tag = TagMembers(self.driver_manager, self.data_manager)
        self.get_names = GetNames(self.driver_manager, self.data_manager)
        self.send.setAutoDelete(False)
        self.tag.setAutoDelete(False)
        self.get_names.setAutoDelete(False)
        
        # Connect signal update ui
        self.send.signals.log.connect(lambda msg: self.ui.sendLog.setPlainText(msg))
        self.tag.signals.log.connect(lambda msg: self.ui.tagStatus.setText(msg))
        self.tag.signals.list_name.connect(lambda msg: self.ui.listName.setPlainText(msg))
        self.get_names.signals.log.connect(lambda msg: self.ui.tagStatus.setText(msg))
        self.get_names.signals.list_name.connect(lambda msg: self.ui.listName.setPlainText(msg))

        self.ui.comboBox.activated.connect(self.chooseFunction)
        self.ui.fromGroupCheckbox.stateChanged.connect(self.changeUseOfGroup)
        self.ui.delayCheckbox.stateChanged.connect(lambda: self.ui.delay.hide() if self.ui.delay.isVisible() else self.ui.delay.show())
        self.ui.delayCheckbox.stateChanged.connect(lambda: self.ui.delayLabel.hide() if self.ui.delayLabel.isVisible() else self.ui.delayLabel.show())
        
        self.ui.sendOK.clicked.connect(self.run_guiHD)
        self.ui.tagOK.clicked.connect(self.run_tag)
        self.ui.getNameBtn.clicked.connect(self.run_get_names)
        self.ui.autoSave.clicked.connect(self.data_manager.set_autosave)
        self.ui.copyLogBtn.clicked.connect(self.copy_error_link)
        self.ui.credits.clicked.connect(self.access_credit)
        
        saveData_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        saveData_shortcut.activated.connect(lambda: self.save_data())
        
        self.show()

    def maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.sizeGrip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()
        else:
            self.showMaximized()
            self.ui.sizeGrip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
    def mousePressEvent(self, event):
        # Get the current position of the mouse
        self.dragPos = event.globalPosition().toPoint()
    def resize_grips(self):
        self.left_grip.setGeometry(0, 5, 5, self.height())
        self.right_grip.setGeometry(self.width() - 5, 5, 5, self.height())
        self.top_grip.setGeometry(0, 0, self.width(), 5)
        self.bottom_grip.setGeometry(0, self.height() - 5, self.width(), 5)
    def resizeEvent(self, event):
        # Update Size Grips
        self.resize_grips()
        
    def chooseFunction(self):
        currentFunc = self.ui.comboBox.currentText()
        if currentFunc == "GỬI HOẠT ĐỘNG":
            self.ui.stackedWidget.setCurrentWidget(self.ui.send)
        elif currentFunc == "TAG THÀNH VIÊN":
            self.ui.stackedWidget.setCurrentWidget(self.ui.tag)
    def changeUseOfGroup(self):
        if self.ui.fromGroupCheckbox.isChecked():
            self.ui.linkForName.show()
            self.ui.getNameBtn.show()
        else:
            self.ui.linkForName.hide()
            self.ui.getNameBtn.hide()
    
    def init_textbox(self):
        self.data_manager.load_data()
        data = self.data_manager.data
        cookies = data["COOKIES"]
        
        # Gui hoat dong
        list_link = data["GUI_HOAT_DONG"]["links"]
        message = data["GUI_HOAT_DONG"]["message"]
        
        # Tag thanh vien
        link_post = data["TAG_THANH_VIEN"]["link_post"]
        link_group = data["TAG_THANH_VIEN"]["link_group"]
        list_name = data["TAG_THANH_VIEN"]["members"]
        comment = data["TAG_THANH_VIEN"]["comment"]
                
        self.ui.cookieInput.setText(cookies)
        self.ui.listLink.setPlainText("\n".join(list_link))
        self.ui.message.setPlainText(message)
        
        self.ui.linkPost.setText(link_post)
        self.ui.linkForName.setText(link_group)
        self.ui.listName.setPlainText(", ".join(list_name))
        self.ui.comment.setPlainText(comment)
        
        self.ui.listLink.setPlaceholderText("\n".join(self.data_manager.DEFAULT_DATA["GUI_HOAT_DONG"]["links"]))
        self.ui.cookieInput.setPlaceholderText(self.data_manager.DEFAULT_DATA["COOKIES"])
        self.ui.message.setPlaceholderText(self.data_manager.DEFAULT_DATA["GUI_HOAT_DONG"]["message"])
        
        self.ui.linkPost.setPlaceholderText(self.data_manager.DEFAULT_DATA["TAG_THANH_VIEN"]["link_post"])
        self.ui.linkForName.setPlaceholderText(self.data_manager.DEFAULT_DATA["TAG_THANH_VIEN"]["link_group"])
        self.ui.comment.setPlaceholderText(self.data_manager.DEFAULT_DATA["TAG_THANH_VIEN"]["comment"])
        
        self.ui.fromGroupCheckbox.setChecked(False)
        self.ui.autoSave.click()
        self.ui.linkForName.hide()
        self.ui.getNameBtn.hide()
        self.ui.delay.hide()
        self.ui.delayLabel.hide()
        self.ui.logFrame.hide()
        
    def copy_error_link(self):
        pyperclip.copy(self.data_manager.error_link)
        self.ui.sendLog.setPlainText(f"Đã copy các link bị lỗi!\n{self.ui.sendLog.toPlainText()}")
    def save_data(self):
        self.data_manager.data["COOKIES"] = self.ui.cookieInput.text().strip()
        
        self.data_manager.data["GUI_HOAT_DONG"] = {
            "links": list(map(str.strip, self.ui.listLink.toPlainText().split("\n"))),
            "message": self.ui.message.toPlainText().strip()
        }
        
        if self.ui.delayCheckbox.isChecked() or self.ui.delay.text() == "":
            delay_value = None
        else:
            delay_value = int(self.ui.delay.text())

        self.data_manager.data["TAG_THANH_VIEN"] = {
            "link_post": self.ui.linkPost.text().strip(),
            "link_group": self.ui.linkForName.text().strip(),
            "members": list(map(str.strip, self.ui.listName.toPlainText().split(","))),
            "comment": self.ui.comment.toPlainText().strip(),
            "delay": delay_value
        }
        if self.data_manager.save_data():
            if self.ui.stackedWidget.currentWidget() == self.ui.send:
                self.ui.logFrame.show()
                self.ui.sendLog.setPlainText(f"Đã lưu dữ liệu vào file {self.data_manager.data_path}\n{self.ui.sendLog.toPlainText()}")
            elif self.ui.stackedWidget.currentWidget() == self.ui.tag:
                self.ui.tagStatus.setText(f"Đã lưu dữ liệu vào file {self.data_manager.data_path}")
        else:
            if self.ui.stackedWidget.currentWidget() == self.ui.send:
                self.ui.sendLog.setPlainText(f"Không thể lưu dữ liệu vào file đang mở\n{self.ui.sendLog.toPlainText()}")
            elif self.ui.stackedWidget.currentWidget() == self.ui.tag:
                self.ui.tagStatus.setText("Không thể lưu dữ liệu vào file đang mở")
            return
    def access_credit(self):
        if not self.driver_manager.setup_driver():
            if self.ui.stackedWidget.currentWidget() == self.ui.send:
                self.ui.sendLog.setPlainText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            elif self.ui.stackedWidget.currentWidget() == self.ui.tag:
                self.ui.tagStatus.setText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver_manager.driver.execute_script('window.open("https://www.facebook.com/h0anq.qianq/")')
        self.driver_manager.driver.switch_to.window(self.driver_manager.driver.window_handles[0])
    
    def run_guiHD(self):
        self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
        self.ui.logFrame.show()
        
        self.data_manager.data["COOKIES"] = self.ui.cookieInput.text()
        self.data_manager.data["GUI_HOAT_DONG"]["links"] = [x.strip() for x in self.ui.listLink.toPlainText().split("\n") if x.strip()]
        self.data_manager.data["GUI_HOAT_DONG"]["message"] = self.ui.message.toPlainText().strip()

        QThreadPool.globalInstance().start(self.send)
        
    def run_tag(self):
        self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
        
        # Update data before run
        self.data_manager.data["COOKIES"] = self.ui.cookieInput.text()
        self.data_manager.data["TAG_THANH_VIEN"]["link_post"] = self.ui.linkPost.text().strip()
        self.data_manager.data["TAG_THANH_VIEN"]["link_group"] =  self.ui.linkForName.text().strip()
        self.data_manager.data["TAG_THANH_VIEN"]["members"] = list(map(str.strip, self.ui.listName.toPlainText().split(",")))
        self.data_manager.data["TAG_THANH_VIEN"]["comment"] = self.ui.comment.toPlainText().strip()
        if self.ui.delayCheckbox.isChecked():
            try:
                self.data_manager.data["TAG_THANH_VIEN"]["delay"] = int(self.ui.comment.toPlainText())
            except:
                self.data_manager.data["TAG_THANH_VIEN"]["delay"] = 1
        else:
            self.data_manager.data["TAG_THANH_VIEN"]["delay"] = None
        
        # ✅ Defer start by one event loop cycle to ensure all connections are live
        QThreadPool.globalInstance().start(self.tag)
    
    def run_get_names(self):
        self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
        
        # Update data before run
        self.data_manager.data["COOKIES"] = self.ui.cookieInput.text()
        self.data_manager.data["TAG_THANH_VIEN"]["link_post"] = self.ui.linkPost.text().strip()
        self.data_manager.data["TAG_THANH_VIEN"]["link_group"] =  self.ui.linkForName.text().strip()
        self.data_manager.data["TAG_THANH_VIEN"]["members"] = list(map(str.strip, self.ui.listName.toPlainText().split(",")))
        self.data_manager.data["TAG_THANH_VIEN"]["comment"] = self.ui.comment.toPlainText().strip()
        if self.ui.delayCheckbox.isChecked():
            try:
                self.data_manager.data["TAG_THANH_VIEN"]["delay"] = int(self.ui.comment.toPlainText())
            except:
                self.data_manager.data["TAG_THANH_VIEN"]["delay"] = 1
        else:
            self.data_manager.data["TAG_THANH_VIEN"]["delay"] = None
        
        # ✅ Defer start by one event loop cycle to ensure all connections are live
        QThreadPool.globalInstance().start(self.get_names)