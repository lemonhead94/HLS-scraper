import re


class ArticlePageLocator:
    PUBLISH_DATE = ("div", {"class": "hls-article-info"})
    AUTHOR = ("div", {"class": "hls-article-text-author"})
    TEXT = ("div", {"class": "hls-article-text-unit"})

    @staticmethod
    def extract_date(text: str) -> str:
        return re.search(r"\d{2}\.\d{2}\.\d{4}", text).group()  # type: ignore
