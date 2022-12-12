from datetime import datetime

from bs4 import BeautifulSoup

from hlsscraper.locators import OpenDataPageLocator


class OpenData:

    base_url = "https://hls-dhs-dss.ch"

    def __init__(self, page: BeautifulSoup):
        self.page = page

    def get_last_upload_date(self) -> datetime:
        upload_date = self.page.find(*OpenDataPageLocator.LAST_UPLOAD_DATE)
        if upload_date is None:
            raise ValueError("last upload date not found")
        return OpenDataPageLocator.extract_date(upload_date.text)

    def get_person_csv_url(self) -> str:
        csv_url = self.page.find(*OpenDataPageLocator.DE_PERSON_CSV_URL)
        if csv_url is None:
            raise ValueError("person csv url not found")
        return f"{self.base_url}{csv_url['href']}"

    def get_place_csv_url(self) -> str:
        csv_url = self.page.find(*OpenDataPageLocator.DE_PLACE_CSV_URL)
        if csv_url is None:
            raise ValueError("place csv url not found")
        return f"{self.base_url}{csv_url['href']}"

    def get_family_csv_url(self) -> str:
        csv_url = self.page.find(*OpenDataPageLocator.DE_FAMILY_CSV_URL)
        if csv_url is None:
            raise ValueError("family csv url not found")
        return f"{self.base_url}{csv_url['href']}"
