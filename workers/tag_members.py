from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from PySide6.QtCore import QObject, QRunnable, Slot, Signal
import time
import pyperclip

from manager import DataManager, DriverManager

class TagMembers(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        list_name = Signal(str)
        
    def __init__(self, driver_manager: DriverManager, data_manager: DataManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.driver = self.driver_manager.driver
        self.data_manager = data_manager
        self.signals = self.Signals()
        
    def check_open_post(self):
        div = self.driver.find_element(By.XPATH, "//div[@role='banner']/following-sibling::div[1]")
        if div.get_attribute("class") == "x9f619 x1n2onr6 x1ja2u2z":
            return False
        else: return True
    def tag(self):
        self.cookies: str = self.data_manager.data["COOKIES"]
        self.link_post: str = self.data_manager.data["TAG_THANH_VIEN"]["link_post"]
        self.list_name: list[str] = self.data_manager.data["TAG_THANH_VIEN"]["members"]
        self.comment: str = self.data_manager.data["TAG_THANH_VIEN"]["comment"]
        self.delay: int = self.data_manager.data["TAG_THANH_VIEN"]["delay"]
        if not any(name for name in self.list_name if name):
            self.signals.log.emit("Thiếu thông tin: Tag thành viên")
            return
        self.list_name.append(self.comment)
        
        self.driver.get(self.link_post)
        if "locale=" in self.link_post:
            self.driver_manager.adjust_language(self.link_post.split("locale=")[1][:2])
        if any(message in self.driver.page_source for message in self.driver_manager.error_messages):
            self.signals.log.emit("Không thể thao tác với bài đăng!")
            return
        self.signals.log.emit("Đang tag thành viên...")
        
        actions = ActionChains(self.driver)
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
                    
                    if self.delay is not None:
                        time.sleep(3 if attemp == 1 else self.delay)
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
                        self.signals.log.emit(f"Đã xảy ra lỗi khi tag: {error_name.strip()}")
                        return
        if error_name != "":
            self.signals.log.emit(f"Đã tag xong, tên bị lỗi: {error_name.strip()}")
        else:
            self.signals.log.emit("Đã tag xong, vui lòng bấm gửi comment!")
        if self.data_manager.auto_save: self.data_manager.save_data()
    
    @Slot()
    def run(self):
        if not self.driver_manager.setup_driver():
            self.signals.log.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            return
        self.driver = self.driver_manager.driver
        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.is_login:
            if self.cookies != "":
                self.driver_manager.add_cookie(self.cookies)
                self.driver.refresh()
                self.driver_manager.wait_for_element(By.ID, "facebook")
                if not self.driver_manager.check_login():
                    self.signals.log.emit("Chưa đăng nhập, sai cookie")
                    return
            else:
                self.signals.log.emit("Chưa đăng nhập, vui lòng điền cookie")
                return
        self.tag()