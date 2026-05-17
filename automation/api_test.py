import os
import requests
import pytest

BASE_URL = "https://reqres.in/api"


def get_headers():
    # reqres.in doesn't require authentication
    return {"Content-Type": "application/json"}


def test_create_user():
    payload = {"name": "Automation User", "job": "QA Engineer"}
    response = requests.post(f"{BASE_URL}/users", json=payload, headers=get_headers())
    assert response.status_code == 201
    body = response.json()
    assert body.get("name") == payload["name"]
    assert body.get("job") == payload["job"]
    assert body.get("id") is not None
    assert body.get("createdAt") is not None


def test_read_user():
    response = requests.get(f"{BASE_URL}/users/2", headers=get_headers())
    assert response.status_code == 200
    body = response.json()
    assert body.get("data") is not None
    assert body["data"]["id"] == 2


def test_update_user():
    payload = {"name": "Automation User Updated", "job": "Senior QA"}
    response = requests.put(f"{BASE_URL}/users/2", json=payload, headers=get_headers())
    assert response.status_code == 200
    body = response.json()
    assert body.get("name") == payload["name"]
    assert body.get("job") == payload["job"]
    assert body.get("updatedAt") is not None


def test_delete_user():
    response = requests.delete(f"{BASE_URL}/users/2", headers=get_headers())
    assert response.status_code == 204


def test_invalid_endpoint_returns_404():
    response = requests.get(f"{BASE_URL}/invalid-endpoint", headers=get_headers())
    assert response.status_code == 404


def test_invalid_payload_returns_error():
    response = requests.post(f"{BASE_URL}/users", json={"invalid": "field"}, headers=get_headers())
    assert response.status_code in (201, 400)
    if response.status_code == 400:
        assert response.json().get("error") is not None


def test_get_non_existing_user():
    response = requests.get(f"{BASE_URL}/users/999", headers=get_headers())
    assert response.status_code == 404