import os
import unittest
from datetime import datetime

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
        expected_upload_date = datetime(2022, 10, 10)
        upload_date = self.open_data.get_last_upload_date()
        self.assertEqual(upload_date, expected_upload_date)

    def test_get_person_csv_url(self):
        expected_csv_url = "https://hls-dhs-dss.ch/download/OpenDataFiles/WebHome/liste_bio_d_utf8.csv?rev=1.35"
        csv_url = self.open_data.get_person_csv_url()
        self.assertEqual(csv_url, expected_csv_url)

    def test_get_place_csv_url(self):
        expected_csv_url = "https://hls-dhs-dss.ch/download/OpenDataFiles/WebHome/liste_geo_d_utf8.csv?rev=1.35"
        csv_url = self.open_data.get_place_csv_url()
        self.assertEqual(csv_url, expected_csv_url)

    def test_get_family_csv_url(self):
        expected_csv_url = "https://hls-dhs-dss.ch/download/OpenDataFiles/WebHome/liste_fam_d_utf8.csv?rev=1.35"
        csv_url = self.open_data.get_family_csv_url()
        self.assertEqual(csv_url, expected_csv_url)


if __name__ == "__main__":
    unittest.main()
