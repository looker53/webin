from collections import namedtuple

from selenium.webdriver.remote.webelement import WebElement

from webin.driver import Driver

_locator_by = {
    'id': 'id',
    'xpath': 'xpath',
    'name': 'name',
    'class_': 'class name',
    'css': 'css selector',
    'tag': 'tag name'
}


class UiElement:
    def __init__(self, desc='', **locator):
        self.loaded = False
        self.locator = locator
        self.el: WebElement = None
        self.desc = desc

    def __get__(self, instance: Driver, owner):
        if len(self.locator) != 1:
            raise ValueError('use one locator')
        if next(iter(self.locator)) not in _locator_by:
            raise ValueError('locator must be one of id, name, css, xpath, class_, tag')
        by, value = next(iter(self.locator.items()))
        locator = (_locator_by.get(by), value)
        el = instance.driver.wait_element(locator)
        self.loaded = True
        self.el = el
        return self

    def __set__(self, instance, value):
        pass

    def click(self):
        if self.el.is_enabled():
            self.el.click()
        return self

    @property
    def text(self):
        return self.el.text


class Input(UiElement):
    def fill(self, words):
        self.el.send_keys(words)
        return self


class Button(UiElement):
    pass


class Div(UiElement):
    pass
