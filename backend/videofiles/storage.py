from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.conf import settings
import requests
from django.core.files import File
import json
from rest_framework.response import Response


class CDNVideoApi:
    base_files_url = None
    token_data = None
    username = None
    email = None
    password = None

    def __init__(self, *, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        # https://doc.cdnvideo.ru/api_desc/api_desc/#%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81
        # {"status": 200, "person_id": 8502, "token": "cdn2_7A9ARL2KRMJ3HD8YS5I148BB55VS0C", "lifetime": 21599000}

    @property
    def token(self):
        return self.token_data['token']
    
    def get_url(self):
        return f"https://api.cdnvideo.ru/app/storage/v1/{self.username}/files/"

    def fetch_token(self):
        if self.token_data:
            return self.token_data
        token_request = requests.post("https://api.cdnvideo.ru/app/oauth/v1/token/", data={
            "username": self.email,
            "password": self.password
        })

        if token_request.status_code != 200:
            # TODO: need raise exception
            raise Exception("Incorrect CDN VIDEO credentials", token_request)

        token_data = json.loads(token_request.text)
        self.token_data = token_data
        return token_data

    def is_error_response(self, json_content, raise_exception=False):
        if json_content.get('status') == 'error':
            if raise_exception:
                # TODO: error of request
                raise Exception(json_content)
            return False
        return False

    def upload_file(self, filename, file):  # file - TemporaryUploadedFile
        multipart_form_data = {
            "file": file
        }
        save_request = requests.post(
            f"{self.base_files_url}{filename}", headers={"CDN-AUTH-TOKEN": self.token}, files=multipart_form_data)

        if save_request.status_code != 201:
            raise Exception(save_request.text)

        content = json.loads(save_request.text)
        if content.get('status') != 'Completed':
            raise Exception(content)
        return content

    def get_file_or_dir(self, path_to_file):
        request_file = requests.get(f"{self.base_files_url}{path_to_file}", headers={
                                    "CDN-AUTH-TOKEN": self.token})
        if request_file.status_code == 404:
            # TODO: not found error
            print(request_file)
            raise Exception(request_file.text)
        if request_file.status_code == 420:
            # TODO: Ошибка в значениях параметров (см. description)
            raise Exception(request_file.error)
        content = json.loads(request_file.text)
        if content.get('status') != 'Completed':
            raise Exception(content)
        return content.get('data')

    def remove_file(self, path):
        request_remove_file = requests.delete(f"{self.base_files_url}{path}", headers={
                                              "CDN-AUTH-TOKEN": self.token})
        if request_remove_file.status_code != 204:
            raise Exception(request_remove_file.text)

@deconstructible
class CDNVideoStorageFile(Storage):
    api = None
    def __init__(self, *, api, **kwargs):
        self.api = api
        super().__init__(**kwargs)

    def _open(self, name, mode):
        try:
            request_file = self.api.get_file_or_dir(name)
        except:
            return ""
        return request_file

    def _save(self, name, content):
        request_save_file = self.api.upload_file(name, content)
        self.api.is_error_response(request_save_file, raise_exception=True)
        return name

    def exists(self, name: str) -> bool:
        try:
            self.api.get_file_or_dir(name)
        except:
            return False
        return True

    def url(self, name):
        try:
            request_file = self.api.get_file_or_dir(name)
        except:
            return ""
        return request_file.get('download_url')

    def delete(self, name: str) -> None:
        # TODO: Not work
        self.api.remove_file(name)
