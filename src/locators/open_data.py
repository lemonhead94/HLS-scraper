import re


class OpenDataPageLocator:
    LAST_UPLOAD_DATE = ("div", {"class": "pull-right"})

    @staticmethod
    def extract_date(text: str) -> str:
        return re.search(r"\d{2}/\d{2}/\d{4}", text).group()  # type: ignore
