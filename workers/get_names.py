from selenium.webdriver.common.by import By
from PySide6.QtCore import QObject, QRunnable, Slot, Signal

from managers import DataManager, DriverManager

class GetNames(QRunnable):
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
            
    def get_member_name(self):
        self.cookies: str = self.data_manager.data["COOKIES"]
        self.link_group: str = self.data_manager.data["TAG_THANH_VIEN"]["link_group"]
        try:
            group_id = self.link_group.split("groups/")[1].split("/")[0]
        except:
            self.signals.log.emit("Link nhóm facebook không hợp lệ")
            return
        if group_id == "":
            self.signals.log.emit("Thiếu thông tin: Link nhóm")
            return
        count = 0
        while 1:
            count += 1
            if count == 5:
                self.signals.log.emit("Xảy ra lỗi")
                break
            try:
                self.driver.get(f"https://www.facebook.com/groups/{group_id}/members")
                self.driver_manager.adjust_language()
                if any(message in self.driver.page_source for message in self.driver_manager.error_messages):
                    self.signals.log.emit("Không thể truy cập nhóm!")
                    return
                try:
                    self.signals.log.emit("Đang lấy danh sách tên thành viên...")
                    self.driver_manager.scroll_to_bottom()
                    list_member = self.driver.find_elements(By.XPATH,'//div[@class="html-div x14z9mp x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x1oo3vh0 x1rdy4ex"]')[-1].find_elements(By.XPATH, "./*")
                except:
                    self.signals.log.emit("Xảy ra lỗi!")
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
        self.signals.list_name.emit(list_name_str)
        self.signals.log.emit(f"Đã lấy xong danh sách tên thành viên: {member_count} người")
        if self.data_manager.auto_save:
            self.data_manager.data["TAG_THANH_VIEN"]["members"] = list(map(str.strip, list_name_str.split(",")))
            self.data_manager.save_data()
    
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
        self.get_member_name()