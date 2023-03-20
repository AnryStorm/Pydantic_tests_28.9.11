from pydantic import BaseModel
import pytest
import requests


class AccessTokenRequest(BaseModel):
    access_token: str

class User(BaseModel):
    id: int
    first_name: str
    last_name: str


def test_access_token_required():
    request = {
        "access_token": "token123"
    }
    AccessTokenRequest(**request)


def test_users_get_response():
    response = [
        {"id": 123, "first_name": "John", "last_name": "Doe"},
        {"id": 456, "first_name": "Jane", "last_name": "Doe"}
    ]
    users = [User(**user) for user in response]



def test_access_token_required():
    request = {}
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def test_access_token_format():
    request = {
        "access_token": "invalid_token_format"
    }
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def test_users_get_success():
    response = [
        {"id": 123, "first_name": "John", "last_name": "Doe"},
        {"id": 456, "first_name": "Jane", "last_name": "Doe"}
    ]
    users = [User(**user) for user in response]
    assert len(users) == 2
    assert users[0].id == 123
    assert users[0].first_name == "John"
    assert users[0].last_name == "Doe"


def test_users_get_no_users():
    response = []
    users = [User(**user) for user in response]
    assert len(users) == 0


def test_user_format():
    user = {
        "id": "invalid_id_format",
        "first_name": "John",
        "last_name": "Doe"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_name_format():
    user = {
        "id": 123,
        "first_name": "John123",
        "last_name": "Doe"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_lastname_format():
    user = {
        "id": 123,
        "first_name": "John",
        "last_name": "Doe123"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_users_get_one_user():
    response = [{"id": 123, "first_name": "John", "last_name": "Doe"}]
    users = [User(**user) for user in response]
    assert len(users) == 1
    assert users[0].id == 123
    assert users[0].first_name == "John"
    assert users[0].last_name == "Doe"



def test_users_get_max_users():
    response = [{"id": i, "first_name": "User", "last_name": str(i)} for i in range(1000)
]
    users = [User(**user) for user in response]
    assert len(users) == 1000
    assert users[-1].id == 999
    assert users[-1].first_name == "User"
    assert users[-1].last_name == "999"


def test_users_get_invalid_response():
    response = [{"invalid_attr": "value"}]
    with pytest.raises(ValueError):
        users = [User(**user) for user in response]
        