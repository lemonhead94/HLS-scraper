import os
import unittest

import mechanicalsoup

from src.pages import Person


class TestPerson5(unittest.TestCase):
    def setUp(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        html_file = os.getcwd() + "/tests/mocks/mock_Person_7.html"
        with open(html_file) as file:
            self.browser.open_fake_page(
                page_text=file.read(),
                url="https://hls-dhs-dss.ch/de/articles/033519/2004-06-22/",
            )
        self.person = Person(page=self.browser.page)

    def tearDown(self):
        return self.browser.close()

    def test_get_person_fullname(self):
        expected_fullname = "Henri Gendre"
        full_name = self.person.get_fullname()
        self.assertEqual(full_name, expected_fullname)

    def test_get_person_first_name(self):
        expected_first_name = "Henri"
        first_name = self.person.get_first_name()
        self.assertEqual(first_name, expected_first_name)

    def test_get_person_last_name(self):
        expected_last_name = "Gendre"
        last_name = self.person.get_last_name()
        self.assertEqual(last_name, expected_last_name)

    def test_get_person_date_of_birth(self):
        expected_dob = "15.8.1900"
        dob = self.person.get_date_of_birth()
        self.assertEqual(dob, expected_dob)

    def test_get_person_date_of_death(self):
        expected_dod = "13.2.1981"
        dod = self.person.get_date_of_death()
        self.assertEqual(dod, expected_dod)

    # Person Article Tests
    def test_get_article_publish_date(self):
        expected_publish_date = "22.06.2004"
        publish_date = self.person.get_publish_date()
        self.assertEqual(publish_date, expected_publish_date)

    def test_get_article_author(self):
        expected_author = "Marianne Rolle"
        author = self.person.get_author()
        self.assertEqual(author, expected_author)

    def test_get_article_translator(self):
        expected_translator = "Sabine Kraut"
        translator = self.person.get_translator()
        self.assertEqual(translator, expected_translator)

    def test_get_article_text(self):
        history = self.person.get_text()
        self.assertTrue(len(history) > 1)


if __name__ == "__main__":
    unittest.main()
