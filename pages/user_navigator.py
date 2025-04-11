from .base_page import BasePage
from selenium.webdriver.common.by import By

class UserNav(BasePage):
    """用户菜单统一管理类"""
    def __init__(self, driver):
        super().__init__(driver)
        self.usrnav = (By.XPATH, '//button[@aria-label="Open user navigation menu"]')
        self.usrnav_signout = (By.XPATH, '//*[@id=":r16:--label"]')
        # self.usrnav_signout = (By.XPATH, "//span[@class='Box-sc-g0xbh4-0 jtiCfm' and @text()='Sign out']")
        # self.usrnav_signout = (By.XPATH, '//div[@data-component="ActionList.Item--DividerContainer"]/span[contains(@class, "jtiCfm") and text()="Sign out"]')
        self.usrnav_your_profile = (By.XPATH, '//a[contains(text(),"Your profile")]')
        