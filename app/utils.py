from functools import wraps
from selenium import webdriver


def get_api_info_script(URL, KEY, HOST):
    return """
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "%s", false);
    xhr.setRequestHeader("x-rapidapi-key", "%s");
    xhr.setRequestHeader("x-rapidapi-host", "%s");
    xhr.send(null);
    return xhr.responseText;
    """ % (
        URL,
        KEY,
        HOST,
    )


def with_webdriver(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")

        hub_url = "http://chrome:4444/wd/hub"
        driver = webdriver.Remote(command_executor=hub_url, options=options)

        try:
            result = func(driver, *args, **kwargs)
        except Exception as e:
            print(e)
            raise
        finally:
            try:
                driver.quit()
            except Exception as quit_exception:
                print(quit_exception)

        return result

    return wrapper
