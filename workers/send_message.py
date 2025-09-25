from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PySide6.QtCore import QObject, QRunnable, Slot, Signal
import pyperclip, time

from managers import DataManager, DriverManager

class SendMessage(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        
    def __init__(self, driver_manager: DriverManager, data_manager: DataManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.data_manager = data_manager
        self.signals = self.Signals()
    
    @Slot()
    def run(self):
        self.cookies: str = self.data_manager.data["COOKIES"]
        self.list_link: list[str] = self.data_manager.data["GUI_HOAT_DONG"]["links"]
        self.message: str = self.data_manager.data["GUI_HOAT_DONG"]["message"]
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
        self.signals.log.emit("Đang gửi hoạt động...")
        status = ""
        actions = ActionChains(self.driver)
        if not bool(self.list_link) or self.message == "":
            self.signals.log.emit("Thiếu thông tin: Hoạt động")
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
                    self.signals.log.emit(status)
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
                                        (link := div.find_element(By.XPATH, "./div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a"))
                                        and link.get_attribute("aria-label").strip() not in ("", None)
                                        and link
                                    )
                                )

                                username = username_div.get_attribute("aria-label").strip()
                                if name in username:
                                    target_chat = div
                                    break
                            except Exception as e:
                                print(f"{name} Error finding chat: {e}")
                                continue
                            
                        if not target_chat:
                            self.driver_manager.handle_chat_close()
                            raise Exception(f"{name} Chat not found")
                        
                        time.sleep(0.5)

                        textbox = WebDriverWait(target_chat, 10).until(
                            EC.element_to_be_clickable((By.XPATH, ".//div[@aria-placeholder='Aa']"))
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
                        
                        # Optional: Wait for paste effect
                        self.driver_manager.wait5.until(
                            lambda d: d.execute_script("return arguments[0].innerText.trim().length > 0;", textbox)
                        )
                        # self.driver_manager.wait5.until(lambda _: textbox.text != "")
                        
                        send = WebDriverWait(target_chat, 10).until(EC.element_to_be_clickable(
                            (By.XPATH, f".//div[@aria-label='{self.driver_manager.send_str}']")
                        ))
                        send.click()
                        # actions.send_keys(Keys.ENTER).perform()
                        
                        time.sleep(1) # delay after send_message action
                        
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
                        if any(message in self.driver.page_source for message in self.driver_manager.error_messages):
                            status = f"❌ {link}\n{status}"
                            self.data_manager.error_link = f"{link}\n{self.data_manager.error_link}"
                            self.signals.log.emit(status)
                            error_count += 1
                            break
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
            self.signals.log.emit(status)
        status = f"Đã gửi xong!!\nthành công {success_count}, lỗi {error_count}\n{status}"
        self.data_manager.error_link = self.data_manager.error_link.strip()
        self.signals.log.emit(status)
        if self.data_manager.auto_save: self.data_manager.save_data()