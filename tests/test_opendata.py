import os
import unittest

import mechanicalsoup

from src.pages import OpenData


class TestOpenData(unittest.TestCase):
    def setUp(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        html_file = os.getcwd() + "/tests/mocks/mock_OpenData.html"
        with open(html_file) as file:
            self.browser.open_fake_page(
                page_text=file.read(),
                url="https://hls-dhs-dss.ch/de/opendata",
            )
        self.open_data = OpenData(page=self.browser.page)

    def tearDown(self):
        return self.browser.close()

    def test_get_last_upload_date(self):
        expected_upload_date = "10/10/2022"
        upload_date = self.open_data.get_last_upload_date()
        self.assertEqual(upload_date, expected_upload_date)


if __name__ == "__main__":
    unittest.main()
