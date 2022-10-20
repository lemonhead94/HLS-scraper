import re

from bs4 import BeautifulSoup

from src.locators import PersonPageLocator
from src.pages import Article


class Person(Article):
    def __init__(self, page: BeautifulSoup):
        self.page = page

    def get_fullname(self) -> str:
        """returns the full name of a person"""
        return f"{self.get_first_name()} {self.get_last_name()}"

    def get_first_name(self) -> str:
        """returns the first name of a person"""
        given_name = self.page.find(**PersonPageLocator.GIVEN_NAME)
        return str(given_name.text) if given_name else ""

    def get_last_name(self) -> str:
        """returns the last name of a person"""
        family_name = self.page.find(**PersonPageLocator.FAMILY_NAME)
        if family_name is None:
            raise ValueError("Given Name not found")
        return str(family_name.text)

    def get_date_of_birth(self) -> str:
        """returns the date of birth of a person"""
        dob = self.page.find(*PersonPageLocator.DATE_OF_BIRTH)
        dob2 = self.page.find(*PersonPageLocator.DATE_OF_BIRTH_2)
        first_mentioning = self.page.find(*PersonPageLocator.FIRST_MENTION_BIRTH)

        if dob is None and dob2 is None and first_mentioning is None:
            return self._get_no_dates_specified(is_birth_date=True)

        if dob:
            return str(dob.text)
        elif dob2:
            return str(dob2.text)
        else:
            return str(first_mentioning.text)

    def get_date_of_death(self) -> str:
        """returns the date of death of a person"""
        dod = self.page.find(*PersonPageLocator.DATE_OF_DEATH)
        last_mentioning = self.page.find(*PersonPageLocator.LAST_MENTION_DEATH)

        if dod is None and last_mentioning is None:
            return self._get_no_dates_specified(is_birth_date=False)

        if dod:
            return str(dod.text)
        else:
            return str(last_mentioning.text)

    def _get_no_dates_specified(self, is_birth_date: bool) -> str:
        """returns the text if no dates are specified"""
        no_dates = self.page.find_all(*PersonPageLocator.NO_DATES_SPECIFIED)
        search = None
        if len(no_dates) > 0:
            text = no_dates[-1].text.replace("\n", "").strip()
            if is_birth_date:
                search = re.search(r"Ersterwähnung(.*?)Letzterwähnung", text)
            else:
                search = re.search(r"Letzterwähnung(.*?)$", text)

        if search:
            return search.group(1).strip()
        else:
            return ""
