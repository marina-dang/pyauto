from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException 

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.home_signup_btn = (By.XPATH, "/html/body/div[1]/div[3]/header/div/div[2]/div/div/a")
        self.home_signin_btn = (By.XPATH, "/html/body/div[1]/div[3]/header/div/div[2]/div/div/div/a")
    
    def is_signup_visible(self):
        """调用基类方法时去掉super()"""
        return self.is_visible(self.home_signup_btn, timeout=15)
    
    def get_visible_elements(self):
        """安全获取可见元素"""
        try:
            return [e.text for e in self.driver.find_elements(By.XPATH, '//*') 
                   if e.is_displayed() and e.is_enabled()]
        except StaleElementReferenceException:
            return ["元素状态已过期，无法获取完整列表"]