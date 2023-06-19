import pytest
import requests

from resources.config import URL, ADMIN
from resources.helpers import generate_random_string


def test_01_get_brands():
    response = requests.get(f"{URL}/brands")

    assert response.status_code == 200, f"Unexpected status code {response.status_code}"
    assert len(response.json()) > 0, "Brand list is empty"


def test_02_post_brand():
    brand = generate_random_string(7)
    payload = {
        "name": f"new brand {brand}",
        "slug": f"new-brand-{brand}"
    }
    response = requests.post(f"{URL}/brands", json=payload)

    assert response.status_code == 201, f"Unexpected status code {response.status_code}"
    assert response.json()["name"] == payload["name"]
    assert response.json()["slug"] == payload["slug"]


def test_03_put_brand():
    brand = generate_random_string(7)
    payload = {
        "name": f"new brand {brand}",
        "slug": f"new-brand-{brand}"
    }
    response = requests.post(f"{URL}/brands", json=payload)

    brand_id = response.json()["id"]
    payload_update = {
        "name": f"new brand {brand} update",
        "slug": f"new-brand-{brand}-update"
    }
    response_update = requests.put(f"{URL}/brands/{brand_id}", json=payload_update)
    assert response_update.status_code == 200
    assert response_update.json()["success"] is True


@pytest.mark.parametrize("token", [{"email": ADMIN}], indirect=True)
def test_004_delete_brand(token):
    brand = generate_random_string(7)
    payload = {
        "name": f"new brand {brand}",
        "slug": f"new-brand-{brand}"
    }
    response = requests.post(f"{URL}/brands", json=payload)

    brand_id = response.json()["id"]

    headers = {"Authorization": f"Bearer {token}"}
    response_delete = requests.delete(f"{URL}/brands/{brand_id}", headers=headers)
    assert response_delete.status_code == 204


def test_005_will_pass():
    assert True is True


def test_006_will_fail():
    assert False is True


@pytest.mark.skip()
def test_007_this_test_is_skipped():
    assert False is False
