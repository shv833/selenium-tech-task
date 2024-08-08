from app.utils import get_api_info_script


def test_get_api_info_script():
    url = "https://example.com/api"
    key = "my_key"
    host = "example.com"
    script = get_api_info_script(url, key, host)
    assert "xhr.open(" in script
    assert url in script
    assert key in script
    assert host in script
