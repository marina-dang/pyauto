from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time
import os

class BasePage:
    """
    元素归属指南：
    - UserNav: 用户导航菜单相关元素
    - LogoutPage: 登出流程专属元素
    - LoginPage: 登录表单相关元素
    """
    def __init__(self, driver):
        self.driver = driver
        self.screenshot_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'screenshots'
        )
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def is_visible(self, locator, timeout=10):
        """检查元素是否可见"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def take_screenshot(self, name):
        """统一截图方法"""
        path = os.path.join(self.screenshot_dir, f"{name}_{time.strftime('%Y%m%d_%H%M%S')}.png")
        self.driver.save_screenshot(path)

    def wait_click(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()