import pytest
import requests

@pytest.fixture
def url():
    return "http://127.0.0.1:5000"

@pytest.mark.api
def test_get_all_links(url):
    r = requests.get(f"{url}/get_all", verify=False)
    assert r.status_code == 200
    # TODO: more checks
