from datetime import datetime

import pytest
from selenium import webdriver

import webin


@pytest.fixture()
def driver() -> webin.Driver:
    driver = webin.Driver(webdriver.Chrome())
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    timestamp = datetime.now().strftime('%H-%M-%S')

    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':

        feature_request = item.funcargs['request']

        driver = feature_request.getfuncargvalue('browser')
        driver.save_screenshot('D:/report/scr'+timestamp+'.png')

        extra.append(pytest_html.extras.image('D:/report/scr'+timestamp+'.png'))

        # always add url to report
        extra.append(pytest_html.extras.url('http://www.example.com/'))
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            extra.append(pytest_html.extras.image('D:/report/scr.png'))
            extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
        report.extra = extra
