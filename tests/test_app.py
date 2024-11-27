import json
import pytest
from app.app import app
from unittest import mock


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_submit_location(client, mocker):
    # given
    mock_send_to_queue = mocker.patch(
        "app.app._send_to_queue",
        return_value=None
    )

    payload = {
        "device_id": "device_1337",
        "latitude": 41.021629,
        "longitude": 28.994048,
        "speed": 13.37,
        "timestamp": "2024-11-11T13:37:23Z"
    }

    # when
    response = client.post(
        "/api/locations",
        data=json.dumps(payload),
        content_type="application/json"
    )

    # then
    assert response.status_code == 200
    assert response.json["message"] == "Data submitted successfully"
    mock_send_to_queue.assert_called_once_with(payload)


def test_get_data_by_date_range(client, mocker):
    # given
    mock_find_by_range = mocker.patch("app.repository.find_by_range")
    mock_find_by_range.return_value = [
        {
            "id": 1,
            "device_id": "device_1337",
            "latitude": 41.021629,
            "longitude": 28.994048,
            "speed": 13.37,
            "timestamp": "2024-11-11T13:37:23Z"
        }
    ]

    # when
    response = client.get(
        "/api/locations/range",
        query_string={
            "device_id": "device_1337",
            "start_date": "2024-11-10T13:37:23Z",
            "end_date": "2024-11-12T13:37:23Z"
        }
    )

    # then
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["device_id"] == "device_1337"


def test_get_latest_location(client, mocker):
    # given
    mock_find_by_latest = mocker.patch("app.repository.find_by_latest")
    mock_find_by_latest.return_value = {
        "id": 1,
        "device_id": "device_1337",
        "latitude": 41.021629,
        "longitude": 28.994048,
        "speed": 13.37,
        "timestamp": "2024-11-11T13:37:23Z"
    }

    # when
    response = client.get(
        "/api/locations/latest",
        query_string={
            "device_id": "device_1337"
        }
    )

    # then
    assert response.status_code == 200
    assert response.json["device_id"] == "device_1337"
