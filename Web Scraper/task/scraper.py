import requests
from bs4 import BeautifulSoup


"""This script takes a link to a movie or tv show description and prints scraped title and description to the console.
It displays "Invalid movie page!" for other websites. Tested for imbd."""


def get_response(url: str, params: dict = None) -> requests.Response:
    """Takes url and optionally parameters (dict) as arguments and returns response object. 
    English version of the page is enforced."""
    if params is None:
        params = {}
    return requests.get(url, params=params, headers={"Accept-Language": "en-US,en;q=0.5"})


def extract_title(response: requests.Response):
    """Parses page content for title and description of the film. Returns dictionary object containing title
     and description. If there is no title and description or there is no response, it returns error message."""
    fail_str = "Invalid movie page!"
    if response.status_code:
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.text
        description = soup.find('meta', {'name': 'description'})["content"]
        if title and description:
            return {"title": title, "description": description}
    else:
        return fail_str


if __name__ == "__main__":
    user_url = input("Input the URL:\n")
    if "title" in user_url:
        r = get_response(user_url)
        print(extract_title(r))
    else:
        print("Invalid movie page!")
