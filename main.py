from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PySide6.QtWidgets import QMainWindow, QApplication, QSizeGrip
from PySide6.QtCore import QPoint, Qt, QEvent, QRunnable, Slot, QThreadPool, QTimer, Signal
from PySide6.QtGui import QShortcut, QKeySequence, QMouseEvent
import time, sys, os
import pyperclip

from gui.ui_interface import Ui_MainWindow
from gui.custom_grips import CustomGrip
from driver_manager import DriverManager
from data_manager import DataManager

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
        self.driver_manager = DriverManager(self.data_manager.chrome_path)

        self.ui.comboBox.activated.connect(self.chooseFunction)
        self.ui.fromGroupCheckbox.stateChanged.connect(self.changeUseOfGroup)
        self.ui.delayCheckbox.stateChanged.connect(lambda: self.ui.delay.hide() if self.ui.delay.isVisible() else self.ui.delay.show())
        self.ui.delayCheckbox.stateChanged.connect(lambda: self.ui.delayLabel.hide() if self.ui.delayLabel.isVisible() else self.ui.delayLabel.show())
        
        self.ui.sendOK.clicked.connect(self.run_guiHD)
        self.ui.tagOK.clicked.connect(lambda: self.run_tag("tag"))
        self.ui.getNameBtn.clicked.connect(lambda: self.run_tag("get_member_name"))
        self.ui.autoSave.clicked.connect(self.data_manager.set_autosave)
        self.ui.copyLogBtn.clicked.connect(self.copy_error_link)
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
        
        self.data_manager.data["TAG_THANH_VIEN"] = {
            "link_post": self.ui.linkPost.text().strip(),
            "link_group": self.ui.linkForName.text().strip(),
            "members": list(map(str.strip, self.ui.listName.toPlainText().split(","))),
            "comment": self.ui.comment.toPlainText().strip()
        }
        if self.data_manager.save_data():
            if self.ui.stackedWidget.currentWidget() == self.ui.send:
                self.ui.sendLog.setPlainText(f"Đã lưu dữ liệu vào file {self.file_path}\n{self.ui.sendLog.toPlainText()}")
            elif self.ui.stackedWidget.currentWidget() == self.ui.tag:
                self.ui.tagStatus.setText(f"Đã lưu dữ liệu vào file {self.file_path}")
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
    
    def run_tag(self, action: str):
        self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
        tag_thanh_vien = Tag_thanh_vien(self.driver_manager, self.ui, action, self.data_manager)
        tag_thanh_vien.run()
    
    def run_guiHD(self):
        self.move(self.screen().size().width()- self.size().width(), self.screen().size().height() - self.size().height() - 50)
        self.ui.logFrame.show()
        QApplication.processEvents()  # Let Qt update the GUI now
        guiHD = Gui_hoat_dong(self.driver_manager, self.ui, self.data_manager)
        guiHD.run()
        
class Gui_hoat_dong:
    def __init__(self, driver_manager: DriverManager, ui: Ui_MainWindow, data_manager: DataManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.ui = ui
        self.data_manager = data_manager
        self.cookies = self.data_manager.data["COOKIES"]
        self.list_link = self.data_manager.data["GUI_HOAT_DONG"]["links"]
        self.message = self.data_manager.data["GUI_HOAT_DONG"]["message"]
        
    def run(self):
        if not self.driver_manager.setup_driver():
            self.ui.sendLog.setPlainText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver = self.driver_manager.driver
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.is_login:
            self.cookies = self.ui.cookieInput.text()
            if self.cookies != "":
                self.driver_manager.add_cookie(self.cookies)
                self.driver.refresh()
                self.driver_manager.wait_for_element(By.ID, "facebook")
                if not self.driver_manager.check_login():
                    self.ui.sendLog.setPlainText("Chưa đăng nhập, sai cookie")
                    return
            else:
                self.ui.sendLog.setPlainText("Chưa đăng nhập, vui lòng điền cookie")
                return
        self.ui.sendLog.setPlainText("Đang gửi hoạt động...")
        status = ""
        self.message = self.ui.message.toPlainText().strip()
        actions = ActionChains(self.driver)
        self.list_link = [x.strip() for x in self.ui.listLink.toPlainText().split("\n") if x.strip()]
        if not bool(self.list_link) or self.message == "":
            self.ui.sendLog.setPlainText("Thiếu thông tin: Hoạt động")
            return
        self.data_manager.error_link = ""
        success_count = 0
        error_count = 0
        for link in self.list_link:
            if len(link.strip()) > 8:
                if link[0] == "f":
                    link = "https://web." + link
                try:
                    self.driver.get(link)
                    if any(message in self.driver.page_source for message in self.driver_manager.error_messages):
                        raise Exception(f"Error user link")
                    if "locale=" in link:
                        self.driver_manager.adjust_language(link.split("locale=")[1][:2])
                    self.driver.execute_script("window.scrollTo(0, 300)")
                    self.driver_manager.handle_chat_close()
                    lst = self.driver_manager.wait15.until(EC.presence_of_all_elements_located(
                        (By.XPATH, "//div[@class='xdwrcjd x2fvf9 x1xmf6yo x1w6jkce xusnbm3']")
                    ))
                    isFriend = False
                    if lst[0].text == self.driver_manager.friend_str:
                        isFriend = True
                    get_name_script = """
                        return arguments[0].firstChild.nodeValue;
                    """
                    name = self.driver.execute_script(get_name_script, self.driver.find_element(By.XPATH, "//div[@class='x1e56ztr x1xmf6yo']/span/h1"))
                except:
                    status = f"❌ {link}\n{status}"
                    self.data_manager.error_link = f"{link}\n{self.data_manager.error_link}"
                    self.ui.sendLog.setPlainText(status)
                    error_count += 1
                    continue
                for attempt in range(1, 6):
                    try:
                        # Make sure correct element is found
                        if len(lst) < 2 or lst[1].text != self.driver_manager.message_str:
                            status = f"{name} - Chưa kết bạn, không thể inbox\n" + status
                            break
                        
                        # Click the 'Nhắn tin' button
                        NhanTin = self.driver_manager.wait15.until(EC.element_to_be_clickable(
                            (By.XPATH, f"//div[@aria-label='{self.driver_manager.message_str}']")
                        ))
                        NhanTin.click()
                        
                        # Wait until chat container appears
                        self.driver_manager.wait15.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR,
                            "html > body > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(5) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > *")) >= 1)
                        
                        chat_divs = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            "html > body > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(5) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > *"
                        )
                        
                        target_chat = None
                        
                        for div in chat_divs:
                            try:
                                # Wait until the text of the div is not empty
                                username_div = self.driver_manager.wait20.until(
                                    lambda _: (
                                        (hl := div.find_element(By.XPATH, "./div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]//h2")).text.strip() != "" and hl
                                    )
                                )

                                username = username_div.text.strip()
                                if name in username:
                                    target_chat = div
                                    break
                            except Exception as e:
                                print("Error finding chat:", e)
                                continue
                            
                        if not target_chat:
                            self.driver_manager.handle_chat_close()
                            raise Exception("Chat not found")

                        textbox = WebDriverWait(target_chat, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[@aria-placeholder='Aa']"))
                        )
                        actions.click(textbox).perform()
                        
                        # Wait until it becomes the active element (cursor is inside)
                        try:
                            self.driver_manager.wait5.until(
                                lambda d: d.execute_script("return document.activeElement === arguments[0];", textbox)
                            )
                        except:
                            # Retry click once more if needed
                            actions.click(textbox).perform()
                            self.driver_manager.wait5.until(
                                lambda d: d.execute_script("return document.activeElement === arguments[0];", textbox)
                            )
                        
                        pyperclip.copy(self.message)
                        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                        
                        self.driver_manager.wait5.until(lambda _: textbox.text != "")  # Optional: Wait for paste effect
                        
                        send = WebDriverWait(target_chat, 10).until(EC.element_to_be_clickable(
                            (By.XPATH, f"//div[@aria-label='{self.driver_manager.send_str}']")
                        ))
                        send.click()
                        # actions.send_keys(Keys.ENTER).perform()
                        
                        close_chat = target_chat.find_element(By.XPATH, f"//div[@aria-label='{self.driver_manager.close_chat_str}']")
                        close_chat.click()
                        
                        # ✅ Wait until target_chat disappears from the DOM
                        self.driver_manager.wait5.until(EC.staleness_of(target_chat))
                        
                        if isFriend:
                            status = f"✔️ {name}\n{status}"
                        else:
                            status = f"✔️ {name}, chưa kết bạn\n{status}"   
                            
                        if attempt == 3:
                            self.driver.get(link)
                            if "locale=" in link:
                                self.driver_manager.adjust_language(link.split("locale=")[1][:2])
                            self.driver.execute_script("window.scrollTo(0, 300)")
                            self.driver_manager.handle_chat_close()
                        
                        success_count += 1
                        break
                    
                    except Exception as e:
                        print("Error during message sending:", e)
                        if self.driver.get_window_size()["width"] <= 912:
                            self.driver.set_window_size(1130, 500)
                        self.driver_manager.handle_chat_close()
                        lst = self.driver_manager.wait15.until(EC.presence_of_all_elements_located(
                            (By.XPATH, "//div[@class='xdwrcjd x2fvf9 x1xmf6yo x1w6jkce xusnbm3']")
                        ))

                        if attempt == 5:
                            status = f"❌ {name}\n{status}"
                            self.data_manager.error_link = f"{link}\n{self.data_manager.error_link}"
                            error_count += 1
                            break
            elif len(link.strip()) > 0:
                status = f"❌ {link}\n{status}"
                self.data_manager.error_link = f"{link}\n{self.data_manager.error_link}"
                error_count += 1
            self.ui.sendLog.setPlainText(status)
        status = f"Đã gửi xong!!\nthành công {success_count}, lỗi {error_count}\n{status}"
        self.data_manager.error_link = self.data_manager.error_link.strip()
        self.ui.sendLog.setPlainText(status)
        if self.data_manager.auto_save: self.data_manager.save_data()
        
class Tag_thanh_vien:
    def __init__(self, driver_manager: DriverManager, ui: Ui_MainWindow, action: str, data_manager: DataManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.driver = self.driver_manager.driver
        self.action = action
        self.ui = ui
        self.data_manager = data_manager
        self.cookies = self.data_manager.data["COOKIES"]
        self.list_name = self.data_manager.data["TAG_THANH_VIEN"]["members"]
        self.comment = self.data_manager.data["TAG_THANH_VIEN"]["comment"]
    def check_open_post(self):
        div = self.driver.find_element(By.XPATH, "//div[@role='banner']/following-sibling::div[1]")
        if div.get_attribute("class") == "x9f619 x1n2onr6 x1ja2u2z":
            return False
        else: return True
    def tag(self):
        self.list_name = list(map(str.strip, self.ui.listName.toPlainText().split(",")))
        if not any(name for name in self.list_name if name):
            self.ui.tagStatus.setText("Thiếu thông tin: Tag thành viên")
            return
        self.comment = self.ui.comment.toPlainText()
        self.list_name.append(self.comment)
        self.driver.get(self.ui.linkPost.text())
        if "locale=" in self.ui.linkPost.text():
            self.driver_manager.adjust_language(self.ui.linkPost.text().split("locale=")[1][:2])
        if any(message in self.driver.page_source for message in self.driver_manager.error_messages):
            self.ui.tagStatus.setText("Không thể thao tác với bài đăng!")
            return
        self.ui.tagStatus.setText("Đang tag thành viên...")
        
        actions = ActionChains(self.driver)
        delay = 1
        if self.ui.delayCheckbox.isChecked():
            try:
                delay = float(self.ui.delay.text())
            except: delay = 1
        error_name = ""
        count_error = 0
        if self.check_open_post():
            suggestion_css = "div.x78zum5.xdt5ytf.xg6iff7.xippug5.x1n2onr6 > div:nth-of-type(3) > div"
            actions.send_keys(Keys.TAB).perform()
        else:
            suggestion_css = "div.x78zum5.xdt5ytf.x1n2onr6.xat3117.xxzkxad > div:nth-of-type(2) > div"
        for i, name in enumerate(self.list_name):
            for attemp in range(1, 6):
                try:
                    index_error = 0
                    textbox = self.driver_manager.wait10.until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[@role='textbox' and @aria-placeholder[starts-with(., '{self.driver_manager.comment_as_str}')]]"))
                    )
                    index_error = 1
                    is_active = self.driver.execute_script("return document.activeElement === arguments[0];", textbox)
                    if is_active == False:
                        actions.click(textbox).perform()
                        actions.key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()
                        time.sleep(0.5)
                    if i == len(self.list_name) - 1:
                        pyperclip.copy(self.comment)
                        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                        break
                    textbox.send_keys("@", name)
                    
                    if self.ui.delayCheckbox.isChecked():
                        time.sleep(3 if attemp == 1 else delay)
                    index_error = 2
                    self.driver_manager.wait10.until(
                        lambda driver: len(driver.find_element(By.CSS_SELECTOR, suggestion_css).find_elements(By.XPATH, "./*")) >= 1
                    )
                    index_error = 3
                    
                    textbox.send_keys(Keys.TAB)
                    time.sleep(0.5)
                    textbox.send_keys(" ")
                    break
                except:
                    if self.driver.get_window_size()["width"] <= 912:
                        self.driver.set_window_size(1130, 500)
                    self.driver_manager.handle_chat_close()
                    if attemp == 2:
                        if i == 0: # First name error -> clear all + re tag
                            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                            actions.send_keys(Keys.BACKSPACE).perform()
                        else: # Not first name error + have typed name -> send " "
                            if index_error == 2:
                                textbox.send_keys(" ")
                    if attemp == 5:
                        error_name += name + " "
                        count_error += 1
                        break
                    if count_error >= 2:
                        self.ui.tagStatus.setText(f"Đã xảy ra lỗi khi tag: {error_name.strip()}")
                        return
        if error_name != "":
            self.ui.tagStatus.setText(f"Đã tag xong, tên bị lỗi: {error_name.strip()}")
        else:
            self.ui.tagStatus.setText("Đã tag xong, vui lòng bấm gửi comment!")
        if self.data_manager.auto_save:
            self.data_manager.save_data()
            self.ui.tagStatus.setText(f"Đã lưu dữ liệu vào file {self.data_manager.data_path}")
            
    def get_member_name(self):
        try:
            group_id = self.ui.linkForName.text().split("groups/")[1].split("/")[0]
        except:
            self.ui.tagStatus.setText("Link nhóm facebook không hợp lệ")
            return
        if group_id == "":
            self.ui.tagStatus.setText("Thiếu thông tin: Link nhóm")
            return
        count = 0
        while 1:
            count += 1
            if count == 5:
                self.ui.tagStatus.setText("Xảy ra lỗi")
                break
            try:
                self.driver.get(f"https://www.facebook.com/groups/{group_id}/members")
                self.driver_manager.adjust_language()
                if any(message in self.driver.page_source for message in self.driver_manager.error_messages):
                    self.ui.tagStatus.setText("Không thể truy cập nhóm!")
                    return
                try:
                    self.ui.tagStatus.setText("Đang lấy danh sách tên thành viên...")
                    self.driver_manager.scroll_to_bottom()
                    list_member = self.driver.find_elements(By.XPATH,'//div[@class="html-div x14z9mp x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x1oo3vh0 x1rdy4ex"]')[-1].find_elements(By.XPATH, "./*")
                except:
                    self.ui.tagStatus.setText("Xảy ra lỗi!")
                    return
                list_name_str = ""
                member_count = 0
                for member in list_member:
                    name_member = member.find_element(By.XPATH, "div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/span[1]").text.strip()
                    list_name_str += f"{name_member}, "
                    member_count += 1
                list_name_str = list_name_str.rstrip(", ")
                break
            except:
                self.driver_manager.handle_chat_close()
        self.ui.listName.setPlainText(list_name_str)
        self.ui.tagStatus.setText(f"Đã lấy xong danh sách tên thành viên: {member_count} người")
        if self.data_manager.auto_save:
            self.data_manager.save_data()
            self.ui.tagStatus.setText(f"Đã lưu dữ liệu vào file {self.data_manager.data_path}")
        
    def run(self):
        if not self.driver_manager.setup_driver():
            self.ui.tagStatus.setText("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver = self.driver_manager.driver
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.is_login:
            self.cookies = self.ui.cookieInput.text()
            if self.cookies != "":
                self.driver_manager.add_cookie(self.cookies)
                self.driver.refresh()
                self.driver_manager.wait_for_element(By.ID, "facebook")
                if not self.driver_manager.check_login():
                    self.ui.tagStatus.setText("Chưa đăng nhập, sai cookie")
                    return
            else:
                self.ui.tagStatus.setText("Chưa đăng nhập, vui lòng điền cookie")
                return
        if self.action == "tag":
            self.tag()
        elif self.action == "get_member_name":
            self.get_member_name()

if __name__ == "__main__":
    if not os.path.exists("ChromeData"): # Nếu chưa có Folder lưu data -> Tạo
        os.makedirs("ChromeData")
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())