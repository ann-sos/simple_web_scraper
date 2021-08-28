import requests
from bs4 import BeautifulSoup
import string
import os

"""Scrapes N first pages of nature.com for articles of type X, creates separate directory for each page
 and saves content of the articles to .txt files named after title of the article. 
 Number of pages to scrape N and type of the article X are input by the user"""

# A dict of article types and class attribute values for <div> tag.
# Values of this dict serve as parameters for extract_content function.
types_attributes = {"Research Highlight": "article-item__body",
                    "Book Review": "c-article-body u-clearfix",
                    "News & Views": "c-article-body u-clearfix",
                    "Article": "c-article-body",
                    "Outlook": "c-article-body u-clearfix",
                    "Nature Briefing": "c-article-body u-clearfix",
                    "News Feature": "c-article-body u-clearfix",
                    "News": "c-article-body u-clearfix",
                    "Editorial": "c-article-body u-clearfix",
                    "Comment": "c-article-body u-clearfix",
                    "Futures": "c-article-body u-clearfix",
                    "Career Column": "c-article-body u-clearfix"}


def get_response(url: str, params: dict = None) -> requests.Response:
    """Takes url and optionally parameters (dict) as arguments and returns response object. 
    English version of the page is enforced."""
    if params is None:
        params = {}
    return requests.get(url, params=params, headers={"Accept-Language": "en-US,en;q=0.5"})


def extract_news(response: requests.Response, input_type: str):
    """Extracts hrefs to the articles categorized as input_type and their titles.
    Returns a list of hrefs and a list of titles."""
    if response:
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("article")
        local_hrefs = []
        local_titles = []
        for article in articles:
            article_type = article.find("span", {"class": "c-meta__type"}).text
            if article_type == input_type:
                article = article.find("a", {"data-track-action": "view article"})
                local_titles.append(article.text)
                local_hrefs.append(article.get("href"))
        return local_hrefs, local_titles


def extract_content(href, class_attribute):
    """Extracts the text of the article."""
    local_article_text = ""
    local_soup = BeautifulSoup(requests.get("http://nature.com" + href).content,
                               "html.parser")
    section = local_soup.find("div", {"class": class_attribute})
    paragraphs = section.find_all(["p", "h2", "h3", "h4"])
    unwanted = section.select("p[class], p[data-track], p[data-track-label]")
    for u in unwanted:
        u.extract()  # Removes href to other articles from paragraphs
    for p in paragraphs:
        local_article_text += p.text
    return local_article_text


def save_content(article_title, content, directory):
    """Saves the text of the article to .txt file."""
    t_stripped = article_title.translate(str.maketrans('', '', string.punctuation))
    t_under = t_stripped.replace(" ", "_")
    filepath = os.path.join(directory, t_under + ".txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.basename(filepath)


def main(pages_num, art_type):
    saved_articles = []
    for page_num in range(1, pages_num + 1):
        r = get_response("https://www.nature.com/nature/articles", params={"page": page_num})
        os.mkdir(f"Page_{page_num}")
        if r:
            news_hrefs, titles = extract_news(r, art_type)
            for news, title in zip(news_hrefs, titles):
                article_text = extract_content(news, types_attributes[article_type])
                saved_articles.append(save_content(title, article_text, f"Page_{page_num}"))
            print("Saved articles:", saved_articles)
        else:
            print(f"The URL returned {r.status_code}!")


if __name__ == "__main__":
    pages_number = int(input())  # the number of pages on which the program should look for the articles
    article_type = input()  # type of articles, for example "News"
    main(pages_number, article_type)

