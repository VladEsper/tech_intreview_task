import requests

from gears import trans_json


class DogsApi:
    def __init__(self):
        self.session = requests.Session()

    def create_resources(self, domain: str, headers: dict, exp_code: int = 200) -> dict:
        response = self.session.get(url=f"{domain}/v1/disk/resources", headers=headers)
        if response.status_code == exp_code:
            return trans_json(response) # добавить класс апи клиента в котором вынести все методы post, put, get, где сделать проверки и преобразования json в словарь
        else:
            raise Exception(f"Unexpected response code: {response.status_code}")