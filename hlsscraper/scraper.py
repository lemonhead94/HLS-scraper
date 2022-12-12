import time
from csv import writer
from datetime import datetime
from typing import Any, List
from urllib.request import Request, urlopen

import mechanicalsoup
import pandas as pd

from hlsscraper.pages import OpenData, Person
from hlsscraper.pages.logging_utils import log_exception, setup_logging_to_file

COLUMN_NAMES = [
    "HLS_ID",
    "HLS_URL",
    "first_name",
    "last_name",
    "birth_date",
    "death_date",
    "text",
    "published",
    "author",
    "translator",
]


def __get_dataframe_from_csv(url: str) -> pd.DataFrame:
    req = Request(url)
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
    )
    content = urlopen(req)
    return pd.read_csv(content)


def __append_list_as_row(file_name: str, list_of_elem: List[Any]) -> None:
    with open(file_name, "a+", newline="") as write_obj:
        csv_writer = writer(write_obj, delimiter=";")
        csv_writer.writerow(list_of_elem)


def __add_hls_record_to_df(
    df: pd.DataFrame,
    hls_id: str,
    hls_url: str,
    first_name: str,
    last_name: str,
    birth_date: str,
    death_date: str,
    text: str,
    published: str,
    author: str,
    translator: str,
) -> None:
    """Adds a HLS record to a pandas dataframe."""
    # add new row to existing dataframe
    df.loc[len(df)] = [
        hls_id,
        hls_url,
        first_name,
        last_name,
        birth_date,
        death_date,
        text,
        published,
        author,
        translator,
    ]


def __get_update_hls_records(
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


def __get_new_hls_records(
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


def scrape(
    base_csv_path: str,
    update_csv_path: str,
    new_csv_path: str,
    last_scraping: str,
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

        df_hls_bio = __get_dataframe_from_csv(open_data_page.get_person_csv_url())
        df_base = pd.read_csv(base_csv_path, sep=";")

        # update existing person records in scraper csv
        df_update_hls_records = __get_update_hls_records(df_hls_bio, df_base)
        df_updates = pd.DataFrame(columns=COLUMN_NAMES)
        index = 1
        for _, row in df_update_hls_records.iterrows():
            time.sleep(crawl_delay)
            print(
                f"Updating {str(index).zfill(len(str(len(df_update_hls_records))))} out of {len(df_update_hls_records)} | ID: {str(row.ID).zfill(5)} | URL: {row.URL}"
            )
            index += 1
            browser.open(row.URL)
            person_page = Person(page=browser.page)

            first_name = person_page.get_first_name()
            last_name = person_page.get_last_name()
            birth_date = person_page.get_date_of_birth()
            death_date = person_page.get_date_of_death()
            text = person_page.get_text()
            published = person_page.get_publish_date()
            author = person_page.get_author()
            translator = person_page.get_translator()

            # update the new records dataframe
            __add_hls_record_to_df(
                df=df_updates,
                hls_id=row.ID,
                hls_url=row.URL,
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                death_date=death_date,
                text=text,
                published=published,
                author=author,
                translator=translator,
            )

            # update the base dataframe
            df_base.loc[df_base.HLS_ID == row.ID, "HLS_URL"] = row.URL
            df_base.loc[df_base.HLS_ID == row.ID, "first_name"] = first_name
            df_base.loc[df_base.HLS_ID == row.ID, "last_name"] = last_name
            df_base.loc[df_base.HLS_ID == row.ID, "birth_date"] = birth_date
            df_base.loc[df_base.HLS_ID == row.ID, "death_date"] = death_date
            df_base.loc[df_base.HLS_ID == row.ID, "text"] = text
            df_base.loc[df_base.HLS_ID == row.ID, "published"] = published
            df_base.loc[df_base.HLS_ID == row.ID, "author"] = author
            df_base.loc[df_base.HLS_ID == row.ID, "translator"] = translator

        # overwrite existing scraper csv
        df_base.to_csv(base_csv_path, sep=";", index=False)

        # add new person records to scraper csv
        df_new_hls_records = __get_new_hls_records(df_hls_bio, df_base)
        df_new_records = pd.DataFrame(columns=COLUMN_NAMES)
        index = 1
        for _, row in df_new_hls_records.iterrows():
            time.sleep(crawl_delay)
            print(
                f"Adding   {str(index).zfill(len(str(len(df_new_hls_records))))} out of {len(df_new_hls_records)} | ID: {str(row.ID).zfill(5)} | URL: {row.URL}"
            )
            index += 1
            browser.open(row.URL)
            person_page = Person(page=browser.page)

            first_name = person_page.get_first_name()
            last_name = person_page.get_last_name()
            birth_date = person_page.get_date_of_birth()
            death_date = person_page.get_date_of_death()
            text = person_page.get_text()
            published = person_page.get_publish_date()
            author = person_page.get_author()
            translator = person_page.get_translator()

            # update the new records dataframe
            __add_hls_record_to_df(
                df=df_new_records,
                hls_id=row.ID,
                hls_url=row.URL,
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                death_date=death_date,
                text=text,
                published=published,
                author=author,
                translator=translator,
            )

            # fetch data from person page
            __append_list_as_row(
                file_name=base_csv_path,
                list_of_elem=[
                    row.ID,
                    row.URL,
                    first_name,
                    last_name,
                    birth_date,
                    death_date,
                    text,
                    published,
                    author,
                    translator,
                ],
            )

        # write new and updated records to csv
        df_updates.to_csv(update_csv_path, sep=";", index=False)
        df_new_records.to_csv(new_csv_path, sep=";", index=False)

    except Exception as e:
        log_exception(e)
    finally:
        browser.close()
