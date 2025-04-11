from selenium.webdriver.common.by import By
import unittest
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from tests.test_base import TestBase
from pages.auth import LoginPage

class LoginTest(TestBase):
    def setUp(self):
        super().setUp()
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        env_path = os.path.join(project_root, '.env')  # 指向项目根目录的.env
        load_dotenv(env_path, override=True)
        
        self.valid_user = os.getenv('GITHUB_USER')
        self.valid_pass = os.getenv('GITHUB_PASS')
        if not self.valid_user or not self.valid_pass:
            self.fail(f"环境变量缺失 | 文件路径: {env_path} | 请确认已设置GITHUB_USER和GITHUB_PASS")
        self.login_page = LoginPage(self.driver)
        self.login_url = os.getenv('GITHUB_LOGIN_URL', 'https://github.com/login')
        if not self.valid_user or not self.valid_pass:
            self.fail(f"加载.env失败 | 文件路径: {env_path}")

    def test_successful_login(self):
        """有效凭证登录测试"""
        if not self.valid_user or not self.valid_pass:
            self.skipTest("未配置登录凭证")
            
        self.driver.get(self.login_url)
        self.login_page.enter_credentials(self.valid_user, self.valid_pass)
        self.login_page.click_login()
        
        try:
            self.assertTrue(
                self.login_page.wait_login_success(),
                "用户头像未显示，登录失败"
            )
        except AssertionError as e:
            self.login_page.take_screenshot("login_success_failed")
            raise  # 重新抛出异常保证测试失败
            
        try:
            self.driver.delete_all_cookies()
        except Exception as e:
            print(f"无害的清理错误: {str(e)}")

    def tearDown(self):
        # 添加安全关闭逻辑
        try:
            if hasattr(self.driver, 'service') and self.driver.service.process:
                self.driver.quit()
        except Exception as e:
            print(f"浏览器关闭异常: {str(e)}")

if __name__ == '__main__':
    unittest.main()