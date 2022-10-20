# import sys
import time
from csv import writer
from datetime import datetime
from typing import Any, List
from urllib.request import Request, urlopen

import mechanicalsoup
import pandas as pd

from src.pages import OpenData, Person
from src.pages.logging_utils import log_exception, setup_logging_to_file


def get_dataframe_from_csv(url: str) -> pd.DataFrame:
    req = Request(url)
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
    )
    content = urlopen(req)
    return pd.read_csv(content)


def append_list_as_row(file_name: str, list_of_elem: List[Any]) -> None:
    with open(file_name, "a+", newline="") as write_obj:
        csv_writer = writer(write_obj, delimiter=";")
        csv_writer.writerow(list_of_elem)


def get_update_hls_records(
    hls_records: pd.DataFrame, scraped_data: pd.DataFrame
) -> pd.DataFrame:
    """Returns a list of records that need to be updated in the scraper csv."""
    df_merged = pd.merge(
        hls_records,
        scraped_data,
        how="right",
        left_on="ID",
        right_on="HLS_ID",
    )
    return df_merged[df_merged.HLS_URL != df_merged.URL]


def get_new_hls_records(
    hls_records: pd.DataFrame, scraped_data: pd.DataFrame
) -> pd.DataFrame:
    """Returns a list of new records that need to be scraped and added to the scraper csv."""
    df_merged = pd.merge(
        hls_records,
        scraped_data,
        how="left",
        left_on="ID",
        right_on="HLS_ID",
    )
    return df_merged[df_merged.HLS_URL != df_merged.URL]


def main(
    last_scraping: str,
    scraper_csv_path: str,
    crawl_delay: int = 20,
) -> None:
    try:
        last_scraping_date = datetime.strptime(last_scraping, "%d.%m.%Y")
        setup_logging_to_file("scraper.log")
        browser = mechanicalsoup.StatefulBrowser()
        browser.open("https://hls-dhs-dss.ch/de/opendata")

        open_data_page = OpenData(page=browser.page)
        last_hls_update = open_data_page.get_last_upload_date()
        # early exit if there is nothing new to scrape
        if last_scraping_date >= last_hls_update:
            exit

        df_hls_bio = get_dataframe_from_csv(open_data_page.get_person_csv_url())
        df_hls_scrape = pd.read_csv(scraper_csv_path, sep=";")

        # update existing person records in scraper csv
        df_update_hls_records = get_update_hls_records(df_hls_bio, df_hls_scrape)
        for index, row in df_update_hls_records.iterrows():
            time.sleep(crawl_delay)
            print(
                f"Updating existing persons {index} out of {df_update_hls_records.shape[0]} | ID: {row.ID} | URL: {row.URL}"
            )
            browser.open(row.URL)
            person_page = Person(page=browser.page)
            df_hls_scrape.loc[df_hls_scrape.HLS_ID == row.ID, "HLS_URL"] = row.URL
            df_hls_scrape.loc[
                df_hls_scrape.HLS_ID == row.ID, "first_name"
            ] = person_page.get_first_name()
            df_hls_scrape.loc[
                df_hls_scrape.HLS_ID == row.ID, "last_name"
            ] = person_page.get_last_name()
            df_hls_scrape.loc[
                df_hls_scrape.HLS_ID == row.ID, "birth_date"
            ] = person_page.get_date_of_birth()
            df_hls_scrape.loc[
                df_hls_scrape.HLS_ID == row.ID, "death_date"
            ] = person_page.get_date_of_death()
            df_hls_scrape.loc[
                df_hls_scrape.HLS_ID == row.ID, "text"
            ] = person_page.get_text()
            df_hls_scrape.loc[
                df_hls_scrape.HLS_ID == row.ID, "published"
            ] = person_page.get_publish_date()
            df_hls_scrape.loc[
                df_hls_scrape.HLS_ID == row.ID, "author"
            ] = person_page.get_author()
            df_hls_scrape.loc[
                df_hls_scrape.HLS_ID == row.ID, "translator"
            ] = person_page.get_translator()

        # overwrite existing scraper csv
        df_hls_scrape.to_csv(scraper_csv_path, sep=";", index=False)

        # add new person records to scraper csv
        df_new_hls_records = get_new_hls_records(df_hls_bio, df_hls_scrape)
        for index, row in df_new_hls_records.iterrows():
            time.sleep(crawl_delay)
            print(
                f"Adding new person records {index} out of {df_new_hls_records.shape[0]} | ID: {row.ID} | URL: {row.URL}"
            )
            browser.open(row.URL)
            person_page = Person(page=browser.page)

            # fetch data from person page
            append_list_as_row(
                file_name=scraper_csv_path,
                list_of_elem=[
                    row.ID,
                    row.URL,
                    person_page.get_first_name(),
                    person_page.get_last_name(),
                    person_page.get_date_of_birth(),
                    person_page.get_date_of_death(),
                    person_page.get_text(),
                    person_page.get_publish_date(),
                    person_page.get_author(),
                    person_page.get_translator(),
                ],
            )

    except Exception as e:
        log_exception(e)
    finally:
        browser.close()


if __name__ == "__main__":
    # main(sys.argv[1:])
    main(last_scraping="15.10.2022", crawl_delay=20, scraper_csv_path="hls_people.csv")
