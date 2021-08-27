import requests
from bs4 import BeautifulSoup
import string

"""Scrapes for news articles on 3rd page of nature.com website and saves content of the articles to .txt files."""




def get_response(url: str, params: dict = None) -> requests.Response:
    """Takes url and optionally parameters (dict) as arguments and returns response object. 
    English version of the page is enforced."""
    if params is None:
        params = {}
    return requests.get(url, params=params, headers={"Accept-Language": "en-US,en;q=0.5"})


def extract_news(response: requests.Response):
    """Extracts hrefs to News articles and their titles. Returns list of hrefs and list of titles."""
    if response:
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("article")
        hrefs = []
        titles = []
        for article in articles:
            article_type = article.find("span", {"class": "c-meta__type"}).text
            if article_type == "News":
                article = article.find("a", {"data-track-action": "view article"})
                titles.append(article.text)
                hrefs.append(article.get("href"))
        return hrefs, titles


def extract_content(href):
    """Extracts the text of the article."""
    local_article_text = ""
    local_soup = BeautifulSoup(requests.get("http://nature.com" + href).content, "html.parser")
    section = local_soup.find("div", {"class": "c-article-body u-clearfix"})
    paragraphs = section.find_all(["p", "h2", "h3", "h4"])
    unwanted = section.find_all("p", {"class": "recommended__title u-serif"})
    for u in unwanted:
        u.extract()     # Removes href to other articles from paragraphs
    for p in paragraphs:
        local_article_text += p.text
    return local_article_text


def save_content(article_title, content):
    """Saves the text of the article to .txt file."""
    t_stripped = article_title.translate(str.maketrans('', '', string.punctuation))
    t_under = t_stripped.replace(" ", "_")
    filename = t_under+".txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename


if __name__ == "__main__":
    saved_articles = []
    r = get_response("https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3")
    if r:
        news_hrefs, titles = extract_news(r)
        for news, title in zip(news_hrefs, titles):
            article_text = extract_content(news)
            saved_articles.append(save_content(title, article_text))
        print("Saved articles:", saved_articles)
    else:
        print(f"The URL returned {r.status_code}!")
