"""
A list of functionalities related to sending/receiving data from the server side
Star Li, listar2000@berkeley.edu
"""
import json
import requests
import os
from urllib.parse import urljoin
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread

# temporary location for base_url (for testing purpose)
BASE_URL = "http://rejection.ocf.berkeley.edu:5000"

# def atlas_request(endpoint, method="POST"):
#     try:
#         requests_method = eval("requests.{}".format(method.lower()))
#     except AttributeError as err:
#         print("package requests doesn't have method {}".format(method))

#     def request_decorator(func):
#         def wrapper(json_resp):
#             path = BASE_URL + endpoint
#             print(requests_method, path)
#             resp = requests_method(path)
#             resp.raise_for_status()
#             return func(Atlas_api_fetcher, resp)
#         return wrapper
#     return request_decorator

# def join_path(routes, url=BASE_URL):
#     routes.insert(0, url)
#     return '/'.join(routes)


class Atlas_api_fetcher(object):
    def __init__(self, base_url=BASE_URL):
        # super().__init__()
        self.base_url = base_url

    # def multi_thread_fn(func):
    #     def wrapper(self, *args, **kwargs):
    #         self.run = func
    #         return self.start()
    #     return wrapper
    # def get_file_list_fn(self):
    #     route = '/files'
    #     resp = requests.get(BASE_URL + route, timeout=5)
    #     resp.raise_for_status()

    #     return resp.json()

    def get_file_list(self):
        # self.run = self.get_file_list_fn
        # return self.start()
        route = "/files"
        resp = requests.get(BASE_URL + route, timeout=5)
        resp.raise_for_status()

        return resp.json()

    """
    progress: the Qt Progress Bar object
    """

    def get_file(self, filename, progress, location="./"):
        route = "/files/" + filename
        resp = requests.get(BASE_URL + route)
        resp.raise_for_status()

        local_name = "/".join([location, filename])

        try:
            with open(local_name, "wb") as f:
                progress.setMaximum(len(resp.content))
                stream_size = 8192
                loaded = 0
                # the below streaming mode is used to handle large (> 5mb) files
                for chunk in resp.iter_content(chunk_size=stream_size):
                    if chunk:
                        f.write(chunk)
                        loaded += stream_size
                        progress.setValue(loaded)
                        QApplication.processEvents()

        except (OSError, TypeError) as error:
            if os.path.isfile(local_name):
                os.remove(local_name)
            return False

        return True

    def upload_file(self, filename):
        # use suffix instead
        suffix = filename.split("/")[-1]
        route = "/files/" + suffix
        with open(filename, "rb") as f:
            resp = requests.post(BASE_URL + route, data=f.read())
            resp.raise_for_status()


# testing
if __name__ == "__main__":
    fetcher = Atlas_api_fetcher()
    status = fetcher.get_file("scene0400_00_vh_clean_2.ply")
    print(status)
