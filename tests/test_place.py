import os
import unittest

import mechanicalsoup

from src.locators import PlacePageLocator
from src.pages import Article


class TestPlace(unittest.TestCase):
    def setUp(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        html_file = os.getcwd() + "/tests/mocks/mock_Place.html"
        with open(html_file) as file:
            self.browser.open_fake_page(
                page_text=file.read(),
                url="https://hls-dhs-dss.ch/de/articles/000190/2016-09-15/",
            )
        self.article = Article(page=self.browser.page)

    def tearDown(self):
        return self.browser.close()

    def test_get_place_name(self):
        expected_place_name = "Gutenburg"
        place_name = self.browser.page.find(*PlacePageLocator.NAME).text
        self.assertEqual(place_name, expected_place_name)

    # Article Tests
    def test_get_article_publish_date(self):
        expected_publish_date = "15.09.2016"
        publish_date = self.article.get_publish_date()
        self.assertEqual(publish_date, expected_publish_date)

    def test_get_article_author(self):
        expected_author = "Anne-Marie Dubler"
        author = self.article.get_author()
        self.assertEqual(author, expected_author)

    def test_get_place_history(self):
        history = self.article.get_text()
        self.assertTrue(len(history) > 1)


if __name__ == "__main__":
    unittest.main()
