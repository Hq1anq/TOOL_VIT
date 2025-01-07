from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PySide6.QtWidgets import QMainWindow, QApplication, QSizeGrip
from PySide6.QtCore import QPoint, Qt, QEvent, QRunnable, Slot, QThreadPool, QTimer, Signal
from PySide6.QtGui import QShortcut, QKeySequence, QGuiApplication
import time, sys, os
import pyperclip
import pandas as pd
from ui_interface import Ui_MainWindow
from custom_grips import CustomGrip

class MainWindow(QMainWindow):
    log_updated = Signal(str)
    tag_status_updated = Signal(str)
    tag_name_updated = Signal(str)
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.dragPos = QPoint()
        
        self.default_cookies = "c_user=...;fr=...;sb=...;xs=...;datr=..."
        self.default_list_link = ["https://www.facebook.com/profile.php?id=...", "https://m.facebook.com/...",
                                      "https://www.facebook.com/..."]
        self.default_message = '''[VIT][ĐI DẠY]
- Thời gian: ...
- Địa điểm: Nhà nuôi dưỡng trẻ em Hữu Nghị Đống Đa (102 phố Yên Lãng, quận Đống Đa)
- Số lượng: 6 - 8 TNV
- Trang phục: Áo xanh, đeo thẻ SV
CF ĐĂNG KÝ KÈM PHƯƠNG TIỆN (NẾU CÓ).
HẠN ĐĂNG KÝ: ...'''
        self.default_link_post = "https://www.facebook.com/groups/.../posts/..."
        self.default_link_group = "https://www.facebook.com/groups/..."
        self.default_name = ["Văn A", "Thị B", "Nguyễn C"]
        self.default_comment = "cf nào mọi người"
        self.file_path = "Data.xlsx"
        self.driver = None
        self.autoSave = False
    
        # Remove window tittle bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        def doubleClickMaximizeRestore(event):
            if event.type() == QEvent.MouseButtonDblClick:
                self.ui.changeWindowBtn.click()
        self.ui.contentTop.mouseDoubleClickEvent = doubleClickMaximizeRestore

        def moveWindow(event):
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

        self.ui.comboBox.activated.connect(self.chooseFunction)
        self.ui.fromGroupCheckbox.stateChanged.connect(self.changeUseOfGroup)
        self.ui.delayCheckbox.stateChanged.connect(lambda: self.ui.delay.hide() if self.ui.delay.isVisible() else self.ui.delay.show())
        self.ui.delayCheckbox.stateChanged.connect(lambda: self.ui.delayLabel.hide() if self.ui.delayLabel.isVisible() else self.ui.delayLabel.show())
        
        self.ui.sendOK.clicked.connect(lambda: run_gui_hoat_dong(self))
        self.ui.tagOK.clicked.connect(lambda: run_tag_thanh_vien(self, "tag"))
        self.ui.getNameBtn.clicked.connect(lambda: run_tag_thanh_vien(self, "get_member_name"))
        self.ui.autoSave.clicked.connect(self.set_autosave)
        self.ui.credits.clicked.connect(self.access_credit)
        
        saveData_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        saveData_shortcut.activated.connect(lambda: self.save_data())
        
        self.show()
        
        self.init_textbox()
        
        self.log_updated.connect(self.update_log)
        self.tag_status_updated.connect(self.update_tag_status)
        self.tag_name_updated.connect(self.update_tag_name)
        
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
            
    def update_log(self, text):
        self.ui.sendLog.setPlainText(text)
        self.ui.sendLog.setStyleSheet("color: yellow")
        QTimer.singleShot(1000, self.reset_log_color)
    def update_tag_status(self, status):
        self.ui.tagStatus.setText(status)
        self.ui.tagStatus.setStyleSheet("color: yellow")
        QTimer.singleShot(1000, self.reset_tag_color)
    def update_tag_name(self, name):
        self.ui.listName.setPlainText(name)
        self.ui.listName.setStyleSheet("color: yellow")
        QTimer.singleShot(1000, self.reset_name_color)
    def reset_log_color(self):
        self.ui.sendLog.setStyleSheet("color: white")
    def reset_tag_color(self):
        self.ui.tagStatus.setStyleSheet("color: white")
    def reset_name_color(self):
        self.ui.listName.setStyleSheet("color: white")
    def create_df(self, content_data, fields):
        # Tạo DataFrame từ content_data
        content_df = pd.DataFrame(content_data)
        
        # Tìm chiều dài tối đa của các danh sách trong các cột
        max_len = max(len(content_data[0][field]) if isinstance(content_data[0][field], list) else 1 for field in fields)
        
        # Mở rộng các danh sách để có cùng độ dài
        for field in fields:
            # content_df[field] = content_df[field].apply(lambda x: x + [None] * (max_len - len(x)))
            # Đảm bảo mọi giá trị trong `field` là danh sách
            if not isinstance(content_data[0][field], list):
                content_data[0][field] = [content_data[0][field]]
            # Mở rộng danh sách để có chiều dài tối đa
            content_df[field] = [content_data[0][field] + [None] * (max_len - len(content_data[0][field]))]
        
        # Explode các cột để chuyển các mục trong danh sách thành các hàng riêng biệt
        content_df = content_df.explode(fields).astype(str).replace("None", "")
        return content_df
    def DF2List(self, dataframe, col):
        return [x.strip() for x in dataframe[col].tolist() if pd.notna(x) and x.strip() != ""]
    def init_textbox(self):
        if not os.path.exists(self.file_path):
            cookies = self.default_cookies
            list_link = self.default_list_link
            message = self.default_message
            guiHoatDong_data = [{
                "COOKIES": cookies,
                "LINK FACEBOOK": list_link,
                "MESSAGE": message
            }]
            link_post = self.default_link_post
            link_group = self.default_link_group
            list_name = self.default_name
            comment = self.default_comment
            tag_data = [{
                "LINK POST": link_post,
                "LINK GROUP (FOR GET USER NAME)": link_group,
                "NAME (FOR TAG)": list_name,
                "COMMENT": comment
            }]
            guiHoatDong_DF = self.create_df(guiHoatDong_data, ["COOKIES", "LINK FACEBOOK", "MESSAGE"])
            tag_DF = self.create_df(tag_data, ["LINK POST", "LINK GROUP (FOR GET USER NAME)", "NAME (FOR TAG)", "COMMENT"])
            guiHoatDong_DF.to_excel(self.file_path, sheet_name="Gui hoat dong", index=False)
            with pd.ExcelWriter(self.file_path, mode="a", if_sheet_exists="replace") as writer:
                tag_DF.to_excel(writer, sheet_name="Tag thanh vien", index=False)
        else:
            try:
                guiHoatDong_DF = pd.read_excel(self.file_path, sheet_name="Gui hoat dong")
                cookies = guiHoatDong_DF.at[0, "COOKIES"] if pd.notna(guiHoatDong_DF.at[0, "COOKIES"]) else ""
                list_link = self.DF2List(guiHoatDong_DF, "LINK FACEBOOK")
                message = guiHoatDong_DF.at[0, "MESSAGE"] if pd.notna(guiHoatDong_DF.at[0, "MESSAGE"]) else ""
            except:
                cookies = self.default_cookies
                list_link = self.default_list_link
                message = self.default_message
                guiHoatDong_data = [{
                    "COOKIES": cookies,
                    "LINK FACEBOOK": list_link,
                    "MESSAGE": message
                }]
                guiHoatDong_DF = self.create_df(guiHoatDong_data, ["COOKIES", "LINK FACEBOOK", "MESSAGE"])
                try:
                    with pd.ExcelWriter(self.file_path, mode="a", if_sheet_exists="replace") as writer:
                        guiHoatDong_DF.to_excel(writer, sheet_name="Gui hoat dong", index=False)
                except:
                    self.log_updated.emit("Không thể thao tác với file đang mở")
            try:
                tag_DF = pd.read_excel(self.file_path, sheet_name="Tag thanh vien")
                link_post = tag_DF.at[0, "LINK POST"] if pd.notna(tag_DF.at[0, "LINK POST"]) else ""
                link_group = tag_DF.at[0, "LINK GROUP (FOR GET USER NAME)"] if pd.notna(tag_DF.at[0, "LINK GROUP (FOR GET USER NAME)"]) else ""
                list_name = self.DF2List(tag_DF, "NAME (FOR TAG)")
                comment = tag_DF.at[0, "COMMENT"] if pd.notna(tag_DF.at[0, "COMMENT"]) else ""
            except:
                link_post = self.default_link_post
                link_group = self.default_link_group
                list_name = self.default_name
                comment = self.default_comment
                tag_data = [{
                    "LINK POST": link_post,
                    "LINK GROUP (FOR GET USER NAME)": link_group,
                    "NAME (FOR TAG)": list_name,
                    "COMMENT": comment
                }]
                tag_DF = self.create_df(tag_data, ["LINK POST", "LINK GROUP (FOR GET USER NAME)", "NAME (FOR TAG)", "COMMENT"])
                try:
                    with pd.ExcelWriter(self.file_path, mode="a", if_sheet_exists="replace") as writer:
                        tag_DF.to_excel(writer, sheet_name="Tag thanh vien", index=False)
                except:
                    self.tag_status_updated.emit("Không thể thao tác với file đang mở")
                
        self.ui.cookieInput.setText(cookies)
        self.ui.listLink.setPlainText("\n".join(list_link))
        self.ui.message.setPlainText(message)
        
        self.ui.linkPost.setText(link_post)
        self.ui.linkForName.setText(link_group)
        self.ui.listName.setPlainText(", ".join(list_name))
        self.ui.comment.setPlainText(comment)
        
        self.ui.listLink.setPlaceholderText("\n".join(self.default_list_link))
        self.ui.cookieInput.setPlaceholderText(self.default_cookies)
        self.ui.message.setPlaceholderText(self.default_message)
        
        self.ui.linkPost.setPlaceholderText(self.default_link_post)
        self.ui.linkForName.setPlaceholderText(self.default_link_group)
        self.ui.comment.setPlaceholderText(self.default_comment)
        
        self.ui.fromGroupCheckbox.setChecked(False)
        self.ui.autoSave.click()
        self.ui.linkForName.hide()
        self.ui.getNameBtn.hide()
        self.ui.delay.hide()
        self.ui.delayLabel.hide()
    def set_autosave(self):
        self.autoSave = not self.autoSave
    def is_file_open(self):
        try:
            file = open(self.file_path, "a")
            file.close()
            return False
        except:
            return True
    def save_data(self):
        if self.is_file_open():
            if self.ui.stackedWidget.currentWidget() == self.ui.send:
                self.log_updated.emit(f"Không thể lưu dữ liệu vào file đang mở\n{self.ui.sendLog.toPlainText()}")
            elif self.ui.stackedWidget.currentWidget() == self.ui.tag:
                self.tag_status_updated.emit("Không thể lưu dữ liệu vào file đang mở")
            return
        guiHoatDong_data = [{
                "COOKIES": self.ui.cookieInput.text().strip(),
                "LINK FACEBOOK": list(map(str.strip, self.ui.listLink.toPlainText().split("\n"))),
                "MESSAGE": self.ui.message.toPlainText().strip()
            }]
        tag_data = [{
                "LINK POST": self.ui.linkPost.text().strip(),
                "LINK GROUP (FOR GET USER NAME)": self.ui.linkForName.text().strip(),
                "NAME (FOR TAG)": list(map(str.strip, self.ui.listName.toPlainText().split(","))),
                "COMMENT": self.ui.comment.toPlainText().strip()
            }]
        guiHoatDong_DF = self.create_df(guiHoatDong_data, ["COOKIES", "LINK FACEBOOK", "MESSAGE"])
        tag_DF = self.create_df(tag_data, ["LINK POST", "LINK GROUP (FOR GET USER NAME)", "NAME (FOR TAG)", "COMMENT"])
        with pd.ExcelWriter(self.file_path, mode="a", if_sheet_exists="replace") as writer:
            guiHoatDong_DF.to_excel(writer, sheet_name="Gui hoat dong", index=False)
            tag_DF.to_excel(writer, sheet_name="Tag thanh vien", index=False)
        if self.ui.stackedWidget.currentWidget() == self.ui.send:
            self.log_updated.emit(f"Đã lưu dữ liệu vào file {self.file_path}\n{self.ui.sendLog.toPlainText()}")
        elif self.ui.stackedWidget.currentWidget() == self.ui.tag:
            self.tag_status_updated.emit(f"Đã lưu dữ liệu vào file {self.file_path}")
    def access_credit(self):
        if self.driver is None:
            options = Options()
            options.add_experimental_option("detach", True) # Giữ cửa sổ mở
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            currentDirectory = os.getcwd()
            profilePath = os.path.join(currentDirectory, "ChromeData")
            options.add_argument("user-data-dir=" + profilePath) # Chỉ định profile cho browser
            options.add_argument("--disable-notifications")
            options.add_argument("--window-size=1200,500")
            try:
                self.driver = webdriver.Chrome(options=options)
            except:
                self.log_updated.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
                return
            self.driver.implicitly_wait(5)
        try:
            self.driver.execute_script('window.open("https://www.facebook.com/h0anq.qianq/")')
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:
            options = Options()
            options.add_experimental_option("detach", True) # Giữ cửa sổ mở
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            currentDirectory = os.getcwd()
            profilePath = os.path.join(currentDirectory, "ChromeData")
            options.add_argument("user-data-dir=" + profilePath) # Chỉ định profile cho browser
            options.add_argument("--disable-notifications")
            options.add_argument("--window-size=1200,500")
            try:
                self.driver = webdriver.Chrome(options=options)
            except:
                self.log_updated.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
                return
            self.driver.implicitly_wait(5)
            self.driver.execute_script('window.open("https://www.facebook.com/h0anq.qianq/")')
            self.driver.switch_to.window(self.driver.window_handles[0])
        
class Gui_hoat_dong(QRunnable):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.ui = main.ui
        self.cookies = ""
        self.list_link = ""
        self.message = ""
    @Slot()
    def run(self):
        try:
            self.main.driver.title
        except:
            options = Options()
            options.add_experimental_option("detach", True) # Giữ cửa sổ mở
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            currentDirectory = os.getcwd()
            profilePath = os.path.join(currentDirectory, "ChromeData")
            options.add_argument("user-data-dir=" + profilePath) # Chỉ định profile cho browser
            options.add_argument("--disable-notifications")
            options.add_argument("--window-size=1200,500")
            try:
                self.main.driver = webdriver.Chrome(options=options)
            except:
                self.main.log_updated.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
                return
            self.main.driver.implicitly_wait(5)
        self.main.driver.get("https://facebook.com")
        self.main.driver.set_window_position(0, 0)
        if self.isLogin(self.main.driver):
            pass
        else:
            self.cookies = self.ui.cookieInput.text()
            if self.cookies != "":
                self.AddCookie(self.cookies, self.main.driver)
                self.main.driver.refresh()
                if not self.isLogin(self.main.driver):
                    self.main.log_updated.emit("Chưa đăng nhập, sai cookie")
                    return
            else:
                self.main.log_updated.emit("Chưa đăng nhập, vui lòng điền cookie")
                return
        self.main.log_updated.emit("Đang gửi hoạt động...")
        status = ""
        self.message = self.ui.message.toPlainText()
        pyperclip.copy(self.message)
        actions = ActionChains(self.main.driver)
        self.list_link = [x.strip() for x in self.ui.listLink.toPlainText().split("\n")]
        if self.message == "" or self.list_link[0] == "":
            self.main.log_updated.emit("Thiếu thông tin: Hoạt động")
            return
        for link in self.list_link:
            try:
                self.main.driver.set_window_size(1200, 500)
                if link[0] == "f":
                    link = "https://web." + link
                self.main.driver.get(link)
                self.main.driver.execute_script("window.scrollTo(0, 300)")
                time.sleep(1)
                lst = self.main.driver.find_elements(By.XPATH, "//div[@class='xsgj6o6 xw3qccf x1xmf6yo x1w6jkce xusnbm3']")
                isFriend = False
                if lst[0].text == "Bạn bè":
                    isFriend = True
                name = self.main.driver.find_element(By.XPATH, "//div[@class='x1e56ztr x1xmf6yo']").text.strip()
                count = 0
                while 1:
                    count += 1
                    if count == 10:
                        status = link + " - Xảy ra lỗi\n" + status
                        break
                    try:
                        if lst[1].text != "Nhắn tin":
                            status = link + " - Chưa kết bạn, không thể inbox\n" + status
                            break
                        NhanTin = self.main.driver.find_element(By.XPATH, "//div[@aria-label='Nhắn tin']")
                        NhanTin.click()
                        time.sleep(1)
                        containerChat = self.main.driver.find_elements(By.CSS_SELECTOR, "html > body > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div > div:nth-of-type(5) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > *")
                        if len(containerChat) >= 2:
                            for close in self.main.driver.find_elements(By.XPATH, "//div[@aria-label='Đóng đoạn chat']"):
                                actions.click(close).perform()
                                time.sleep(0.5)
                            NhanTin = self.main.driver.find_element(By.XPATH, "//div[@aria-label='Nhắn tin']")
                            NhanTin.click()
                            time.sleep(1)
                            containerChat = self.main.driver.find_elements(By.CSS_SELECTOR, "html > body > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div > div:nth-of-type(5) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > *")
                            if len(containerChat) >= 2:
                                for close in self.main.driver.find_elements(By.XPATH, "//div[@aria-label='Đóng đoạn chat']"):
                                    actions.click(close).perform()
                                    time.sleep(0.5)
                                NhanTin = self.main.driver.find_element(By.XPATH, "//div[@aria-label='Nhắn tin']")
                                NhanTin.click()
                                time.sleep(1)
                        if isFriend:
                            time.sleep(1)
                            textbox = self.main.driver.find_element(By.XPATH, "//div[@aria-placeholder='Aa']")
                            if (name in textbox.get_attribute("aria-describedby")):
                                actions.click(textbox).perform()
                                time.sleep(1)
                                is_active = self.main.driver.execute_script("return document.activeElement === arguments[0];", textbox)
                                if not is_active:
                                    actions.click(textbox).perform()
                                    time.sleep(1)
                                actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                                status = name + " - đã gửi\n" + status
                            else: 
                                raise Exception
                        else:
                            time.sleep(1)
                            textbox = self.main.driver.find_element(By.XPATH, "//div[@aria-placeholder='Aa']")
                            if (name in textbox.get_attribute("aria-describedby")):
                                actions.click(textbox).perform()
                                time.sleep(1)
                                is_active = self.main.driver.execute_script("return document.activeElement === arguments[0];", textbox)
                                if not is_active:
                                    actions.click(textbox).perform()
                                    time.sleep(1)
                                actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                                status = name + " - đã gửi, chưa kết bạn\n" + status
                            else:
                                raise Exception
                        actions.send_keys(Keys.ENTER).perform()
                        time.sleep(1)
                        close_chat = self.main.driver.find_element(By.XPATH, "//div[@aria-label='Đóng đoạn chat']")
                        actions.click(close_chat).perform()
                        break
                    except:
                        if self.main.driver.get_window_size()["width"] <= 912:
                            self.main.log_updated.emit("Chiều rộng cửa sổ quá bé, vui lòng điều chỉnh lại kích thước cửa sổ")
                        self.handle_chat_close(self.main.driver, actions)
            except:
                status = link + " - Xảy ra lỗi\n" + status
            self.main.log_updated.emit(status)
        status = "Đã gửi xong!!\n" + status
        self.main.log_updated.emit(status)
        if self.main.autoSave: self.main.save_data()
    def handle_chat_close(self, driver, actions):
        containerChat = driver.find_elements(By.CSS_SELECTOR, "html > body > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div > div:nth-of-type(5) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > *")
        if containerChat:
            for close in driver.find_elements(By.XPATH, "//div[@aria-label='Đóng đoạn chat']"):
                actions.click(close).perform()
                time.sleep(0.5)
    def isLogin(self, driver):
        return ("Bạn bè" in driver.page_source) or ("Friends" in driver.page_source)
    def AddCookie(self, cookie_string, driver):
        cookies = [cookie.strip() for cookie in cookie_string.split(';')]
        for cookie in cookies:
            name, value = cookie.split('=', 1)
            driver.add_cookie({'name': name, 'value': value})

class Tag_thanh_vien(QRunnable):
    def __init__(self, main, action):
        super().__init__()
        self.main = main
        self.action = action
        self.ui = main.ui
        self.cookies = ""
        self.list_name = []
        self.comment = ""
    @Slot()
    def handle_chat_close(self, driver, actions):
        containerChat = driver.find_elements(By.CSS_SELECTOR, "html > body > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div > div:nth-of-type(5) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > *")
        if containerChat:
            for close in driver.find_elements(By.XPATH, "//div[@aria-label='Đóng đoạn chat']"):
                actions.click(close).perform()
                time.sleep(0.5)
    def isLogin(self, driver):
        return ("Bạn bè" in driver.page_source) or ("Friends" in driver.page_source)
    def AddCookie(self, cookie_string, driver):
        cookies = [cookie.strip() for cookie in cookie_string.split(';')]
        for cookie in cookies:
            name, value = cookie.split('=', 1)
            driver.add_cookie({'name': name, 'value': value})
    def check_open_post(self, driver):
        div = driver.find_element(By.XPATH, "//div[@role='banner']/following-sibling::div[1]")
        if div.get_attribute("class") == "x9f619 x1n2onr6 x1ja2u2z":
            return False
        else: return True
    def tag(self, driver):
        self.list_name = list(map(str.strip, self.ui.listName.toPlainText().split(",")))
        self.comment = self.ui.comment.toPlainText()
        if self.comment == "" or self.list_name[0] == "":
            self.main.tag_status_updated.emit("Thiếu thông tin: Tag thành viên")
            return
        driver.get(self.ui.linkPost.text())
        if "Bạn hiện không xem được nội dung này" in driver.page_source:
            self.main.tag_status_updated.emit("Không thể thao tác với bài đăng!")
            return
        self.main.tag_status_updated.emit("Đang tag thành viên...")
        actions = ActionChains(driver)
        delay = 1
        if self.ui.delayCheckbox.isChecked():
            try:
                delay = float(self.ui.delay.text())
            except: delay = 1
        error_name = ""
        if self.check_open_post(driver):
            for name in self.list_name:
                if len(name) > 2:
                    try:
                        driver.set_window_size(1200, 500)
                        count = 0
                        while 1:
                            count += 1
                            if count == 10:
                                error_name += name + " "
                                break
                            try:
                                textbox = driver.find_element(By.XPATH, "//div[@class='xwib8y2 xurb0ha x1y1aw1k']//div[@role='textbox']")
                                is_active = driver.execute_script("return document.activeElement === arguments[0];", textbox)
                                if is_active == False:
                                    textbox.click()
                                    actions.key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()
                                    time.sleep(0.5)
                                textbox.send_keys("@", name)
                                if name == self.list_name[0]:
                                    time.sleep(3)
                                else: time.sleep(delay)
                                textbox.send_keys(Keys.TAB)
                                time.sleep(0.5)
                                textbox.send_keys(" ")
                                break
                            except:
                                if driver.get_window_size()["width"] <= 912:
                                    self.main.tag_status_updated.emit("Chiều rộng cửa sổ quá bé, vui lòng điều chỉnh lại kích thước cửa sổ")
                                self.handle_chat_close(driver, actions)
                    except:
                        self.main.tag_status_updated.emit("Xảy ra lỗi")
            cnt = 0
            while 1:
                cnt += 1
                if cnt == 10:
                    self.main.tag_status_updated.emit("Xảy ra lỗi")
                    return
                try:
                    textbox = driver.find_element(By.XPATH, "//div[@class='xwib8y2 xurb0ha x1y1aw1k']//div[@role='textbox']")
                    is_active = driver.execute_script("return document.activeElement === arguments[0];", textbox)
                    if is_active == False:
                        textbox.click()
                        actions.key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()
                        time.sleep(0.5)
                    textbox.send_keys(self.comment)
                    break
                except:
                    self.handle_chat_close(driver, actions)
            self.main.tag_status_updated.emit("Đã tag xong, vui lòng bấm gửi comment!")
            if self.main.autoSave: self.main.save_data()
        else:
            for name in self.list_name:
                if len(name) > 2:
                    try:
                        driver.set_window_size(1200, 500)
                        count = 0
                        while 1:
                            count += 1
                            if count == 10:
                                error_name += name + " "
                                break
                            try:
                                textbox = driver.find_element(By.XPATH,'//div[@class="xzsf02u x1a2a7pz x1n2onr6 x14wi4xw notranslate"]')
                                is_active = driver.execute_script("return document.activeElement === arguments[0];", textbox)
                                if is_active == False:
                                    textbox.click()
                                    actions.key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()
                                    time.sleep(0.5)
                                textbox.send_keys("@", name)
                                if name == self.list_name[0]:
                                    time.sleep(3)
                                else: time.sleep(delay)
                                textbox.send_keys(Keys.TAB)
                                time.sleep(0.5)
                                textbox.send_keys(" ")
                                break
                            except:
                                if driver.get_window_size()["width"] <= 912:
                                    self.main.tag_status_updated.emit("Chiều rộng cửa sổ quá bé, vui lòng điều chỉnh lại kích thước cửa sổ")
                                self.handle_chat_close(driver, actions)
                    except:
                        self.main.tag_status_updated.emit("Xảy ra lỗi")
            cnt = 0
            while 1:
                cnt += 1
                if cnt == 10:
                    self.main.tag_status_updated.emit("Xảy ra lỗi")
                    return
                try:
                    textbox = driver.find_element(By.XPATH,'//div[@class="xzsf02u x1a2a7pz x1n2onr6 x14wi4xw notranslate"]')
                    is_active = driver.execute_script("return document.activeElement === arguments[0];", textbox)
                    if is_active == False:
                        textbox.click()
                        actions.key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()
                        time.sleep(0.5)
                    textbox.send_keys(self.comment)
                    break
                except:
                    self.handle_chat_close(driver, actions)
            if len(error_name) > 2:
                self.main.tag_status_updated.emit("Đã tag xong, tag lỗi: ", error_name)
            else:
                self.main.tag_status_updated.emit("Đã tag xong, vui lòng bấm gửi comment!")
            if self.main.autoSave: self.main.save_data()
    def scroll_to_bottom(self, driver, SCROLL_PAUSE_TIME=1.5):
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    def get_member_name(self, driver):
        try:
            group_id = self.ui.linkForName.text().split("groups/")[1].split("/")[0]
        except:
            self.main.tag_status_updated.emit("Link nhóm facebook không hợp lệ")
            return
        if group_id == "":
            self.main.tag_status_updated.emit("Thiếu thông tin: Link nhóm")
            return
        actions = ActionChains(driver)
        count = 0
        while 1:
            count += 1
            if count == 10:
                self.main.tag_status_updated.emit("Xảy ra lỗi")
                break
            try:
                driver.get(f"https://www.facebook.com/groups/{group_id}/members")
                self.main.tag_status_updated.emit("Đang lấy danh sách tên thành viên...")
                self.scroll_to_bottom(driver)
                list_member = driver.find_elements(By.XPATH,'//div[@class="html-div x11i5rnm x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1oo3vh0 x1rdy4ex"]')[-1].find_elements(By.XPATH, "./*")
                list_name_str = ""
                member_count = 0
                for member in list_member:
                    name_member = member.find_element(By.XPATH,"div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/span[1]/span[1]/a[1]").text.strip()
                    list_name_str += f"{name_member}, "
                    member_count += 1
                list_name_str = list_name_str.rstrip(", ")
                break
            except:
                self.handle_chat_close(driver, actions)
        self.main.tag_name_updated.emit(list_name_str)
        self.main.tag_status_updated.emit(f"Đã lấy xong danh sách tên thành viên: {member_count} người")
        if self.main.autoSave: self.main.save_data()
    def run(self):
        try: self.main.driver.title
        except:
            options = Options()
            options.add_experimental_option("detach", True) # Giữ cửa sổ mở
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            currentDirectory = os.getcwd()
            profilePath = os.path.join(currentDirectory, "ChromeData")
            options.add_argument("user-data-dir=" + profilePath) # Chỉ định profile cho browser
            options.add_argument("--disable-notifications")
            options.add_argument("--window-size=1200,500")
            try:
                self.main.driver = webdriver.Chrome(options=options)
            except:
                self.main.tag_status_updated.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
                return
            self.main.driver.implicitly_wait(5)
        self.main.driver.get("https://facebook.com")
        self.main.driver.set_window_position(0, 0)
        if self.isLogin(self.main.driver):
            pass
        else:
            self.cookies = self.ui.cookieInput.text()
            if self.cookies != "":
                self.AddCookie(self.cookies, self.main.driver)
                self.main.driver.refresh()
                if not self.isLogin(self.main.driver):
                    self.main.tag_status_updated.emit("Chưa đăng nhập, sai cookie")
                    return
            else:
                self.main.tag_status_updated.emit("Chưa đăng nhập, vui lòng điền cookie")
                return
        if self.action == "tag":
            self.tag(self.main.driver)
        elif self.action == "get_member_name":
            self.get_member_name(self.main.driver)

def run_gui_hoat_dong(ui):
    ui.move(ui.screen().size().width()- ui.size().width(), ui.screen().size().height() - ui.size().height() - 50)
    worker = Gui_hoat_dong(ui)
    QThreadPool.globalInstance().start(worker)
def run_tag_thanh_vien(ui, action = "tag"):
    ui.move(ui.screen().size().width()- ui.size().width(), ui.screen().size().height() - ui.size().height() - 50)
    worker = Tag_thanh_vien(ui, action)
    QThreadPool.globalInstance().start(worker)
if __name__ == "__main__":
    if not os.path.exists("ChromeData"): # Nếu chưa có Folder lưu data -> Tạo
        os.makedirs("ChromeData")
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
