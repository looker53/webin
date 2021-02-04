from webin.element import Input, Button, Div


class LoginPage:
    username_el = Input('用户输入框', name='phone')
    pwd_el = Input(desc='密码输入框', name='password')
    login_btn_el = Button(desc='登录按钮', xpath='//button[@class="btn btn-special"]')
    error_msg_el = Div(desc='错误提示框', class_='form-error-info')

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.goto('http://120.78.128.25:8765/Index/login.html')
        return self

    def login(self, username, pwd):
        self.username_el.fill(username)
        self.pwd_el.fill(pwd)
        self.login_btn_el.click()
        return self

    @property
    def error_msg(self):
        return self.error_msg_el.text

