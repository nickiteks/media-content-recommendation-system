from django.test import TestCase
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver


# Create your tests here.
class SystemTest(LiveServerTestCase):

    def test_auth(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        selenium = webdriver.Chrome('C://Users//NULS//PycharmProjects//media-content-recommendation-system//RSApp'
                                    '//static//chromedriver.exe',
                                    options=options)
        selenium.get("http://127.0.0.1:8000/")

        selenium.find_element_by_xpath('//a[contains(@href,"/login/")]').click()

        input_username = selenium.find_element(by='name', value="username")
        input_password = selenium.find_element(by='name', value="password")

        input_username.send_keys("admin")
        input_password.send_keys('1111')

        selenium.find_element(value="Login").click()

        assert 'Привет, admin' in selenium.page_source

    # def test_game(self):
    #     options = webdriver.ChromeOptions()
    #     options.add_argument('--kiosk')
    #     selenium = webdriver.Chrome('C://Users//NULS//PycharmProjects//media-content-recommendation-system//RSApp'
    #                                 '//static//chromedriver.exe',
    #                                 options=options)
    #     selenium.get("http://127.0.0.1:8000/")
    #     selenium.find_element_by_xpath('//a[contains(@href,"/game_page/")]').click()
    #
    #     input_game = selenium.find_element(value='select')
    #     input_game.send_keys("Devil May Cry 5")
    #
    #     selenium.find_element(value='game').click()
    #
    #     assert 'God of War: Ascension' in selenium.page_source