from allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have


def test_fill_email(skip_ios_test):
    with step('Fill email to input'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Text Button')).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Text Input')).type("hello@browserstack.com").press_enter()
    
    with step('Check filled email from output'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Text Output')).should(have.text("hello@browserstack.com"))
