import os
import unittest

import mechanicalsoup

from src.pages import Family


class TestFamily(unittest.TestCase):
    def setUp(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        html_file = os.getcwd() + "/tests/mocks/mock_Family.html"
        with open(html_file) as file:
            self.browser.open_fake_page(
                page_text=file.read(),
                url="https://hls-dhs-dss.ch/de/articles/028745/2008-12-02/",
            )
        self.family = Family(page=self.browser.page)

    def tearDown(self):
        return self.browser.close()

    def test_get_family_name(self):
        expected_family_name = "Knubel"
        family_name = self.family.get_family_name()
        self.assertEqual(family_name, expected_family_name)

    # Family Article Tests
    def test_get_article_publish_date(self):
        expected_publish_date = "02.12.2008"
        publish_date = self.family.get_publish_date()
        self.assertEqual(publish_date, expected_publish_date)

    def test_get_article_author(self):
        expected_author = "Bernard Truffer"
        author = self.family.get_author()
        self.assertEqual(author, expected_author)

    def test_get_article_text(self):
        history = self.family.get_text()
        self.assertTrue(len(history) > 1)


if __name__ == "__main__":
    unittest.main()
