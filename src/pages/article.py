from bs4 import BeautifulSoup

from src.locators import ArticlePageLocator


class Article:
    def __init__(self, page: BeautifulSoup):
        self.page = page

    def get_author(self) -> str:
        """returns the author of the article"""
        author_element = self.page.find(*ArticlePageLocator.AUTHOR)
        if author_element is None or len(author_element.contents) < 3:
            raise ValueError("Author not found")
        return str(author_element.contents[2].strip())

    def get_translator(self) -> str:
        """returns the translator of the article"""
        author_element = self.page.find(*ArticlePageLocator.AUTHOR)
        if author_element is None or len(author_element.contents) < 5:
            return ""
        return str(author_element.contents[4].strip())

    def get_publish_date(self) -> str:
        """returns the publication date of the article"""
        publish_date_element = self.page.find(*ArticlePageLocator.PUBLISH_DATE)
        if publish_date_element is None:
            raise ValueError("Publish Date not found")
        return str(ArticlePageLocator.extract_date(publish_date_element.text))

    def get_text(self) -> str:
        """returns the text of the article"""
        article_text = self.page.find(*ArticlePageLocator.TEXT).find("p")
        if article_text is None:
            raise ValueError("Text Content not found")
        return str(article_text.text)
