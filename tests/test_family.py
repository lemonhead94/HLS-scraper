import os
import unittest

import mechanicalsoup

from src.locators import FamilyPageLocator
from src.pages import Article


class TestFamily(unittest.TestCase):
    def setUp(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        html_file = os.getcwd() + "/tests/mocks/mock_Family.html"
        with open(html_file) as file:
            self.browser.open_fake_page(
                page_text=file.read(),
                url="https://hls-dhs-dss.ch/de/articles/028745/2008-12-02/",
            )
        self.article = Article(page=self.browser.page)

    def tearDown(self):
        return self.browser.close()

    def test_get_family_name(self):
        expected_family_name = "Knubel"
        family_name = self.browser.page.find(*FamilyPageLocator.NAME).text
        self.assertEqual(family_name, expected_family_name)

    # Article Tests
    def test_get_article_publish_date(self):
        expected_publish_date = "02.12.2008"
        publish_date = self.article.get_publish_date()
        self.assertEqual(publish_date, expected_publish_date)

    def test_get_article_author(self):
        expected_author = "Bernard Truffer"
        author = self.article.get_author()
        self.assertEqual(author, expected_author)

    def test_get_article_text(self):
        history = self.article.get_text()
        self.assertTrue(len(history) > 1)


if __name__ == "__main__":
    unittest.main()
