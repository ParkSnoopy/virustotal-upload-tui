import requests
import questionary
from pathlib import Path

from dotenv import dotenv_values

CONFIG = dotenv_values(".env")



def upload_once(filename:str) -> str:
    files = {
        "file": (
            filename,
            open(filename, "rb"),
            "application/x-compressed",
        )
    }

    headers = {
        "accept": "application/json",
        "x-apikey": CONFIG['APIKEY'],
    }

    upload_response = requests.post(
        CONFIG['URL_UPLOAD'],
        files=files,
        headers=headers,
    )

    file_id = (
        upload_response
            .json()
            ['data']
            ['id']
    )

    report_response = requests.get(
        CONFIG['URL_REPORT'].format(file_id=file_id),
        headers=headers,
    )

    file_checksum = (
        report_response
            .json()
            ['meta']
            ['file_info']
            ['sha256']
    )

    return CONFIG['URL_GUI'].format(
        file_checksum=file_checksum,
    )



if __name__ == "__main__":
    filenames = list()

    while True:
        filename = questionary.path(
            "Select file to Upload: "
        ).ask()

        if Path(filename).is_file():
            filenames.append(filename)
        else:
            break

    for filename in filenames:
        print(f"  `{upload_once(filename)}` : '{filename}'")
