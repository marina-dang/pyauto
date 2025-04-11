import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  # 正确导入Firefox配置类
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import os
from datetime import datetime

class TestBase(unittest.TestCase):
    def setUp(self):
        firefox_options = Options()  # 使用Firefox专属配置对象
        # 保持浏览器打开用于调试（需放在driver实例化前）
        firefox_options.add_argument("--foreground")
        # firefox_options.add_argument("--headless")  # 无头模式可按需开启
        
        service = Service(GeckoDriverManager(
            version="v0.33.0"
        ).install())
        
        self.driver = webdriver.Firefox(
            service=service,
            options=firefox_options  # 应用配置选项
        )
        self.driver.implicitly_wait(10)

    @property
    def screenshot_dir(self):
        """统一截图目录属性"""
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(project_root, 'screenshots')
    
    # 测试基类处理全局异常
    def _capture_failure(self, error):
        self.driver.save_screenshot(...)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/failure_{self.__class__.__name__}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"[DEBUG] Current URL...")

    def tearDown(self):
        """统一异常处理"""
        if hasattr(self, '_outcome'):
            result = self._outcome.result
            if result.errors or result.failures:
                for test, exc in result.errors + result.failures:
                    if exc:
                        self._capture_failure(exc[1])
            if hasattr(self, 'driver'):
                self.driver.quit()
        super().tearDown()

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def _log_visible_elements(self):
        """记录页面元素辅助调试"""
        try:
            elements = self.home_page.get_visible_elements()
            print(f"[DEBUG] 可见元素: {elements[:5]}...")  # 只打印前5个避免日志过长
        except Exception as e:
            print(f"[WARN] 元素获取失败: {str(e)}")
