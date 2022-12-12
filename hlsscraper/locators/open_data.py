import re
from datetime import datetime


class OpenDataPageLocator:
    LAST_UPLOAD_DATE = ("div", {"class": "pull-right"})
    DE_PERSON_CSV_URL = (
        "a",
        {"href": re.compile(r".*liste_bio_d_utf8\.csv")},
    )
    DE_PLACE_CSV_URL = (
        "a",
        {"href": re.compile(r".*liste_geo_d_utf8\.csv")},
    )
    DE_FAMILY_CSV_URL = (
        "a",
        {"href": re.compile(r".*liste_fam_d_utf8\.csv")},
    )

    @staticmethod
    def extract_date(text: str) -> datetime:
        date = re.search(r"\d{2}/\d{2}/\d{4}", text).group()  # type: ignore
        return datetime.strptime(date, "%d/%m/%Y")
