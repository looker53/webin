import pytest
import webin
from selenium import webdriver


def test_find_element(driver):
    driver.goto('http://www.baidu.com')
    el = driver.find(('id', 'kw'))
    assert el

def test_wait_element(driver):
    driver.goto('http://www.baidu.com')
    el = driver.wait_element(('id', 'kw'))
    assert el



    


