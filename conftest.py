import pytest

from config import TOKEN
from core import u


@pytest.fixture(
    scope="function",
    params=[
        pytest.param(
            "doberman",
            id="doberman",
        ),
        pytest.param(
            "bulldog",
            id="bulldog",
        ),
        pytest.param(
            "collie",
            id="collie",
        ),
    ],
)
def data_dogs(request) -> tuple[str, dict, str]:
    breed = request.param
    domain = 'https://cloud-api.yandex.net'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'OAuth {TOKEN}'
    }
    u(breed, TOKEN)
    return domain, headers, breed

