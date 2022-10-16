from bs4 import BeautifulSoup

from src.locators import OpenDataPageLocator


class OpenData:
    def __init__(self, page: BeautifulSoup):
        self.page = page

    def get_last_upload_date(self) -> str:
        upload_date = self.page.find(*OpenDataPageLocator.LAST_UPLOAD_DATE)
        if upload_date is None:
            raise ValueError("last upload date not found")
        return str(OpenDataPageLocator.extract_date(upload_date.text))
