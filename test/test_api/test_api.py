import os

import requests
from dotenv import load_dotenv

load_dotenv()

TFL_APP_KEY = os.getenv("TFL_APP_KEY")


def test_api():
    response = requests.get(
        "https://api.tfl.gov.uk/Line/Mode/tube/Status",
        params={"app_key": TFL_APP_KEY},
    )
    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    test_api()
