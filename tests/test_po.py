from datetime import datetime

import pytest

from page.login import LoginPage
from webin.driver import screenshot_required






# @screenshot_required
def test_po():
    # actual = LoginPage(driver).load().login('', '').error_msg
    actual = 'f'
    expect = '请输入手号'
    assert actual == expect
