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


class ResidentialAdvertScraper(BaseScraper):
    def _get_location(self) -> tuple:
        location = self.driver.find_element(
            By.CSS_SELECTOR, "h2[itemprop='address']"
        ).text
        return tuple(location.split(", ", 1))

    def _get_description(self) -> str:
        try:
            description = self.driver.find_element(
                By.CSS_SELECTOR,
                "div.property-description > div[itemprop='description']"
            ).text
        except NoSuchElementException:
            description = "No description"

        return description

    def _get_price(self) -> str:
        return self.driver.find_element(
            By.CLASS_NAME, "price"
        ).text

    def _get_area(self) -> str:
        return self.driver.find_element(
            By.CLASS_NAME, "carac-value"
        ).text

    def _get_rooms_amount(self, css_class: str) -> str | int:
        try:
            rooms_str = self.driver.find_element(
                By.CLASS_NAME, css_class
            ).text
            rooms = int(rooms_str.split()[0])
        except NoSuchElementException:
            rooms = "No data"

        return rooms

    def _get_bathrooms_amount(self) -> str | int:
        return self._get_rooms_amount("sdb")

    def _get_bedrooms_amount(self) -> str | int:
        return self._get_rooms_amount("cac")

    def get_photo_links(self, amount: int) -> list:
        photo_links = []

        for _ in range(amount):
            image = self.driver.find_element(By.CSS_SELECTOR, "div.image-wrapper img")
            source = image.get_attribute("src")
            photo_links.append(source)

            photo = self.driver.find_element(
                By.CSS_SELECTOR, "img#fullImg"
            )
            photo.click()

        return photo_links

    def _get_image_data(self) -> list | None:
        img = self.driver.find_element(
            By.CSS_SELECTOR, "div.primary-photo-container"
        )
        ActionChains(self.driver).move_to_element(img).click(img).perform()

        try:
            amount_obj = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.image-wrapper > div.description")
                )
            )
            amount = int(amount_obj.text.split("/")[1])
            return self.get_photo_links(amount)
        except TimeoutException:
            return None

    def scrape_advert(self, url: str) -> dict:
        self.driver.get(url)

        title = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span[data-id='PageTitle']")
            )
        ).text

        region, address = self._get_location()
        description = self._get_description()
        bathrooms = self._get_bathrooms_amount()
        bedrooms = self._get_bedrooms_amount()
        area = self._get_area()
        price = self._get_price()
        image_links = self._get_image_data()

        return {
            "url": url,
            "title": title,
            "region": region,
            "address": address,
            "description": description,
            "rooms": {
                "bathrooms": bathrooms,
                "bedrooms": bedrooms
            },
            "area": area,
            "price": price,
            "images": image_links
        }
