import os
import unittest

import mechanicalsoup

from src.locators import ArticlePageLocator, PersonPageLocator


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        html_file = os.getcwd() + "/tests/mocks/mock_Person.html"
        with open(html_file) as file:
            self.browser.open_fake_page(
                page_text=file.read(),
                url="https://hls-dhs-dss.ch/de/articles/000993/2015-05-07/",
            )

    def tearDown(self):
        return self.browser.close()

    def test_get_article_publish_date(self):
        expected_publish_date = "07.05.2015"
        publish_date_element = self.browser.page.find(
            *ArticlePageLocator.PUBLISH_DATE
        ).text
        publish_date = ArticlePageLocator.extract_date(publish_date_element)
        self.assertEqual(publish_date, expected_publish_date)

    def test_get_article_author(self):
        expected_author = "Daniela Pauli Falconi"
        expected_translator = "Gertraud Gamper"
        author_element = self.browser.page.find(*ArticlePageLocator.AUTHOR)

        if len(author_element.contents) == 5:
            translator = author_element.contents[4].strip()
        author = author_element.contents[2].strip()

        self.assertEqual(author, expected_author)
        self.assertEqual(translator, expected_translator)

    def test_get_person_fullname(self):
        expected_fullname = "Abbondio Bernasconi"
        given_name = self.browser.page.find(**PersonPageLocator.GIVEN_NAME).text
        family_name = self.browser.page.find(**PersonPageLocator.FAMILY_NAME).text
        self.assertEqual(f"{given_name} {family_name}", expected_fullname)

    def test_get_person_date_of_birth(self):
        expected_dob = "7.8.1757"
        dob = self.browser.page.find(*PersonPageLocator.DATE_OF_BIRTH).text
        self.assertEqual(dob, expected_dob)

    def test_get_person_date_of_death(self):
        expected_dod = "2.9.1822"
        dod = self.browser.page.find(*PersonPageLocator.DATE_OF_DEATH).text
        self.assertEqual(dod, expected_dod)

    def test_get_person_history(self):
        history = self.browser.page.find(*ArticlePageLocator.TEXT).find("p").text
        self.assertTrue(len(history) > 1)


if __name__ == "__main__":
    unittest.main()
