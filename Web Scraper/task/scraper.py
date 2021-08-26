import requests
from bs4 import BeautifulSoup


"""Saves the content of the website to the source.html and notifies about success/failure of the operation. 
URI is provided via user input."""


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


def save_content(res: requests.Response):
    """Saves the page website data to source.html"""
    with open("source.html", "wb") as f:
        f.write(res.content)


if __name__ == "__main__":
    user_url = input("Input the URL:\n")
    r = get_response(user_url)
    if r:
        print(r.status_code)
        save_content(r)
        print("Content saved.")
    else:
        print(f"The URL returned {r.status_code}!")
