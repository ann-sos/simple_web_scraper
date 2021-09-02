import pytest
import requests
from scraper import get_response


def test_gest_response(requests_mock):
        url = "https://www.nature.com/nature/articles"
        requests_mock.get(url+'?page=3', status_code=200)
        assert get_response(url, {"page": 3}).status_code == 200

