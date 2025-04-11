from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from .user_navigator import UserNav
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username_field = (By.ID, 'login_field')
        self.password_field = (By.ID, 'password')
        self.signin_button = (By.NAME, 'commit')
        self.error_message = (By.XPATH, "//div[@class='js-flash-alert']")
        self.user_avatar = (By.XPATH, "//button[@aria-label='Open user navigation menu']")

    def login(self, username, password):
        self.enter_credentials(username, password)
        self.click_login()
    
    def enter_credentials(self, username, password):
        self.driver.find_element(*self.username_field).send_keys(username)
        self.driver.find_element(*self.password_field).send_keys(password)
    
    def click_login(self):
        try:
            self.wait_click(self.signin_button)
        except TimeoutException as e:
            self.driver.save_screenshot('login_button_timeout.png')
            raise Exception(f"登录按钮点击失败: {str(e)}")
    
    def wait_login_success(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.user_avatar)
            )
            return True
        except TimeoutException as e:
            self.driver.save_screenshot('login_success_timeout.png')
            return False
    
    def get_error_text(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.error_message)
            )
            return self.driver.find_element(*self.error_message).text
        except TimeoutException as e:
            self.driver.save_screenshot('error_timeout.png')
            raise Exception(f"错误信息加载超时: {str(e)}")

class LogoutPage(UserNav):
    def __init__(self, driver):
        super().__init__(driver)
        self.confirm_signout = (By.XPATH, '//input[@value="Sign out"]')

    def perform_logout(self):
        try:
            menu = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.usrnav)
            )
            ActionChains(self.driver).move_to_element(menu).click().perform()

            self.driver.execute_script("""
                arguments[0].scrollTop = arguments[0].scrollHeight;
            """, menu)

            signout_option = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.usrnav_signout)
            )

            self.driver.execute_script("""
                const elem = arguments[0];
                elem.scrollIntoView({block: "center", behavior: "instant"});
            """, signout_option)
            
            signout_option.click()
            WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.confirm_signout)).click()
            
        except Exception as e:
            super().take_screenshot('logout_failure') 
            raise