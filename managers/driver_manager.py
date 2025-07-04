from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class DriverManager:
    def __init__(self, chrome_path: str):
        self.driver = None
        self.chrome_path = chrome_path
        self.language = "vi"
        self.friend_str = "Bạn bè"
        self.message_str = "Nhắn tin"
        self.send_str = "Nhấn Enter để gửi"
        self.comment_as_str = "Bình luận dưới tên"
        self.close_chat_str = "Đóng đoạn chat"
        self.error_message = ["Bạn hiện không xem được nội dung này", "Trang này không hiển thị"]

    def setup_driver(self) -> bool:
        try:
            self.driver.title
            return True
        except:
            options = Options()
            options.add_experimental_option("detach", True) # Giữ cửa sổ mở
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            currentDirectory = os.getcwd()
            profilePath = os.path.join(currentDirectory, self.chrome_path)
            # profilePath = "D:\\demo\\ToolHanhChinh\\ChromeData"
            options.add_argument("user-data-dir=" + profilePath) # Chỉ định profile cho browser
            options.add_argument("--disable-notifications")
            options.add_argument("--window-size=1130,500")
            try:
                self.driver = webdriver.Chrome(options=options)
                self.wait20 = WebDriverWait(self.driver, 20)
                self.wait15 = WebDriverWait(self.driver, 15)
                self.wait10 = WebDriverWait(self.driver, 10)
                self.wait5 = WebDriverWait(self.driver, 5)
            except:
                return False
            return True

    def adjust_language(self, force="none"):
        if force == "none":
            self.language = self.driver.find_element(By.XPATH, "//html").get_attribute('lang')
        else: self.language = force
        if self.language != "en":
            self.message_str = "Nhắn tin"
            self.send_str = "Nhấn Enter để gửi"
            self.comment_as_str = "Bình luận dưới tên"
            self.close_chat_str = "Đóng đoạn chat"
            self.friend_str = "Bạn bè"
            self.login_str = "Đăng nhập"
            self.error_messages = ["Bạn hiện không xem được nội dung này", "Trang này không hiển thị"]
        else:
            self.message_str = "Message"
            self.send_str = "Press enter to send"
            self.comment_as_str = "Comment as"
            self.close_chat_str = "Close chat"
            self.friend_str = "Friends"
            self.login_str = "Log in"
            self.error_messages = ["This content isn't available right now", "This Page Isn't Available"]
    
    def handle_chat_close(self):
        script = f"""
        let closeButtons = document.evaluate(
            "//div[@aria-label='{self.close_chat_str}']",
            document,
            null,
            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
            null
        );

        for (let i = 0; i < closeButtons.snapshotLength; i++) {{
            closeButtons.snapshotItem(i).click();
        }}
        """

        # Execute the JavaScript in the browser
        self.driver.execute_script(script)
    
    def get(self, url):
        if self.driver is not None:
            self.driver.get(url)
    
    def check_login(self) -> bool:
        self.is_login = self.friend_str in self.driver.page_source
        return self.is_login
    
    def jump_to_facebook(self) -> bool:
        self.driver.get("https://www.facebook.com/login")
        self.adjust_language()
        self.check_login()
        return self.is_login

    def add_cookie(self, cookie_string: str):
        cookies = [cookie.strip() for cookie in cookie_string.split(';')]
        for cookie in cookies:
            name, value = cookie.split('=', 1)
            self.driver.add_cookie({'name': name, 'value': value})

    def close(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
    
    def scroll_to_bottom(self, max_scrolls: int = 30, timeout: float = 5.0) -> None:
        """Scroll until no new content is loaded or max_scrolls is reached."""
        for i in range(max_scrolls):
            try:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script(f"window.scrollTo(0, {last_height});")

                WebDriverWait(self.driver, timeout).until(
                    lambda d: d.execute_script("return document.body.scrollHeight") > last_height
                )
            except:
                print(f"[Scroll {i+1}] No more new content.")
                break
    
    def wait_for_element(self, by, value):
        try:
            return self.wait15.until(EC.presence_of_element_located((by, value)))
        except Exception as e:
            print(f"Error waiting for element: {e}")
            return None