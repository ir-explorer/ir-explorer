import requests


def test_languages(api):
    x = requests.get(f"{api}/get_available_languages")
    assert x.json() == ["English"]
