from bs4 import BeautifulSoup

from hlsscraper.locators import FamilyPageLocator
from hlsscraper.pages import Article


class Family(Article):
    def __init__(self, page: BeautifulSoup):
        self.page = page

    def get_family_name(self) -> str:
        """returns the given name of a family"""
        family_name = self.page.find(*FamilyPageLocator.FAMILY_NAME)
        if family_name is None:
            raise ValueError("Family / Given Name not found")
        return str(family_name.text)
