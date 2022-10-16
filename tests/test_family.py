import os
import re
import unittest

import mechanicalsoup


class TestFamily(unittest.TestCase):
    def setUp(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        html_file = os.getcwd() + "/tests/mocks/mock_Family.html"
        with open(html_file) as file:
            self.browser.open_fake_page(
                page_text=file.read(),
                url="https://hls-dhs-dss.ch/de/articles/028745/2008-12-02/",
            )

    def tearDown(self):
        return self.browser.close()

    def test_get_article_publish_date(self):
        expected_publish_date = "02.12.2008"
        publish_date_element = self.browser.page.find(
            "div", {"class": "hls-article-info"}
        ).text
        publish_date = re.search(r"\d{2}\.\d{2}\.\d{4}", publish_date_element).group()  # type: ignore
        self.assertEqual(publish_date, expected_publish_date)

    def test_get_article_author(self):
        expected_author = "Bernard Truffer"
        author_element = self.browser.page.find(
            "div", {"class": "hls-article-text-author"}
        )

        author = author_element.contents[2].strip()

        self.assertEqual(author, expected_author)

    def test_get_family_name(self):
        expected_family_name = "Knubel"
        family_name = self.browser.page.find("span", {"class": "hls-lemma"}).text
        self.assertEqual(family_name, expected_family_name)

    def test_get_family_history(self):
        history = (
            self.browser.page.find("div", {"class": "hls-article-text-unit"})
            .find("p")
            .text
        )
        self.assertTrue(len(history) > 1)


if __name__ == "__main__":
    unittest.main()
