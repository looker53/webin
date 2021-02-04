import time
import pyautogui
import pyperclip
from selenium.webdriver import Remote
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

TIME_OUT = 5
INTERVAL = .5


class Driver:
    host = ''

    def __init__(self, driver: Remote):
        self.driver = driver

    def goto(self, url:str):
        if url.startswith(('http://', 'https://')):
            return self.driver.get(url)
        if not url.startswith('/'):
            return ValueError('url must start with slash /.')
        url = self.host + url
        return self.driver.get(url)

    def click(self, locator):
        el = self.wait_clickable(locator)
        el.click()
        return self

    def type(self, locator, words):
        el = self.wait_element(locator)
        el.send_keys(words)
        return self

    def double_click(self, locator):
        ac = ActionChains(self.driver)
        el = self.wait_clickable(locator)
        ac.double_click(el).perform()
        return self

    def right_click(self, locator):
        ac = ActionChains(self.driver)
        el = self.wait_clickable(locator)
        ac.context_click(el).perform()
        return self

    def drag(self, start_locator, end_locator):
        ac = ActionChains(self.driver)
        el_start = self.wait_element(start_locator)
        el_end = self.wait_element(end_locator)
        ac.drag_and_drop(el_start, el_end).perform()
        return self

    def move_to(self, locator):
        ac = ActionChains(self.driver)
        el = self.wait_clickable(locator)
        ac.move_to_element(el).perform()
        return self

    def switch_to_window(self, window_name):
        self.driver.switch_to.window(window_name=window_name)
        return self

    def switch_to_frame(self, locator, timeout=TIME_OUT, interval=INTERVAL):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=interval)
        wait.until(expected_conditions.frame_to_be_available_and_switch_to_it(locator))
        return self

    def switch_to_alert(self, locator, timeout=TIME_OUT, interval=INTERVAL):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=interval)
        el = wait.until(expected_conditions.alert_is_present)
        return el

    def scroll_to_bottom(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        return self

    def scroll_to(self, width, height):
        self.driver.execute_script(f'window.scrollTo({width}, {height})')
        return self

    def upload(self, locator, file):
        el = self.wait_element(locator)
        if el.tag_name == 'input':
            el.send_keys(file)
            return self
        el.click()
        pyperclip.copy(file)
        time.sleep(.2)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter', presses=2)
        return self

    def find(self, locator):
        return self.driver.find_element(*locator)

    def wait_element(self, locator, timeout=TIME_OUT, interval=INTERVAL) -> WebElement:
        used_time = 0
        while used_time < timeout:
            try:
                el = self.driver.find_element(*locator)
                return el
            except NoSuchElementException:
                time.sleep(interval)
                used_time += interval
        raise NoSuchElementException(f"can not find the element by locator:{locator}")

    def wait_visible(self, locator, timeout=TIME_OUT, interval=INTERVAL):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=interval)
        el = wait.until(expected_conditions.visibility_of_element_located(locator))
        return el

    def wait_presence(self, locator, timeout=TIME_OUT, interval=INTERVAL):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=interval)
        el = wait.until(expected_conditions.presence_of_element_located(locator))
        return el

    def wait_clickable(self, locator, timeout=TIME_OUT, interval=INTERVAL):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=interval)
        el = wait.until(expected_conditions.element_to_be_clickable(locator))
        return el

    def quit(self):
        self.driver.quit()

    def screenshot(self):
        self.driver.save_screenshot('demo.png')


def screenshot_required(f):
    def decorator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            for i in args:
                if isinstance(i, Driver):
                    i.screenshot()
            raise e
    return decorator





    

            


