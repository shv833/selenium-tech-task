from app.utils import get_api_info_script


def test_get_api_info_script(subtests):
    url = "https://example.com/api"
    key = "my_key"
    host = "example.com"
    script = get_api_info_script(url, key, host)

    with subtests.test("Check if script contains 'xhr.open'"):
        assert "xhr.open(" in script

    with subtests.test("Check if script contains URL"):
        assert url in script

    with subtests.test("Check if script contains key"):
        assert key in script

    with subtests.test("Check if script contains host"):
        assert host in script
