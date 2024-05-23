from file_manager import write_to_json
from scraper import ResidentialThumbnailScraper, ResidentialAdvertScraper

from constants import  BASE_URL, ADVERTS_AMOUNT, JSON_NAME


def main(url: str, adverts_amount: int) -> list[dict]:
    thumbnail_scraper = ResidentialThumbnailScraper()
    detail_links = thumbnail_scraper.scrape_properties(url, adverts_amount)

    property_scraper = ResidentialAdvertScraper()
    details = [
        property_scraper.scrape_advert(link)
        for link in detail_links
    ]

    return details


if __name__ == "__main__":
    data = main(BASE_URL, ADVERTS_AMOUNT)
    write_to_json(FILE, data)
