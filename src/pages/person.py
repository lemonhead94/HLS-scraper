from bs4 import BeautifulSoup

from src.locators import PersonPageLocator
from src.pages import Article


class Person(Article):
    def __init__(self, page: BeautifulSoup):
        self.page = page

    def get_fullname(self) -> str:
        """returns the full name of a person"""
        given_name = self.page.find(**PersonPageLocator.GIVEN_NAME).text
        family_name = self.page.find(**PersonPageLocator.FAMILY_NAME).text
        if given_name is None:
            raise ValueError("Given Name not found")
        if family_name is None:
            raise ValueError("Given Name not found")

        return f"{given_name} {family_name}"

    def get_date_of_birth(self) -> str:
        """returns the date of birth of a person"""
        dob = self.page.find(*PersonPageLocator.DATE_OF_BIRTH)
        if dob is None:
            raise ValueError("Date of Birth not found")
        return str(dob.text)

    def get_date_of_death(self) -> str:
        """returns the date of death of a person"""
        dod = self.page.find(*PersonPageLocator.DATE_OF_DEATH)
        if dod is None:
            raise ValueError("Date of Death not found")
        return str(dod.text)
