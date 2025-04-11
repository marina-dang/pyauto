from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.test_base import TestBase
from pages.auth import LoginPage, LogoutPage
from dotenv import load_dotenv
import unittest
import os
from selenium.common.exceptions import TimeoutException
from pages.home_page import HomePage
from pages.base_page import BasePage

class LogoutTest(TestBase):
    def setUp(self):
        super().setUp()
        self.driver.maximize_window() 
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        env_path = os.path.join(project_root, '.env')
        load_dotenv(env_path, override=True)
        
        self.valid_user = os.getenv('GITHUB_USER')
        self.valid_pass = os.getenv('GITHUB_PASS')
        if not self.valid_user or not self.valid_pass:
            self.fail("环境变量GITHUB_USER/GITHUB_PASS未配置")
            
        self.login_url = os.getenv('GITHUB_LOGIN_URL', 'https://github.com/login')
        self.login_page = LoginPage(self.driver)
        self.logout_page = LogoutPage(self.driver)

    def test_logout(self):
        self.driver.get(self.login_url)
        self.login_page.login(self.valid_user, self.valid_pass)
        self.logout_page.perform_logout()
    
        # 验证1：精确匹配GitHub首页URL
        WebDriverWait(self.driver, 20).until(
            EC.url_to_be("https://github.com/")
        )
        
        # 验证2：检查首页Sign up按钮可见性
        home_page = HomePage(self.driver)
        try:
            self.assertTrue(
                home_page.is_signup_visible(),
                "Sign up按钮未找到，最后可见元素：" + str(home_page.get_visible_elements()))
        except AssertionError:
            BasePage(driver=self.driver).take_screenshot("logout_verification_failed")
            raise