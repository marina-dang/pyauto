import unittest
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.test_base import TestBase
from pages.auth import LoginPage

class LoginErrorTest(TestBase):
    def setUp(self):
        super().setUp()
        self.login_page = LoginPage(self.driver)
        self.login_url = os.getenv('GITHUB_LOGIN_URL', 'https://github.com/login')

    def test_invalid_credentials(self):
        # 定义测试数据（第37行附近）
        test_cases = [
            ("invalid12345", "dummypass", "无效凭证组合1"),
            ("marina-dang", "wrongpwd_!", "无效凭证组合2"),
        ]

        for username, password, case_desc in test_cases:
            with self.subTest(case_desc=case_desc):
                self.driver.get(self.login_url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "login"))
                )
                self.driver.refresh()
                self.login_page.enter_credentials(username, password)
                self.login_page.click_login()

                # 验证错误信息
                error_text = self.login_page.get_error_text()
                try:
                    self.assertIn("Incorrect username or password", error_text,
                                f"{case_desc} 测试未触发预期错误")
                except AssertionError:
                    self.take_screenshot(f"{self._testMethodName}_{case_desc}_FAILED")  # 仅在失败时截图
                    raise
                
                self.driver.delete_all_cookies()  # 清理cookies
                
                # 添加网络延迟容忍（当前第66行）
                WebDriverWait(self.driver, 15).until(
                    lambda d: "login" not in d.current_url
                )

if __name__ == '__main__':
    unittest.main()