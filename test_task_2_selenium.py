from pytest import fail
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

path_to_chromedriver = "[PATH_TO_CHROMEDRIVER]"


class TestDataRetrieveGitHub(object):
    driver = None

    @classmethod
    def setup_method(cls):
        opts = Options()
        opts.headless = True

        cls.driver = Chrome(
            executable_path=path_to_chromedriver,
            options=opts
        )

    @classmethod
    def teardown_method(cls):
        cls.driver.quit()

    def test_ui(self):
        """
            UI-тест
        """

        self.driver.get('https://ya.ru')
        wait = WebDriverWait(self.driver, 10)

        #
        # Шаг 1. Проверить наличие элементов поиска на странице
        #

        try:
            search_input = self.driver.find_element_by_xpath("//input[@id = 'text']")
        except NoSuchElementException:
            fail("Не получилось найти поле ввода")

        assert search_input.is_displayed(), "Поле ввода невидимо"

        try:
            submit_button = self.driver.find_element_by_xpath("//button/span[text() = 'Найти']/..")
        except NoSuchElementException:
            fail("Не получилось найти кнопку 'Найти'")

        assert submit_button.is_displayed(), "Кнопка 'Найти' невидима"

        #
        # Шаг 2. Ввести текст и дождаться появления предложенных вариантов;
        #        проверить то, что набранный вариант в списке стоит первым
        #

        search_input.send_keys("Selenium")
        wait.until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'suggest2__content')]")
            )
        )

        els = self.driver.find_elements_by_xpath("//div[contains(@class, 'suggest2__content')]/li/span")
        assert len(els) == 5, "Не совпало количество предложенных элементов: %i" % len(els)
        assert els[0].text == "selenium", "Некорректное первое предложение в списке (%s)" % els[0].text

        #
        # Шаг 3. Нажать на кнопку поиска и дождаться перехода
        #

        submit_button.click()
        wait.until(lambda driver: driver.current_url.startswith("https://yandex.ru/search/?text=Selenium"))
