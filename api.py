import requests
from typing import List

API = "http://rejection.ocf.berkeley.edu:5000"

DATA_DIRECTORY = "./data"


def list_remote_files() -> List[str]:
    """
    Returns a list of files on server
    """
    r = requests.get(url=API + "/files")
    return r.json()


def get_file(filename: str) -> None:
    """
    Saves file to data directory
    """
    r = requests.get(url=API + "/files/" + filename)
    file = open(DATA_DIRECTORY + "/" + filename, "w")
    file.write(r.text)
    file.close()
    print(r)


def upload_file(filename: str) -> None:
    """
    Uploads file from data directory
    """
    file = open(DATA_DIRECTORY + "/" + filename, mode="r")
    file_data = file.read()
    file.close()
    r = requests.post(url=API + "/files/" + filename, data=file_data)
    print(r)
