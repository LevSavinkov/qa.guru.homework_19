import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_connection import AppiumConnection
from selene import browser, support

from selenium.webdriver.remote.client_config import ClientConfig

import config
from src.utils import attach

from appium import webdriver


def pytest_addoption(parser):
    parser.addoption(
        '--platformName', default='android'
    )


@pytest.fixture(scope="function")
def skip_android_test(request):
    if request.config.getoption('--platformName') == 'ios':
        pytest.skip("Этот тест для android")


@pytest.fixture(scope="function")
def skip_ios_test(request):
    if request.config.getoption('--platformName') == 'android':
        pytest.skip("Этот тест для ios")


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    client_config = ClientConfig(remote_server_addr='http://hub.browserstack.com/wd/hub')
    
    if request.config.getoption('--platformName') == 'android':
        options = UiAutomator2Options().load_capabilities({
            'platformName': 'android',
            'platformVersion': '9.0',
            'deviceName': 'Google Pixel 3',
            'app': config.app_path,
            'bstack:options': {
                'projectName': 'First Python project',
                'buildName': 'browserstack-build-1',
                'sessionName': 'BStack first_test',
                'userName': config.bstack_userName,
                'accessKey': config.bstack_accessKey,
            }
        })
    else:
        options = XCUITestOptions().load_capabilities({
            'platformName': 'ios',
            'platformVersion': '17',
            'deviceName': 'iPhone 15 Pro Max',
            'app': config.app_path,
            'bstack:options': {
                'projectName': 'First Python project',
                'buildName': 'browserstack-build-1',
                'sessionName': 'BStack first_test',
                'userName': config.bstack_userName,
                'accessKey': config.bstack_accessKey,
            }
        })
    
    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            command_executor=AppiumConnection(client_config=client_config),
            options=options
        )
    
    browser.config.timeout = config.timeout
    
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )
    
    yield
    
    attach.bstack_screenshot(browser)
    
    attach.bstack_xml(browser)
    
    session_id = browser.driver.session_id
    
    with allure.step('tear down app session'):
        browser.quit()
    
    attach.bstack_video(session_id)
