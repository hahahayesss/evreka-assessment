import pytest
import json
from unittest.mock import Mock
from app.consumer import callback


@pytest.fixture
def mock_channel():
    channel = Mock()
    channel.basic_ack = Mock()
    return channel


def test_callback(mock_channel, mocker):
    # given
    mock_insert = mocker.patch("app.repository.insert")
    message_data = {
        "device_id": "device_1337",
        "latitude": 41.021629,
        "longitude": 28.994048,
        "speed": 13.37,
        "timestamp": "2024-11-11T13:37:23Z"
    }
    message_body = json.dumps(message_data).encode()

    # when
    callback(mock_channel, Mock(), Mock(), message_body)

    # then
    mock_insert.assert_called_once_with("device_1337", 41.021629, 28.994048, 13.37, "2024-11-11T13:37:23Z")
    mock_channel.basic_ack.assert_called_once()
