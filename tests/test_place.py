import os
import re
import unittest

import mechanicalsoup


class TestPlace(unittest.TestCase):
    def setUp(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        html_file = os.getcwd() + "/tests/mocks/mock_Place.html"
        with open(html_file) as file:
            self.browser.open_fake_page(
                page_text=file.read(),
                url="https://hls-dhs-dss.ch/de/articles/000190/2016-09-15/",
            )

    def tearDown(self):
        return self.browser.close()

    def test_get_article_publish_date(self):
        expected_publish_date = "15.09.2016"
        publish_date_element = self.browser.page.find(
            "div", {"class": "hls-article-info"}
        ).text
        publish_date = re.search(r"\d{2}\.\d{2}\.\d{4}", publish_date_element).group()  # type: ignore
        self.assertEqual(publish_date, expected_publish_date)

    def test_get_article_author(self):
        expected_author = "Anne-Marie Dubler"
        author_element = self.browser.page.find(
            "div", {"class": "hls-article-text-author"}
        )

        author = author_element.contents[2].strip()

        self.assertEqual(author, expected_author)

    def test_get_place_name(self):
        expected_place_name = "Gutenburg"
        place_name = self.browser.page.find("span", {"class": "hls-lemma"}).text
        self.assertEqual(place_name, expected_place_name)

    def test_get_place_history(self):
        history = (
            self.browser.page.find("div", {"class": "hls-article-text-unit"})
            .find("p")
            .text
        )
        self.assertTrue(len(history) > 1)


if __name__ == "__main__":
    unittest.main()
