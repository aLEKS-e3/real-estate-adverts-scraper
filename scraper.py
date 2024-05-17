import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseScraper:
    def __init__(self) -> None:
        self.options = Options()
        self.driver = webdriver.Chrome(options=self._modify_options())

    def _modify_options(self) -> Options:
        self.options.add_argument("--headless=new")
        self.options.add_argument(
            "user-agent='MQQBrowser/26 Mozilla/5.0 "
            "(Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; "
            "CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) "
            "Version/4.0 Mobile Safari/533.1'"
        )
        return self.options

class ResidentialThumbnailScraper(BaseScraper):
    def _next_page(self):
        next_button = self.driver.find_element(
            By.CSS_SELECTOR, "li.next > a"
        )
        if next_button.is_displayed():
            next_button.click()
            time.sleep(0.25)

    @staticmethod
    def get_detail_url(thumbnail: WebElement) -> str:
        link = WebDriverWait(thumbnail, 1).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "a-more-detail")
            )
        )
        return link.get_attribute("href")

    def scrape_properties(self, url: str, amount: int) -> list:
        self.driver.get(url)
        detail_links = []

        while True:
            thumbnails = self.driver.find_elements(
                By.CLASS_NAME, "property-thumbnail-item"
            )
            links = [
                self.get_detail_url(thumbnail)
                for thumbnail in thumbnails
            ]
            detail_links.extend(links)

            if len(detail_links) >= amount:
                break

            self._next_page()

        return detail_links[:amount]
