import pytest
from core import get_sub_breeds
from helpers import DogsApi


@pytest.mark.api
class TestSmokeDogs:

    def test_check_upload_dog(self, data_dogs: tuple[str, dict, str]):
        domain, headers, breed = data_dogs

        actual_data = DogsApi.create_resources(domain=domain, headers=headers, exp_code=200)

        assert actual_data['type'] == "dir"
        assert actual_data['name'] == "test_folder"
        actual_sub_breeds = get_sub_breeds(breed)
        items = actual_data.get('_embedded').get('items')
        # можно вынести assert-ы в отдельный метод
        if not actual_sub_breeds:
            assert len(items) == 1
            for item in items:
                assert item['type'] == 'file'
                assert item['name'].startswith(breed)
        else:
            assert len(items) == len(actual_sub_breeds)
            for item in items:
                assert item['type'] == 'file'
                assert item['name'].startswith(breed)
