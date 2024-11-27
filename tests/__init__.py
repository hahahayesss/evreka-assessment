import pytest


@pytest.fixture(scope="session")
def test_config():
    return {
        "TESTING": True,
        "DB_HOST": "localhost",
        "DB_PORT": 5432,
        "DB_NAME": "test_db",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "RABBITMQ_HOST": "test_rabbitmq"
    }
