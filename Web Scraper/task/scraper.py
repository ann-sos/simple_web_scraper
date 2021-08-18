import requests


def get_response(url, params=None):
    if params is None:
        params = {}
    return requests.get(url, params=params)


def extract_quote(response):
    fail_str = "Invalid quote resource!"
    if response.status_code:
        return response.json().get('content', fail_str)
    else:
        return fail_str


if __name__ == "__main__":
    r = get_response(input("Input the URL:\n"))
    print(extract_quote(r))