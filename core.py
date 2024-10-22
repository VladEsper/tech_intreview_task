import requests
from typing import List

from gears import trans_json


class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {token}'
        }
        self.session = requests.Session()

    def create_folder(self, path: str) -> int:
        url_create = 'https://cloud-api.yandex.net/v1/disk/resources'
        response = self.session.put(f'{url_create}?path={path}', headers=self.headers)
        if response.status_code == 201:
            return response.status_code
        else:
            raise Exception(f"Error creating folder: {response.status_code}")


    def upload_photos_to_yd(self, path: str, url_file: str, name: str) -> int:
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {
            "path": f'/{path}/{name}',
            'url': url_file,
            "overwrite": "true"
        }
        response = self.session.post(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.status_code
        else:
            raise Exception(f"Error uploading photo: {response.status_code}")

    def delete_folder(self, path: str) -> int:
        url_delete = 'https://cloud-api.yandex.net/v1/disk/resources/delete'
        response = self.session.delete(f'{url_delete}?path={path}')
        if response.status_code == 200:
            return response.status_code
        else:
            raise Exception(f"Error deleting folder: {response.status_code}") # можно использовать для очистки созданных ресурсов в конце теста


def get_sub_breeds(breed: str) -> List[str]:
    response = requests.get(f'https://dog.ceo/api/breed/{breed}/list')
    if response.status_code == 200:
        return trans_json(response).get('message', [])
    else:
        raise Exception(f"Error get sub breeds: {response.status_code}")


def get_urls(breed: str, sub_breeds: List[str]) -> List[str]:
    url_images = []
    if sub_breeds:
        for sub_breed in sub_breeds:
            response = requests.get(f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random")
            sub_breed_urls = trans_json(response).get('message')
            url_images.extend(sub_breed_urls)
    else:
        response = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
        breed_urls = trans_json(response).get('message') # можно вынести в отдельную функцию, так как есть дублирование
        url_images.extend(breed_urls) # можно вынести в отдельную функцию, так как есть дублирование
    return url_images


def u(breed: str, token: str):
    sub_breeds = get_sub_breeds(breed)
    urls = get_urls(breed, sub_breeds)
    yandex_client = YaUploader(token)
    yandex_client.create_folder('test_folder')
    for url in urls:
        part_name = url.split('/')
        name = '_'.join([part_name[-2], part_name[-1]])
        yandex_client.upload_photos_to_yd("test_folder", url, name)
