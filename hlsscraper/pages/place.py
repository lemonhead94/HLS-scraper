from bs4 import BeautifulSoup

from hlsscraper.locators import PlacePageLocator
from hlsscraper.pages import Article


class Place(Article):
    def __init__(self, page: BeautifulSoup):
        self.page = page

    def get_place_name(self) -> str:
        place_name = self.page.find(*PlacePageLocator.NAME)
        if place_name is None:
            raise ValueError("Place name not found")
        return str(place_name.text)
